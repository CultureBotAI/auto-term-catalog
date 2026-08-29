#!/usr/bin/env python3
"""Add a `full_scientific_name` column ("Genus species STRAIN") to strain rows of an
extraction + grounding table (issue #1).

The table has one row per extracted entity mention; `field == "strains"` rows carry a bare
designation (`G39T`, `DSM 14988`) and `field == "study_taxa"` rows carry the binomials the
paper discusses. Nothing links the two, so the link is inferred from the strain row's
`context` (mention marked `[[…]]`) using, in priority order:

  1. preceding_binomial  — a binomial immediately precedes the mention
                            (`Qipengyuania profundimaris [[G39T]]`); accepted if it (or its
                            abbreviated form `Q. profundimaris`) matches a study_taxa label of
                            the same document, or (`preceding_binomial_genus`) if at least its
                            genus occurs among the document's study_taxa.
  2. sp_nov              — `Genus species sp. nov. … (type strain[:] [[X]]` or
                            `strain [[X]] … Genus species sp. nov.` within one context snippet
                            with no competing strain designation in between.
  3. type_strain_novel   — the snippet says `type strain is/: [[X]]` (or holotype / ex-type
                            culture) but the binomial was cut off by the snippet boundary
                            (`…yangense is proposed. The type strain is [[X]]`). The document's
                            *novel* taxa (study_taxa rows whose own context reads
                            `[[Genus species]] sp. nov.`) are suffix-matched against the cut
                            fragment; if the document has a single novel taxon it is used directly.
  4. equivalence         — the mention is an `=`-linked synonym of another designation in the
                            same document (`COJ-58T (=[[KACC 22108T]]`) whose name was resolved
                            by an earlier rule; iterated so chains resolve.

No document-level fallback is used: a document's only study_taxa row is frequently the host
organism (`Tenebrio molitor`), not the isolate's species.

Rows that no rule resolves keep an empty `full_scientific_name`.

Usage:
    python full_scientific_name.py TABLE.tsv --out TABLE.full_names.tsv [--strains-only]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

BINOMIAL = r"[A-Z][a-z]+ [a-z]{3,}(?: subsp\. [a-z]{3,})?"
ABBREV = r"[A-Z]\. [a-z]{3,}(?: subsp\. [a-z]{3,})?"
NON_SPECIES = {"strain", "strains", "type", "novel", "isolate", "isolates", "species", "genus", "with", "and", "the",
               "proposed", "designated", "named", "culture", "cultures", "holotype"}
NON_GENUS = {"In", "While", "Both", "Strain", "Strains", "Type", "The", "Novel", "Two", "Three", "Four", "Five", "Six",
             "Species", "Genus", "For", "Among", "From", "With", "Based", "These", "This", "That", "Their", "Its",
             "However", "Here", "Phylogenetic", "Genomic", "Colonies", "Cells", "Growth", "Optimal"}
TYPE_STRAIN_MENTION = re.compile(
    r"(?:type strain(?: is| was|:|,)?|holotype(?: is|:)?|ex-type (?:culture|strain)(?: is|:)?)\s*(?:strain\s+)?\[\[", re.I
)
NOVEL_TAXON_CTX = re.compile(r"\]\](?: f\.a\.,?)?(?: gen\. nov\.,?)? sp\. nov\.")
CUT_FRAGMENT = re.compile(r"^\.\.\.(\S*?)(?: f\.a\.,?)?(?: gen\. nov\.,?)? sp\. nov\.|^\.\.\.(\S+) is proposed")
MENTION = re.compile(r"\[\[(.+?)\]\]")
PRECEDING = re.compile(rf"({BINOMIAL}|{ABBREV})\s+\[\[")
SP_NOV_BEFORE = re.compile(
    rf"({BINOMIAL})(?: gen\. nov\.,?)?(?: sp\. nov\.)?[^;\[]*?\(?\s*type strain[:,]?\s*(?:is\s+)?(?:strain\s+)?\[\["
)
SP_NOV_AFTER = re.compile(
    rf"strain\s+\[\[[^\]]+\]\][^;\[]*?(?:as|represents?|is proposed as|be classified as|to accommodate)[^;\[]*?({BINOMIAL})(?: gen\. nov\.,?)? sp\. nov\."
)
EQUIV = re.compile(r"([A-Za-z0-9][A-Za-z0-9\-\./ ]{1,30}?T?)\s*\(\s*=\s*\[\[")  # `COJ-58T (=[[KACC 22108T]]`
EQUIV_CHAIN = re.compile(r"=\s*\[\[")


def norm_taxon(t: str) -> str:
    return re.sub(r"\s+", " ", t.strip())


def doc_taxa_index(taxa: list[str]) -> tuple[set[str], dict[str, str]]:
    """Full binomials of a document plus a map from abbreviated form (`Q. profundimaris`) to full."""
    full = {norm_taxon(t) for t in taxa if re.fullmatch(BINOMIAL, norm_taxon(t))}
    abbrev = {}
    for t in full:
        genus, rest = t.split(" ", 1)
        abbrev.setdefault(f"{genus[0]}. {rest}", t)
    return full, abbrev


def expand(name: str, full: set[str], abbrev: dict[str, str]) -> str:
    """Return the full binomial if `name` is a known taxon of the document (full or abbreviated), else ''."""
    name = norm_taxon(name)
    if name in full:
        return name
    if name in abbrev:
        return abbrev[name]
    return ""


def rule_preceding(context: str, full: set[str], abbrev: dict[str, str]) -> tuple[str, str]:
    """Returns (taxon, source). Exact/abbreviated match against the document's taxa first; then a
    clean binomial whose genus is among the document's taxa genera."""
    genera = {t.split(" ")[0] for t in full}
    genus_hit = ""
    for m in PRECEDING.finditer(context):
        cand = norm_taxon(m.group(1))
        genus, species = cand.split(" ")[0], cand.split(" ")[1]
        if species in NON_SPECIES or genus in NON_GENUS:
            continue
        hit = expand(cand, full, abbrev)
        if hit:
            return hit, "preceding_binomial"
        if not genus_hit and "." not in genus and genus in genera:
            genus_hit = cand
    return (genus_hit, "preceding_binomial_genus") if genus_hit else ("", "")


def rule_type_strain_novel(context: str, label: str, novel: list[str]) -> str:
    """`type strain is [[X]]` with the binomial cut off by the snippet boundary: match the cut
    fragment (`...yangense is proposed`) against the document's novel taxa."""
    if not novel:
        return ""
    for snippet in context.split("; "):
        if f"[[{label}]]" not in snippet or not TYPE_STRAIN_MENTION.search(snippet):
            continue
        # a full binomial in the snippet is handled by rule_sp_nov; here only the cut case
        m = CUT_FRAGMENT.search(snippet)
        frag = (m.group(1) or m.group(2)) if m else ""
        if frag:
            frag = frag.strip(".,;:")
            cands = [t for t in novel if t.split(" ")[-1].endswith(frag) or t.endswith(frag)]
            if len(cands) == 1:
                return cands[0]
        before = snippet.split("[[")[0]
        if len(novel) == 1 and not re.search(r"\bsp\. nov\.", before) and not re.search(BINOMIAL, before):
            # nothing else identifies the species and the paper proposes exactly one
            return novel[0]
    return ""


def rule_sp_nov(context: str, label: str, full: set[str], abbrev: dict[str, str]) -> str:
    for snippet in context.split("; ..."):
        if f"[[{label}]]" not in snippet:
            continue
        for rx in (SP_NOV_BEFORE, SP_NOV_AFTER):
            m = rx.search(snippet)
            if m:
                cand = norm_taxon(m.group(1))
                # ensure the sp. nov. binomial and the marked strain are the nearest pair (no other designation between)
                between = snippet[m.start(): m.end()]
                if len(re.findall(r"\b[A-Z]{1,6}[\-\s]?\d[\w\-\.]*T\b", between.replace(f"[[{label}]]", ""))) > 1:
                    continue
                if cand.split(" ")[1] in NON_SPECIES:
                    continue
                return cand if cand in full or not full else cand
    return ""


def rule_equivalence(context: str, resolved: dict[str, str]) -> tuple[str, str]:
    """Mention is `X (=[[this]]…)` or `…=[[this]]` — find the primary designation X and its resolved name."""
    for m in EQUIV.finditer(context):
        primary = m.group(1).strip()
        if primary in resolved and resolved[primary]:
            return resolved[primary], primary
    # chained: `H3SJ34-1T=[[JCM 36465T]]=CGMCC …` — take the token before `=[[`
    for m in re.finditer(r"([A-Za-z0-9][A-Za-z0-9\-\./ ]{1,30}?)\s*=\s*\[\[", context):
        primary = m.group(1).strip()
        if primary in resolved and resolved[primary]:
            return resolved[primary], primary
    return "", ""


def add_full_names(df: pd.DataFrame) -> pd.DataFrame:
    need = {"doc", "field", "label", "context"}
    missing = need - set(df.columns)
    if missing:
        raise SystemExit(f"error: table lacks required columns {sorted(missing)}")
    df = df.copy()
    df["full_scientific_name"] = ""
    df["name_source"] = ""
    df["taxon_label"] = ""

    taxa_rows = df[df["field"] == "study_taxa"]
    taxa_by_doc = taxa_rows.groupby("doc")["label"].apply(list).to_dict()
    novel_by_doc = (
        taxa_rows[taxa_rows["context"].str.contains(NOVEL_TAXON_CTX)]
        .groupby("doc")["label"].apply(lambda s: sorted({norm_taxon(x) for x in s if re.fullmatch(BINOMIAL, norm_taxon(x))}))
        .to_dict()
    )
    strain_idx = df.index[df["field"] == "strains"]

    # pass 1: rules 1-2 and 4
    resolved_by_doc: dict[str, dict[str, str]] = {}
    for i in strain_idx:
        doc, label, ctx = df.at[i, "doc"], df.at[i, "label"], df.at[i, "context"]
        full, abbrev = doc_taxa_index(taxa_by_doc.get(doc, []))
        taxon, src = "", ""
        if ctx:
            taxon, src = rule_preceding(ctx, full, abbrev)
            if not taxon:
                taxon = rule_sp_nov(ctx, label, full, abbrev)
                src = "sp_nov" if taxon else ""
            if not taxon:
                taxon = rule_type_strain_novel(ctx, label, novel_by_doc.get(doc, []))
                src = "type_strain_novel" if taxon else ""
        if taxon:
            df.at[i, "taxon_label"], df.at[i, "name_source"] = taxon, src
            df.at[i, "full_scientific_name"] = f"{taxon} {label}"
            resolved_by_doc.setdefault(doc, {})[label] = taxon

    # pass 2: equivalence (needs earlier results of the same doc); iterate so `A=B=C` chains resolve
    for _ in range(3):
        changed = False
        for i in strain_idx:
            if df.at[i, "full_scientific_name"]:
                continue
            doc, label, ctx = df.at[i, "doc"], df.at[i, "label"], df.at[i, "context"]
            if not ctx:
                continue
            taxon, primary = rule_equivalence(ctx, resolved_by_doc.get(doc, {}))
            if taxon:
                df.at[i, "taxon_label"], df.at[i, "name_source"] = taxon, f"equivalence:{primary}"
                df.at[i, "full_scientific_name"] = f"{taxon} {label}"
                resolved_by_doc.setdefault(doc, {})[label] = taxon
                changed = True
        if not changed:
            break
    return df


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("table", type=Path, help="extraction + grounding TSV/CSV")
    ap.add_argument("--out", type=Path, help="output path (default: <table>.full_names.tsv next to input)")
    ap.add_argument("--strains-only", action="store_true", help="write only field == strains rows")
    args = ap.parse_args()

    with open(args.table, encoding="utf-8") as fh:
        header = fh.readline()
    sep = "\t" if header.count("\t") >= header.count(",") else ","
    df = pd.read_csv(args.table, sep=sep, dtype=str, keep_default_na=False)
    out = add_full_names(df)

    st = out[out["field"] == "strains"]
    n = len(st)
    print(f"strain rows: {n:,}", file=sys.stderr)
    for src, cnt in st["name_source"].str.split(":").str[0].replace("", "(unresolved)").value_counts().items():
        print(f"  {src:20s} {cnt:6,} ({cnt / n * 100:.1f}%)", file=sys.stderr)

    if args.strains_only:
        out = st
    dest = args.out or args.table.with_suffix("").with_suffix(".full_names.tsv")
    out.to_csv(dest, sep="\t", index=False)
    print(f"wrote {dest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
