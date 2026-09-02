#!/usr/bin/env python3
"""Add a `full_scientific_name` column ("Genus species STRAIN") to strain rows of an
extraction + grounding table (issue #1).

The table has one row per extracted entity mention; `field == "strains"` rows carry a bare
designation (`G39T`, `DSM 14988`) and `field == "study_taxa"` rows carry the binomials the
paper discusses. Nothing links the two, so the link is inferred from the strain row's
`context` (mention marked `[[…]]`) using, in priority order:

  1. preceding_binomial  — a binomial (optionally followed by `strain`/punctuation) precedes the mention
                            (`Qipengyuania profundimaris [[G39T]]`); accepted if it (or its
                            abbreviated form `Q. profundimaris`) matches a study_taxa label of
                            the same document, or (`preceding_binomial_genus`) if at least its
                            genus occurs among the document's study_taxa. `Genus sp. [[X]]`
                            yields `Genus sp. X` (`preceding_genus_sp`).
  2. sp_nov              — `Genus species sp./subsp./comb./nom. nov. … (type strain(s)[:] [[X]]`,
                            `Genus species (type strain, [[X]]`, or `strain [[X]] … Genus species
                            sp. nov.` within one context snippet with no competing strain
                            designation in between. The binomial is validated against the
                            document's study_taxa (exact, abbreviated, or ≤2-edit typo of a
                            listed species; else same genus).
  3. type_strain_novel   — the snippet says `type strain is/: [[X]]` (or holotype / ex-type
                            culture) but the binomial was cut off by the snippet boundary
                            (`…yangense is proposed. The type strain is [[X]]`). The document's
                            *novel* taxa (study_taxa rows whose own context reads
                            `[[Genus species]] sp. nov.`) are suffix-matched against the cut
                            fragment; if the document has a single novel taxon it is used directly,
                            provided nothing before the mention names another taxon (no binomial,
                            abbreviation, `… nov.` or `type strain of`) and the label itself is not
                            a binomial.
  4. label_binomial      — the label itself opens with its binomial or an abbreviation of it
                            (`Gordonia otitidis NBRC 100426T`, `M. smithii DSM 861`): preferred
                            spelling comes from the document's study_taxa (expand/validate),
                            else the label is accepted as spelled. Runs only when no context
                            rule fired, and never on family/order + placeholder-word labels
                            (`Burkholderiaceae bacterium PBA`) unless the document lists them.
  5. equivalence         — the mention is an `=`-linked synonym of another designation in the
                            same document (`COJ-58T (=[[KACC 22108T]]`) whose name was resolved
                            by an earlier rule; iterated so chains resolve.

No document-level fallback is used: a document's only study_taxa row is frequently the host
organism (`Tenebrio molitor`), not the isolate's species.

Rows that no rule resolves keep an empty `full_scientific_name`. A QC warning lists documents
where one taxon is assigned to several distinct type-strain (`…T`) designations that are not
`=`-linked in any context.

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
# `Genus species [[X]]`, `'Genus species' [[X]]`, `Genus species strain [[X]]`. A comma (`as H. floricola, strain
# [[X]]`) means the binomial is a comparator, not the strain's species, so it is deliberately not accepted.
PRECEDING = re.compile(rf"({BINOMIAL}|{ABBREV})(?: corrig\.)?['’]?\s+(?:strain\s+)?\[\[")
GENUS_SP = re.compile(r"([A-Z][a-z]{3,}) sp\.\s+(?:strain\s+)?\[\[")
NOV = r"(?: gen\. nov\.,?)?(?: (?:sp|subsp|comb|nom)\. nov\.)"
SP_NOV_BEFORE = re.compile(
    rf"({BINOMIAL}){NOV}[^;\[]*?\(?\s*type strains?[:,]?\s*(?:is\s+|are\s+)?(?:strain\s+)?\[\["
)
TYPE_STRAIN_PAREN = re.compile(rf"({BINOMIAL}) \(type strain[:,]?\s*\[\[")  # `Genus species (type strain, [[X]]`
SP_NOV_AFTER = re.compile(
    rf"strain\s+\[\[[^\]]+\]\][^;\[]*?(?:as|represents?|is proposed as|be classified as|to accommodate)[^;\[]*?({BINOMIAL})(?: gen\. nov\.,?)? sp\. nov\."
)
# `COJ-58T (=[[KACC 22108T]]`, `H3SJ34-1T=[[JCM 36465T]]`, `type strain lpD01T = [[X]]`: the primary designation
# is the last one or two whitespace tokens before `(=` / `=`.
EQUIV = re.compile(r"(\S+(?: \S+)?)\s*\(?\s*=\s*\[\[")
# label opens with a binomial/abbreviation followed by the strain designation
LABEL_BINOMIAL = re.compile(rf"^({BINOMIAL}|{ABBREV})['’]?\s+(\S.*)$")
# words that make a label-only candidate a taxon placeholder, not a binomial
NON_SPECIES_IN_LABEL = {"bacterium", "bacteria", "archaeon", "archaea"}


def compose(taxon: str, label: str) -> str:
    """`Genus species STRAIN`; if the label already carries that binomial (`Gardnerella vaginalis 6119V5`)
    or an abbreviation of it (`G. vaginalis 6119V5`), return the label with the binomial expanded."""
    label = norm_taxon(label)
    if label.startswith(taxon + " ") or label == taxon:
        return label
    genus, rest = taxon.split(" ", 1)
    ab = f"{genus[0]}. {rest}"
    if label == ab:
        return taxon
    if label.startswith(ab + " "):
        return taxon + label[len(ab):]
    # a different binomial/abbreviation inside the label (`strain Bacillus foo X`, `P. vaginalis X`): leave the
    # label unchanged rather than produce a double name — the assigned_taxon column still records the inference
    if re.search(BINOMIAL, label) or re.search(ABBREV, label):
        return label
    return f"{taxon} {label}"


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
    if genus_hit:
        return genus_hit, "preceding_binomial_genus"
    m = GENUS_SP.search(context)
    if m and m.group(1) not in NON_GENUS and (m.group(1) in genera or not genera):
        return f"{m.group(1)} sp.", "preceding_genus_sp"
    return "", ""


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
        if (len(novel) == 1
                and not re.search(r"\b(?:sp|subsp|comb|nom)\. nov\.", before)
                and not re.search(BINOMIAL, before) and not re.search(ABBREV, before)
                and not re.search(r"type strain of", before, re.I)
                and not re.search(BINOMIAL, label) and not re.search(ABBREV, label)):
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
                cand = validate_binomial(norm_taxon(m.group(1)), full, abbrev)
                if not cand:
                    continue
                # ensure the sp. nov. binomial and the marked strain are the nearest pair (no other designation between)
                between = snippet[m.start(): m.end()]
                if len(DESIGNATION.findall(between.replace(f"[[{label}]]", ""))) > 1:
                    continue
                return cand
        m = TYPE_STRAIN_PAREN.search(snippet)
        if m and f"[[{label}]]" in snippet[m.start():m.end() + len(label) + 4]:
            cand = validate_binomial(norm_taxon(m.group(1)), full, abbrev)
            if cand:
                return cand
    return ""


DESIGNATION = re.compile(r"(?<![\w\-])[A-Za-z]{0,6}[\-_\s]?\d[\w\-\.]*T(?![\w\-])")


def validate_binomial(cand: str, full: set[str], abbrev: dict[str, str]) -> str:
    """Reject prose ('The major'), apply stoplists, and prefer the document's own spelling of the
    taxon (papers occasionally misspell their own species in one sentence)."""
    genus, species = cand.split(" ")[0], cand.split(" ")[1]
    if genus in NON_GENUS or species in NON_SPECIES:
        return ""
    hit = expand(cand, full, abbrev)
    if hit:
        return hit
    if full:
        # fuzzy: same genus and species epithets within edit distance 2 (typo tolerance)
        near = sorted((_lev(t.split(" ")[1], species), t) for t in full if t.split(" ")[0] == genus)
        if near and near[0][0] <= 2:
            return near[0][1]
        # genus known in this document -> accept the candidate as spelled
        if genus in {t.split(" ")[0] for t in full}:
            return cand
        return ""
    return cand  # document has no usable taxa; trust the pattern


def _lev(a: str, b: str) -> int:
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def rule_label_binomial(label: str, full: set[str], abbrev: dict[str, str]) -> str:
    """The label itself opens with its binomial (`Gordonia otitidis NBRC 100426T`,
    `M. smithii DSM 861`): prefer the document's spelling of that taxon, else accept as spelled."""
    m = LABEL_BINOMIAL.match(norm_taxon(label))
    if not m:
        return ""
    cand, rest = norm_taxon(m.group(1)), m.group(2)
    genus, species = cand.split(" ")[0], cand.split(" ")[1]
    if genus in NON_GENUS or species in NON_SPECIES:
        return ""
    # a second binomial in the remainder means the label names several organisms — skip
    if re.search(BINOMIAL, rest) or re.search(ABBREV, rest):
        return ""
    hit = expand(cand, full, abbrev)
    if hit:
        return hit
    # without the document's backing, reject placeholder species words and family/order names
    if species in NON_SPECIES_IN_LABEL or genus.endswith(("aceae", "ales")):
        return ""
    if re.fullmatch(ABBREV, cand):
        return cand  # unexpandable abbreviation: keep as spelled
    return validate_binomial(cand, full, abbrev) or cand


def rule_equivalence(context: str, resolved: dict[str, str]) -> tuple[str, str]:
    """Mention is `X (=[[this]]…)` or `…=[[this]]` — find the primary designation X and its resolved name."""
    for m in EQUIV.finditer(context):
        toks = m.group(1).strip().split(" ")
        for cand in (" ".join(toks[-2:]), toks[-1]):
            cand = cand.strip("(),;:=")
            if cand in resolved and resolved[cand]:
                return resolved[cand], cand
    return "", ""


def add_full_names(df: pd.DataFrame) -> pd.DataFrame:
    need = {"doc", "field", "label", "context"}
    missing = need - set(df.columns)
    if missing:
        raise SystemExit(f"error: table lacks required columns {sorted(missing)}")
    df = df.copy()
    df["full_scientific_name"] = ""
    df["name_source"] = ""
    df["assigned_taxon"] = ""

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
        if not taxon:  # needs no context: the label itself carries the binomial
            taxon = rule_label_binomial(label, full, abbrev)
            src = "label_binomial" if taxon else ""
        if taxon:
            df.at[i, "assigned_taxon"], df.at[i, "name_source"] = taxon, src
            df.at[i, "full_scientific_name"] = compose(taxon, label)
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
                df.at[i, "assigned_taxon"], df.at[i, "name_source"] = taxon, f"equivalence:{primary}"
                df.at[i, "full_scientific_name"] = compose(taxon, label)
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
    try:
        df = pd.read_csv(args.table, sep=sep, dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError:
        print(f"error: {args.table} is empty", file=sys.stderr)
        return 1
    out = add_full_names(df)

    st = out[out["field"] == "strains"]
    n = len(st)
    print(f"strain rows: {n:,}", file=sys.stderr)
    for src, cnt in st["name_source"].str.split(":").str[0].replace("", "(unresolved)").value_counts().items():
        print(f"  {src:20s} {cnt:6,} ({cnt / n * 100:.1f}%)", file=sys.stderr)

    # QC: one taxon -> several distinct T designations in a doc, not '='-linked anywhere
    res = st[st["full_scientific_name"] != ""]
    tstr = res[res["label"].str.endswith("T")]
    for (doc, taxon), grp in tstr.groupby(["doc", "assigned_taxon"]):
        labs = sorted(set(grp["label"]))
        if len(labs) < 2:
            continue
        ctx = " ".join(df.loc[df["doc"] == doc, "context"])
        linked = all(re.search(rf"{re.escape(l)}\s*\(?=|=\s*\(?\[?\[?{re.escape(l)}", ctx) for l in labs)
        if not linked:
            print(f"  QC: doc {doc}: {taxon} assigned to {len(labs)} T-strains not '='-linked: {', '.join(labs)}", file=sys.stderr)

    if args.strains_only:
        out = st
    dest = args.out or args.table.with_suffix("").with_suffix(".full_names.tsv")
    out.to_csv(dest, sep="\t", index=False)
    print(f"wrote {dest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
