#!/usr/bin/env python3
"""Profile an OntoGPT extraction + KG-grounding table (TSV/CSV).

Produces a Markdown report covering content (what was extracted), structure
(columns, types, key integrity) and QC (grounding coverage, duplicates,
suspicious values, ungrounded-term catalog).

Usage:
    python profile_table.py TABLE.tsv [--out REPORT.md] [--top N]

Depends on pandas and tabulate (for Markdown tables); see requirements.txt. Column names are looked up by role so the script
tolerates minor schema drift (see ROLE_CANDIDATES).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

# role -> candidate column names, first match wins
ROLE_CANDIDATES = {
    "doc": ["doc", "document", "doc_id"],
    "pmid": ["pmid", "PMID"],
    "field": ["field", "slot"],
    "kind": ["kind", "entity_type"],
    "entity_id": ["entity_id", "id"],
    "label": ["label", "entity_label"],
    "spans": ["original_spans", "spans"],
    "context": ["context"],
    "grounded_id": ["grounded_id"],
    "grounded_ids": ["grounded_ids"],
    "kg_name": ["kg_name"],
    "kg_category": ["kg_category"],
    "match_type": ["match_type"],
    "kg_edge_count": ["kg_edge_count"],
    "rel_id": ["chemical_relationship_id"],
    "rel_label": ["chemical_relationship_label"],
    "rel_match": ["chemical_relationship_match_type"],
    "level_type": ["chemical_level_type"],
}

# Ungrounded-label heuristics used to bucket the catalog
COLLECTION_RE = re.compile(r"^(DSM|DSMZ|ATCC|JCM|KCTC|CGMCC|CCTCC|NBRC|LMG|CECT|NRRL|NCIMB|NCTC|KACC|BCRC|VKM|CIP|CCUG)\b")
MEDIUM_RE = re.compile(
    r"\b(agar|broth|medium|media|blood|serum|extract|peptone|tryptone|trypticase|casein|milk|juice|"
    r"TSB|TSA|BHI|LB|R2A|ISP\s?\d|MRS|Reasoner)\b", re.I)
ENZYME_RE = re.compile(r"\b\w{3,}(idase|osidase|ase)\b|\b(activity|test|assay)\b", re.I)
UNSPEC_RE = re.compile(r"^\W*(unspecified|not specified|not stated|unknown|none|n/?a)\W*$", re.I)
GENERIC_RE = re.compile(
    r"\b(sources?|compounds?|substrates?|sugars?|various|several|some|other|many|multiple|range of|"
    r"a variety|different|elements?|ions|metals|hydrocarbons|organic matter|and oligo|fluid|mucus)\b", re.I)
VALUE_RE = re.compile(r"^\s*[\d\.\-–,]+\s*(?:%|mM|M\b|g/l|mg/l|\(w/v\)|°C|℃|\s\S)", re.I)
# phenotype/trait-like phrases that landed in the chemical slot -> METPO candidates
TRAIT_RE = re.compile(
    r"\b(\w{3,}ase|H2/CO2|autotroph\w*|heterotroph\w*|motil\w+|spore\w*|gram[- ]\w+|aerob\w*|anaerob\w*|"
    r"halophil\w*|thermophil\w*|psychrophil\w*|alkaliphil\w*|acidophil\w*|indole(?![- ]?\d|[- ]acetic)|nitrate reduction|"
    r"fermentation|hydrolysis|solubilization|oxidation|reduction)\b", re.I)
EXPECTED_FIELDS = {"strains", "study_taxa", "chemical_utilization_object", "temperature_observation", "pH_observation"}
FIELD_CUES = {  # field -> regex over concatenated context that suggests the slot should be non-empty
    "temperature_observation": re.compile(r"°C|℃|\btemperature\b", re.I),
    "pH_observation": re.compile(r"\bpH\b", re.I),
    "chemical_utilization_object": re.compile(r"\bNaCl\b|\bcarbon source|\bglucose\b|\bhydroly|\butiliz|\bferment", re.I),
}


def load_full_scientific_name():
    """Import src/process_terms/full_scientific_name.py from the repo this skill lives in, if present."""
    import importlib.util
    here = Path(__file__).resolve()
    for root in here.parents:
        cand = root / "src" / "process_terms" / "full_scientific_name.py"
        if cand.exists():
            spec = importlib.util.spec_from_file_location("full_scientific_name", cand)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    return None


def has(series: pd.Series, rx: re.Pattern) -> pd.Series:
    """Boolean mask: regex search on each value (avoids pandas capture-group warning)."""
    return series.apply(lambda x: bool(rx.search(x)))


# A stereo/configuration descriptor followed by a hyphen/en-dash. Handles `D-`, `(R)-`, `(2R,3S)-`,
# `L(+)-`, `(+)-`, `(−)-`, `cis-`, `(E)-`, `α-`, `DL-`, `meso-`.
STEREO_RE = re.compile(
    r"(?:^|[\s,/\-–])"
    r"(?:"
    r"(?:\(?(DL|LL|DD|dl|ll|dd|[DLdl],[DLdl]|[RS],[RS]|[DLdl]|RS|[RS]|meso|cis|trans|alpha|beta|α|β|[EZ])\)?"
    r"|\((\d+[RSEZrsez](?:,\d+[RSEZrsez])*)\))"
    r"(?:\(([+\-−±])\))?"
    r"|\(([+\-−±])\)"
    r")"
    r"(?=[\-–][A-Za-zα-ω(\[])"
)
STEREO_FAMILY = {"D": "DL", "L": "DL", "DL": "DL", "LL": "DL", "DD": "DL", "meso": "DL",
                 "R": "RS", "S": "RS", "RS": "RS", "+": "sign", "-": "sign", "±": "sign",
                 "cis": "geo", "trans": "geo", "E": "geo", "Z": "geo",
                 "alpha": "alpha/beta", "beta": "alpha/beta"}


def stereo_prefixes(x: str) -> dict[str, list[str]]:
    """Stereo/configuration prefixes in a chemical name grouped by nomenclature family, in order of
    appearance, normalised (d→D, α→alpha, − → -). D/L and R/S are different systems
    (D-lactate == (R)-lactate), so a mismatch is only meaningful within one family.
    Locant-qualified descriptors are kept whole: (2R,3S) in the RS family, (3E,5Z) in geo.
    Bare descriptors must be followed by a letter (`D-glucose`, not `S-27T` or `l-1`)."""
    norm = {"d": "D", "l": "L", "dl": "DL", "ll": "LL", "dd": "DD", "α": "alpha", "β": "beta", "−": "-"}
    out: dict[str, list[str]] = {}
    for simple, locant, sign, sign2 in STEREO_RE.findall(x):
        sign = sign or sign2
        if simple:
            if "," in simple:  # d,l- / R,S- racemate spellings
                simple = simple.replace(",", "").upper()
            m = norm.get(simple, simple)
            out.setdefault(STEREO_FAMILY[m], []).append(m)
        if locant:
            loc = locant.upper()
            fam = "geo" if re.fullmatch(r"(?:\d+[EZ],?)+", loc) else "RS"
            out.setdefault(fam, []).append(loc)
        if sign:
            out.setdefault("sign", []).append(norm.get(sign, sign))
    return out


def stereo_conflict(a: str, b: str) -> bool:
    """True when a and b carry different prefixes (order-sensitive) of the same stereo family."""
    pa, pb = stereo_prefixes(a), stereo_prefixes(b)
    return any(fam in pb and pa[fam] != pb[fam] for fam in pa)


def tokens(x: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", x.lower()) if len(t) > 1}



def resolve(df: pd.DataFrame) -> dict[str, str | None]:
    cols = {c.lower(): c for c in df.columns}
    out = {}
    for role, cands in ROLE_CANDIDATES.items():
        out[role] = next((cols[c.lower()] for c in cands if c.lower() in cols), None)
    return out


def bucket_ungrounded(label: str, kind: str) -> str:
    if UNSPEC_RE.search(label):
        return "unspecified/placeholder"
    if kind == "strain":
        return "strain (kind=strain)"
    if COLLECTION_RE.match(label.strip()):
        return "culture-collection accession"
    if MEDIUM_RE.search(label):
        return "growth medium / component"
    if ENZYME_RE.search(label):
        return "enzyme / assay"
    if kind in ("taxon_candidate",):
        return "taxon (not in NCBITaxon)"
    if kind in ("chemical",):
        return "chemical (not in CHEBI)"
    return "other"


def md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if max_rows is not None:
        df = df.head(max_rows)
    if df.empty:
        return "_(none)_\n"
    return df.to_markdown(index=False) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("table", type=Path)
    ap.add_argument("--out", type=Path, help="write Markdown report here (default: stdout)")
    ap.add_argument("--top", type=int, default=30, help="rows to show in top-N tables")
    ap.add_argument("--catalog-out", type=Path, help="also write the ungrounded-term catalog as TSV")
    args = ap.parse_args()

    try:
        with open(args.table, encoding="utf-8") as fh:
            header = fh.readline()
        sep = "\t" if header.count("\t") >= header.count(",") else ","
        df = pd.read_csv(args.table, sep=sep, dtype=str, keep_default_na=False)
    except (pd.errors.EmptyDataError, FileNotFoundError) as e:
        print(f"error: cannot read {args.table}: {e}", file=sys.stderr)
        return 1
    R = resolve(df)
    missing = [r for r, c in R.items() if c is None]

    L: list[str] = []
    P = L.append
    P(f"# Extraction table review: `{args.table.name}`\n")
    P(f"- Size on disk: {args.table.stat().st_size/1e6:.1f} MB\n- Rows: {len(df):,}\n- Columns: {len(df.columns)}\n")

    # ---------------- STRUCTURE ----------------
    P("\n## 1. Structure\n")
    P("### Columns\n")
    struct = pd.DataFrame({
        "column": df.columns,
        "non_empty": [(df[c] != "").sum() for c in df.columns],
        "pct_non_empty": [f"{(df[c] != '').mean()*100:.1f}%" for c in df.columns],
        "n_unique": [df[c].nunique() for c in df.columns],
        "example": [next((v for v in df[c] if v), "")[:60] for c in df.columns],
    })
    P(md_table(struct))
    if missing:
        P(f"\n**Roles not found in this table:** {', '.join(missing)} (some checks below are skipped)\n")

    if R["doc"]:
        P(f"\n- Documents: {df[R['doc']].nunique():,}")
    if R["pmid"]:
        P(f"\n- PMIDs: {df[R['pmid']].nunique():,}")
        bad_pmid = df[~df[R["pmid"]].str.fullmatch(r"\d+")]
        if len(bad_pmid):
            P(f"\n- ⚠️ Non-numeric PMIDs: {len(bad_pmid):,}")
    if R["doc"] and R["pmid"]:
        multi = df.groupby(R["doc"])[R["pmid"]].nunique()
        if (multi > 1).any():
            P(f"\n- ⚠️ Docs mapping to >1 PMID: {(multi > 1).sum()}")

    # ---------------- CONTENT ----------------
    P("\n\n## 2. Content\n")
    for role in ("field", "kind", "match_type", "kg_category", "level_type", "rel_match"):
        c = R[role]
        if c:
            vc = df[c].replace("", "(empty)").value_counts()
            P(f"\n### `{c}`\n")
            P(md_table(vc.rename_axis(c).reset_index(name="rows"), args.top))
    if R["field"] and R["kind"]:
        P("\n### field × kind\n")
        P(md_table(pd.crosstab(df[R["field"]], df[R["kind"]]).reset_index()))
    if R["entity_id"]:
        prefixes = df[R["entity_id"]].str.split(":").str[0].value_counts()
        P("\n### entity_id prefixes\n")
        P(md_table(prefixes.rename_axis("prefix").reset_index(name="rows")))
        P(f"\n- Unique entity IDs: {df[R['entity_id']].nunique():,}\n")
    if R["grounded_id"]:
        gp = df.loc[df[R["grounded_id"]] != "", R["grounded_id"]].str.split(":").str[0].value_counts()
        P("\n### grounded_id prefixes\n")
        P(md_table(gp.rename_axis("prefix").reset_index(name="rows")))
    if R["label"] and R["grounded_id"]:
        g = df[df[R["grounded_id"]] != ""]
        cols = [R["label"], R["grounded_id"]] + [c for c in (R["kg_category"], R["match_type"]) if c]
        P(f"\n### Top grounded terms (top {args.top})\n")
        P(md_table(g[cols].value_counts().reset_index(name="rows"), args.top))

    # ---------------- QC ----------------
    P("\n\n## 3. QC (all rows unless stated)\n")
    flags: list[str] = []
    if R["grounded_id"]:
        grounded = df[R["grounded_id"]] != ""
        P(f"\n- Grounding coverage: **{grounded.sum():,} / {len(df):,} ({grounded.mean()*100:.1f}%)**\n")
        if R["field"]:
            P("\n### Grounding by field\n")
            ct = pd.crosstab(df[R["field"]], grounded.map({True: "grounded", False: "ungrounded"}))
            for c in ("grounded", "ungrounded"):
                if c not in ct:
                    ct[c] = 0
            ct["pct_grounded"] = (ct["grounded"] / (ct["grounded"] + ct["ungrounded"]) * 100).round(1)
            P(md_table(ct.reset_index()))
            low = ct[ct["pct_grounded"] < 50]
            for f, r in low.iterrows():
                flags.append(f"field `{f}` is only {r['pct_grounded']}% grounded ({int(r['ungrounded']):,} ungrounded rows)")
        # one label -> many grounded ids?
        if R["label"]:
            amb = df[grounded].groupby(R["label"])[R["grounded_id"]].nunique()
            amb = amb[amb > 1].sort_values(ascending=False)
            P(f"\n### Labels grounded to >1 ID ({len(amb):,})\n")
            if len(amb):
                ex = df[grounded & df[R["label"]].isin(amb.index[: args.top])].groupby(R["label"])[R["grounded_id"]].agg(lambda s: ", ".join(sorted(set(s))[:5]))
                P(md_table(amb.head(args.top).rename("n_ids").reset_index().merge(ex.rename("ids").reset_index(), on=R["label"])))
                flags.append(f"{len(amb):,} labels ground to more than one ID (check for inconsistent grounding)")
            else:
                P("_(none)_\n")
        # grounded_id vs grounded_ids consistency
        if R["grounded_ids"]:
            first = df[R["grounded_ids"]].str.split("|").str[0]
            mism = df[grounded & (first != df[R["grounded_id"]])]
            if len(mism):
                flags.append(f"{len(mism):,} rows where `grounded_id` != first of `grounded_ids`")
        # kg_name vs label sanity for name matches
        if R["kg_name"] and R["label"] and R["match_type"]:
            nm = df[(df[R["match_type"]] == "name") & (df[R["kg_name"]].str.lower() != df[R["label"]].str.lower())]
            if len(nm):
                flags.append(f"{len(nm):,} rows with match_type=name but kg_name != label (case-insensitive)")
                P(f"\n### match_type=name but kg_name ≠ label (showing {min(len(nm), args.top)} of {len(nm):,})\n")
                P(md_table(nm[[R["label"], R["kg_name"], R["grounded_id"]]].drop_duplicates(), args.top))
        if R["kg_edge_count"]:
            ec = pd.to_numeric(df[R["kg_edge_count"]], errors="coerce")
            orphan = grounded & (ec.fillna(0) == 0)
            if orphan.any():
                if R["match_type"]:
                    by, grp = R["match_type"], df[R["match_type"]]
                else:
                    by, grp = "grounded_id prefix", df[R["grounded_id"]].str.split(":").str[0]
                tot = grp[grounded].value_counts()
                zero = grp[orphan].value_counts()
                for k, n in zero.items():
                    if n == tot[k]:
                        flags.append(f"kg_edge_count not populated for all {n:,} rows with {by}={k} (edge stats missing for this grounding path, not necessarily orphan nodes)")
                    else:
                        flags.append(f"{n:,}/{tot[k]:,} grounded rows with {by}={k} have kg_edge_count=0")

    # duplicates
    key_cols = [c for c in (R["doc"], R["field"], R["entity_id"], R["spans"]) if c]
    if key_cols:
        # Span-less rows cannot be keyed by mention: exclude them so two distinct un-located
        # mentions of one entity in one doc are not mistaken for relationship duplicates.
        located = (df[R["spans"]] != "") if R["spans"] else pd.Series([True] * len(df))
        dups = df.duplicated(subset=key_cols, keep=False) & located
        P(f"\n- Located rows sharing the same mention key {key_cols}: **{dups.sum():,}** ({(~located).sum():,} span-less rows excluded from this check)\n")
        if dups.any():
            rel_cols = [c for c in df.columns if c.startswith("relationship_") or c.startswith("chemical_relationship")]
            grp = df[dups].groupby(key_cols)
            differing = [c for c in df.columns if c not in key_cols and grp[c].nunique().gt(1).any()]
            non_rel = [c for c in differing if c not in rel_cols and c != R["context"]]
            if non_rel:
                flags.append(f"{dups.sum():,} rows share a mention key but differ in non-relationship columns: {non_rel}")
            elif differing:
                P(f"  - These differ only in relationship columns ({', '.join(c for c in differing if c != R['context'])}): one row per (mention, relationship) — expected, not a defect.\n")
            else:
                P("  - Fully identical rows (see count below).\n")
            # context should be a function of the span; if it differs while the relationship columns
            # are identical, the same mention was emitted twice with different snippets
            if R["context"] and R["context"] in differing:
                same_rel = df[dups].duplicated(subset=key_cols + rel_cols, keep=False)
                ctx_var = df[dups][same_rel].groupby(key_cols + rel_cols)[R["context"]].nunique().gt(1).sum()
                if ctx_var:
                    flags.append(f"{ctx_var:,} mention keys repeat with identical relationship columns but different context (true duplicate emission)")
                    P(f"  - ⚠️ {ctx_var:,} mention keys repeat with identical relationship columns but different `context`.\n")
        if R["spans"] and R["doc"] and R["entity_id"]:
            sl = df[~located]
            sl_key = [R["doc"], R["entity_id"]] + ([R["field"]] if R["field"] else [])
            sl_dup = sl.duplicated(subset=sl_key, keep=False)
            if sl_dup.any():
                rel_cols = [c for c in df.columns if c.startswith("relationship_") or c.startswith("chemical_relationship")]
                sl_diff = [c for c in df.columns if c not in sl_key and sl[sl_dup].groupby(sl_key)[c].nunique().gt(1).any()]
                sl_non_rel = [c for c in sl_diff if c not in rel_cols and c != R["context"]]
                if sl_non_rel:
                    P(f"  - Span-less rows repeating the same (doc, field, entity) and differing in non-relationship columns {sl_non_rel}: **{int(sl_dup.sum()):,}** — cannot tell distinct mentions from duplicates without spans.\n")
                    flags.append(f"{int(sl_dup.sum()):,} span-less rows repeat a (doc, field, entity) with differing {sl_non_rel}")
                else:
                    P(f"  - Span-less rows repeating the same (doc, field, entity): **{int(sl_dup.sum()):,}**, differing only in relationship columns — expected expansion.\n")
    full_dups = df.duplicated(keep=False).sum()
    P(f"- Fully identical rows: **{full_dups:,}**\n")

    # empties / suspicious values
    if R["label"]:
        lab = df[R["label"]]
        empty_lab = (lab.str.strip() == "").sum()
        if empty_lab:
            flags.append(f"{empty_lab:,} rows with empty label")
        unspec = lab.apply(lambda x: bool(UNSPEC_RE.search(x)))
        if unspec.any():
            flags.append(f"{unspec.sum():,} rows (all rows, grounded or not) with placeholder labels (unspecified/unknown/NA)")
        long_lab = lab.str.len() > 80
        if long_lab.any():
            flags.append(f"{long_lab.sum():,} labels longer than 80 chars (likely phrases, not terms)")
            P(f"\n### Very long labels (>80 chars, showing {min(long_lab.sum(), args.top)})\n")
            P(md_table(lab[long_lab].drop_duplicates().to_frame(), args.top))
    if R["spans"]:
        bad_span = ~df[R["spans"]].str.fullmatch(r"(\d+:\d+)(;\s*\d+:\d+)*|")
        if bad_span.any():
            flags.append(f"{bad_span.sum():,} rows with malformed original_spans")
    if R["context"] and R["label"]:
        ctx = df[R["context"]]
        no_mark = (ctx != "") & ~ctx.str.contains(r"\[\[.+?\]\]", regex=True)
        if no_mark.any():
            flags.append(f"{no_mark.sum():,} rows whose context lacks a [[...]] mention marker")

    # ---------------- UNGROUNDED CATALOG ----------------
    if R["grounded_id"] and R["label"]:
        ung = df[df[R["grounded_id"]] == ""].copy()
        kind_col = R["kind"] or R["field"]
        ung["bucket"] = [bucket_ungrounded(l, k) for l, k in zip(ung[R["label"]], ung[kind_col] if kind_col else [""] * len(ung))]
        P("\n\n## 4. Ungrounded-term catalog (rows with empty grounded_id only)\n")
        P(f"\n- Ungrounded rows: {len(ung):,}; unique labels: {ung[R['label']].nunique():,}\n")
        P("\n### By bucket\n")
        P(md_table(ung["bucket"].value_counts().rename_axis("bucket").reset_index(name="rows")))
        agg = {"rows": (R["label"], "size")}
        if R["doc"]:
            agg["n_docs"] = (R["doc"], "nunique")
        if R["field"]:
            agg["fields"] = (R["field"], lambda s: ",".join(sorted(set(s))))
        if R["context"]:
            agg["example_context"] = (R["context"], lambda s: next((x for x in s if x), "")[:120])
        cat = ung.groupby([R["label"], "bucket"]).agg(**agg).reset_index().sort_values("rows", ascending=False)
        for b in cat["bucket"].unique():
            sub = cat[cat["bucket"] == b]
            if b == "strain (kind=strain)":
                labs = sub[R["label"]].str.strip()
                n = len(labs)
                t_suffix = labs.str.fullmatch(r".*\d\s?[Tᵀ]")
                collection = has(labs, COLLECTION_RE)
                binomial = labs.str.match(r"[A-Z][a-z]+ (?:[a-z]{2,}|sp\.|aff\. \S+|cf\. \S+) \S")
                phrase = has(labs, re.compile(r"\b(?:strain|isolate|isolates|clone)\b|_", re.I)) & ~binomial
                bare = labs.str.fullmatch(r"\S*\d\S*") & ~collection & ~binomial & ~phrase
                prefixed = labs.str.fullmatch(r"[A-Z][A-Za-z]{1,7}(?:-[A-Z]+)? \S*\d\S*") & ~collection & ~binomial & ~phrase
                other = ~(collection | binomial | phrase | bare | prefixed)
                def share(mask: pd.Series) -> str:
                    return f"{int(mask.sum()):,} ({mask.mean()*100:.1f}%)"
                part = pd.DataFrame([
                    {"class (mutually exclusive)": "culture-collection accession (DSM/ATCC/JCM/KCTC/CGMCC/…)", "labels": share(collection)},
                    {"class (mutually exclusive)": "Genus species / sp. / aff. + designation", "labels": share(binomial & ~collection)},
                    {"class (mutually exclusive)": "phrase (`strain …`, `13 isolates of …`, `strain_of`)", "labels": share(phrase & ~collection)},
                    {"class (mutually exclusive)": "bare code, no whitespace (`LC2-13A`, `zg-579T`)", "labels": share(bare)},
                    {"class (mutually exclusive)": "lab/collection prefix + code, prefix not in COLLECTION_RE (`YIM 65594T`, `MCCC 1K00261T`)", "labels": share(prefixed)},
                    {"class (mutually exclusive)": "other (with whitespace, no recognised pattern)", "labels": share(other)},
                ])
                cross = pd.DataFrame([
                    {"cross-cutting property": "type-strain suffix `T`/`ᵀ`", "labels": share(t_suffix)},
                    {"cross-cutting property": "contains whitespace", "labels": share(labs.str.contains(r"\s"))},
                    {"cross-cutting property": "seen in >1 document", "labels": share(sub["n_docs"] > 1) if "n_docs" in sub else "n/a"},
                ])
                P(f"\n### {b} — {n:,} unique labels\n")
                P("\n_Strain designations are per-paper identifiers; a ranked list is not informative. Composition instead. Base = unique labels in this bucket; the first table is a partition (sums to 100%), the second lists overlapping properties._\n")
                P(md_table(part))
                P("")
                P(md_table(cross))
                if other.any():
                    P(f"\n_Examples of 'other':_ {', '.join(f'`{x}`' for x in labs[other].head(8))}\n")
                if "n_docs" in sub:
                    multi = sub[sub["n_docs"] > 1].drop(columns=["bucket"])
                    P(f"\n_Strain labels seen in >1 document (top {min(len(multi), 10)}) — the only ones worth cataloguing:_\n")
                    P(md_table(multi, 10))
            else:
                P(f"\n### {b} — {len(sub):,} unique labels (top {min(len(sub), args.top)})\n")
                P(md_table(sub.drop(columns=["bucket"]), args.top))
        if args.catalog_out:
            cat.to_csv(args.catalog_out, sep="\t", index=False)
            P(f"\nFull catalog written to `{args.catalog_out}`\n")

    # ---------------- EXTRACTION QUALITY ----------------
    P("\n\n## 5. Extraction quality (all rows unless stated)\n")
    lab = df[R["label"]] if R["label"] else pd.Series([""] * len(df))
    kind_col = R["kind"] or R["field"]
    chem_mask = (df[kind_col] == "chemical") if kind_col else pd.Series([True] * len(df))
    grounded = (df[R["grounded_id"]] != "") if R["grounded_id"] else pd.Series([False] * len(df))

    # --- 6a false-positive candidates ---
    P("\n### 5a. False-positive candidates (grounded, but suspicious)\n")
    P("\n_Precision proxies. Each table is a review queue, not a verdict._\n")
    if R["grounded_id"] and R["match_type"] and R["kg_name"] and R["label"]:
        syn = df[grounded & (df[R["match_type"]] == "synonym")]
        short = syn[syn[R["label"]].str.len() <= 2][[R["label"], R["kg_name"], R["grounded_id"]]].drop_duplicates()
        P(f"\n**Synonym matches on 1–2-character labels** ({len(short)} unique) — element symbols vs one-letter amino-acid codes collide here:\n")
        P(md_table(short))
        if len(short):
            flags.append(f"{len(short)} distinct 1–2-char labels grounded by synonym (check for symbol/amino-acid collisions, e.g. K→lysine)")
        # zero token overlap between label and kg_name (lexical), excluding tiny formula labels
        lex = df[grounded & df[R["match_type"]].isin(["name", "synonym"]) & (df[R["label"]].str.len() > 3)]
        ov = [len(tokens(l) & tokens(k)) == 0 for l, k in zip(lex[R["label"]], lex[R["kg_name"]])]
        nov = lex[ov][[R["label"], R["kg_name"], R["grounded_id"], R["match_type"]]].value_counts().reset_index(name="rows")
        P(f"\n**No word overlap between label and kg_name** ({len(nov)} unique; top {args.top}) — formulas and true synonyms are fine, look for meaning changes:\n")
        P(md_table(nov, args.top))
        # stereo / configuration prefix differs while the stem is shared (d-glucose -> L-glucose, l-arabinose -> D-arabinose)
        lex2 = df[grounded & df[R["match_type"]].isin(["name", "synonym"])]
        st = []
        for l, k in zip(lex2[R["label"]], lex2[R["kg_name"]]):
            st.append(bool(tokens(l) & tokens(k)) and stereo_conflict(l, k))
        stdf = lex2[st][[R["label"], R["kg_name"], R["grounded_id"], R["match_type"]]].value_counts().reset_index(name="rows")
        P(f"\n**Stereo/configuration prefix differs between label and kg_name** ({len(stdf)} unique) — D/L, R/S (incl. `(2R,3S)`), (+)/(−), cis/trans/E/Z, α/β (anomeric *or* positional) flips *within one nomenclature system* change the compound (`l-arabinose`→D-arabinose); D↔R/S are different systems and are not compared (D-lactate ≡ (R)-lactate):\n")
        P(md_table(stdf, args.top))
        if len(stdf):
            flags.append(f"{len(stdf)} label/kg_name pairs differ in stereo prefix (D/L, R/S, α/β…) — likely wrong enantiomer/isomer")
        one = [bool(tokens(l) & tokens(k)) and bool(stereo_prefixes(l)) != bool(stereo_prefixes(k))
               for l, k in zip(lex2[R["label"]], lex2[R["kg_name"]])]
        onedf = lex2[one][[R["label"], R["kg_name"], R["grounded_id"], R["match_type"]]].copy()
        onedf["direction"] = ["label generic → kg specific" if not stereo_prefixes(l) else "label specific → kg generic (descriptor dropped)"
                              for l in onedf[R["label"]]]
        onedf = onedf.value_counts().reset_index(name="rows").sort_values(["direction", "rows"], ascending=[True, False])
        P(f"\n**Stereo prefix on one side only** ({len(onedf)} unique). Generic→specific (`maltose`→D-maltose) is usually acceptable; specific→generic (`d-lactose`→lactose) means the grounding dropped a descriptor the extractor captured — check:\n")
        P(md_table(onedf, args.top))
    if R["kg_category"] and kind_col and R["grounded_id"]:
        exp = {"chemical": "ChemicalEntity|ChemicalSubstance|Molecule|Macromolecule", "taxon_candidate": "OrganismTaxon", "phenotype_observation": "OntologyClass", "strain": "OrganismTaxon|strain"}
        mm = []
        for k, pat in exp.items():
            sub = df[grounded & (df[kind_col] == k) & ~df[R["kg_category"]].str.contains(pat, regex=True)]
            if len(sub):
                mm.append(sub[[kind_col, R["label"], R["grounded_id"], R["kg_category"]]].drop_duplicates())
        mm = pd.concat(mm) if mm else pd.DataFrame(columns=[kind_col, "label", "grounded_id", "kg_category"])
        P(f"\n**kind / kg_category mismatch** ({len(mm)} unique):\n")
        P(md_table(mm, args.top))
        if len(mm):
            flags.append(f"{len(mm)} groundings whose kg_category does not fit the entity kind")
    if R["grounded_id"] and R["label"]:
        val = df[grounded & chem_mask & lab.str.match(VALUE_RE) & lab.str.contains(r"\d")]
        P(f"\n- Chemical rows whose *label* carries a value/concentration (e.g. `12.5% NaCl`): **{len(val):,}** — value belongs in `chemical_level_type`/`context`, not the term label\n")

    # --- 6b noise ---
    P("\n### 5b. Noise: labels that are not real, specific terms\n")
    noise = {
        "generic class phrase": has(lab, GENERIC_RE) & chem_mask,
        "trait / assay phrase in chemical slot": has(lab, TRAIT_RE) & chem_mask & ~has(lab, MEDIUM_RE),
        "growth medium in chemical slot": has(lab, MEDIUM_RE) & chem_mask,
        "value/unit only": lab.str.fullmatch(r"[\d\.\-–,\s%]+(?:\s*(?:%|mM|M|g/l|g/L|w/v|°C|℃))?") & chem_mask,
        "placeholder": lab.apply(lambda x: bool(UNSPEC_RE.search(x))),
        "≥6 words (chemical/taxon slots)": (lab.str.split().str.len() >= 6) & (df[kind_col] != "phenotype_observation" if kind_col else True),
    }
    nrows = []
    for name, m in noise.items():
        m = m.fillna(False)
        ex = ", ".join(lab[m].value_counts().head(6).index.map(lambda x: f"`{x[:40]}`"))
        nrows.append({"noise type": name, "rows": int(m.sum()), "of which grounded": int((m & grounded).sum()), "examples": ex})
    P(md_table(pd.DataFrame(nrows)))
    any_noise = pd.concat([m.fillna(False) for m in noise.values()], axis=1).any(axis=1)
    P(f"\n- Rows matching ≥1 noise pattern: **{any_noise.sum():,} / {len(df):,} ({any_noise.mean()*100:.1f}%)**\n")

    # --- 6c recall / truncation proxies ---
    P("\n### 5c. Incomplete or truncated extraction (recall proxies)\n")
    P("\n_The table has no source text, so these are proxies from `context` snippets; confirm against abstracts._\n")
    if R["doc"] and R["field"]:
        per = df.groupby(R["doc"])[R["field"]].value_counts().unstack(fill_value=0)
        tot = per.sum(axis=1)
        q = tot.quantile([0, .1, .5, .9, 1]).astype(int)
        P(f"\n- Rows per document: min {q[0]}, p10 {q[.1]}, median {q[.5]}, p90 {q[.9]}, max {q[1]}\n")
        thr = max(2, q[.1] // 2)  # half the 10th percentile, floor 2: "far below normal for this run"
        lowdocs = tot[tot <= thr]
        onlytax = [d for d in lowdocs.index if set(per.columns[per.loc[d] > 0]) <= {"strains", "study_taxa"}]
        P(f"- Documents with ≤{thr} rows (half of p10; possible failed/empty extraction): **{len(lowdocs)}**, of which {len(onlytax)} contain only strain/taxon rows: {', '.join(map(str, lowdocs.index[:10]))}\n")
        if len(lowdocs):
            flags.append(f"{len(lowdocs)} docs have ≤{thr} rows ({len(onlytax)} with only strain/taxon rows) — check for failed extraction")
        zero = (per == 0).sum().rename("docs_with_0_rows").reset_index()
        zero["pct_docs"] = (zero["docs_with_0_rows"] / len(per) * 100).round(1)
        P("\n**Documents with no rows per field:**\n")
        P(md_table(zero))
        if R["context"]:
            ctxdoc = df.groupby(R["doc"])[R["context"]].apply(" ".join)
            rows_ = []
            for fld, cue in FIELD_CUES.items():
                if fld in per.columns:
                    miss = [d for d, c in ctxdoc.items() if cue.search(c) and per.loc[d, fld] == 0]
                    percue = {}
                    for d in miss:
                        for alt in cue.pattern.split("|"):
                            if re.search(alt, ctxdoc[d], cue.flags):
                                percue[alt.replace("\\b", "")] = percue.get(alt.replace("\\b", ""), 0) + 1
                    rows_.append({"field": fld, "docs with cue in context but 0 rows": len(miss),
                                  "per cue": ", ".join(f"{k}:{v}" for k, v in sorted(percue.items(), key=lambda kv: -kv[1])),
                                  "examples": ", ".join(map(str, miss[:6]))})
            P("\n**Field cue present in other rows' context, but field empty** (strong truncation signal):\n")
            P(md_table(pd.DataFrame(rows_)))
            for r_ in rows_:
                if r_["docs with cue in context but 0 rows"]:
                    flags.append(f"{r_['docs with cue in context but 0 rows']} docs mention {r_['field']} cues in context but have no {r_['field']} row")
        missing_fields = EXPECTED_FIELDS - set(per.columns)
        if missing_fields:
            flags.append(f"expected fields absent from the whole table: {sorted(missing_fields)}")
    if R["context"]:
        ctx = df[R["context"]]
        def midtoken(c: str) -> tuple[str, str]:
            """Classify the first problematic [[...]] in a context.
            Returns (kind, snippet): kind is 'in-token' when a token continues across the bracket on
            both sides (substring locator hit, e.g. glu[[co]]se), 'offset' when the span starts/ends
            with whitespace/punctuation (span shifted by a char), '' when clean. A trailing 'T'
            (type-strain superscript) after ]] is ignored."""
            for m in re.finditer(r"\[\[(.+?)\]\]", c):
                inner = m.group(1)
                pre, post = c[max(0, m.start() - 1):m.start()], c[m.end():m.end() + 1]
                snippet = c[max(0, m.start() - 25):m.end() + 25]
                if inner[:1].isspace() or inner[-1:].isspace() or (inner[:1] in "([" and pre.isalnum()):
                    return "offset", snippet
                post_alnum = post.isalnum() and not (post == "T" and not c[m.end() + 1:m.end() + 2].isalnum())
                if (pre.isalnum() and inner[:1].isalnum()) or (post_alnum and inner[-1:].isalnum()):
                    return "in-token", snippet
            return "", ""
        cls = ctx.apply(midtoken)
        kindv, snip = cls.str[0], cls.str[1]
        mt, off = kindv == "in-token", kindv == "offset"
        key_cols_m = [c for c in (R["doc"], R["field"], R["entity_id"], R["spans"]) if c]
        n_ment = lambda m: df[m].drop_duplicates(subset=key_cols_m).shape[0] if key_cols_m else int(m.sum())
        P(f"\n- Spans that start/end on whitespace or an opening bracket (span offset error, e.g. `5.0-11.0[[ (optimum pH 7.0]])`): **{n_ment(off):,} mentions / {off.sum():,} rows**\n")
        if off.any():
            flags.append(f"{n_ment(off):,} mentions have a span offset error (leading/trailing whitespace inside [[…]])")
        P(f"\n- Mentions where the token continues across the `[[…]]` boundary (span locator matched a substring inside a longer word, e.g. `glu[[co]]se`; `]]T` type-strain superscripts ignored): **{n_ment(mt):,} mentions / {mt.sum():,} rows**\n")
        if mt.any():
            P(md_table(pd.DataFrame({"label": df.loc[mt, R["label"]] if R["label"] else "", "snippet": snip[mt]}).drop_duplicates(), min(args.top, 15)))
            flags.append(f"{n_ment(mt):,} mentions whose span is a substring inside a longer word (locator defect; check original_spans upstream)")
    if R["spans"]:
        nospan = (df[R["spans"]] == "")
        P(f"- Rows with empty `original_spans` (mention not located in text): **{nospan.sum():,}**\n")
        if nospan.sum():
            flags.append(f"{nospan.sum():,} rows have no original_spans (entity asserted without a located mention)")

    # --- 6d METPO gaps ---
    P("\n### 5d. METPO / vocabulary gaps\n")
    if R["rel_label"] or "chemical_relationship" in df.columns:
        relc = "chemical_relationship" if "chemical_relationship" in df.columns else R["rel_label"]
        rel = df[df[relc] != ""]
        aggs = {"rows": (relc, "size")}
        if R["rel_id"]:
            aggs["metpo_id"] = (R["rel_id"], lambda s: ", ".join(sorted(set(x for x in s if x))[:3]))
        inv = rel.groupby(relc).agg(**aggs)
        inv = inv.sort_values("rows", ascending=False).reset_index()
        P(f"\n**Relationship types used** ({len(inv)}):\n")
        P(md_table(inv, args.top))
        if R["rel_id"]:
            unmapped = inv[inv["metpo_id"] == ""]
            P(f"\n**Relationship types with no METPO id** ({len(unmapped)}) — candidate new METPO relations:\n")
            P(md_table(unmapped, args.top))
            if len(unmapped):
                flags.append(f"{len(unmapped)} relationship types lack a METPO id: {', '.join(unmapped[relc].head(5))}")
    if R["grounded_id"] and R["label"]:
        cand = df[~grounded & chem_mask & has(lab, TRAIT_RE) & ~has(lab, MEDIUM_RE)]
        cand = cand.groupby(R["label"]).agg(rows=(R["label"], "size"), n_docs=(R["doc"], "nunique") if R["doc"] else (R["label"], "size")).sort_values("rows", ascending=False).reset_index()
        P(f"\n**Ungrounded trait-like labels** ({len(cand)} unique; top {args.top}) — phenotypes/enzymes extracted as chemicals; candidates for METPO classes or for schema guidance:\n")
        P(md_table(cand, args.top))
        # chemicals ungrounded but frequent
        freq = df[~grounded & chem_mask & ~has(lab, TRAIT_RE) & ~has(lab, MEDIUM_RE) & ~has(lab, GENERIC_RE)]
        freq = freq.groupby(R["label"]).size().sort_values(ascending=False)
        freq = freq[freq >= 2]
        P(f"\n**Ungrounded specific chemicals seen in ≥2 rows** ({len(freq)}) — CHEBI synonym / lexical-index gaps:\n")
        P(md_table(freq.rename("rows").reset_index(), args.top))

    # --- 6e process / prompt gaps ---
    P("\n### 5e. Process and prompt-instruction gaps\n")
    P("\n_Signals that the extraction agent is not following (or is not given) a consistent instruction. Needs the prompt/schema to confirm._\n")
    ph = lab[lab.apply(lambda x: bool(UNSPEC_RE.search(x)))].value_counts()
    P(f"\n- Placeholder spellings: **{len(ph)}** variants ({', '.join(f'`{v}`' for v in ph.index[:8])}) — prompt should say *omit* rather than emit a placeholder, or fix one spelling\n")
    if R["field"]:
        present = set(df[R["field"]].unique())
        P(f"- Fields present: {sorted(present)}; expected-but-absent: {sorted(EXPECTED_FIELDS - present) or 'none'}; unexpected: {sorted(present - EXPECTED_FIELDS) or 'none'}\n")
    if kind_col and R["label"]:
        multi_kind = df.groupby(R["label"])[kind_col].nunique()
        multi_kind = multi_kind[multi_kind > 1]
        P(f"- Labels assigned to more than one `{kind_col}` across documents: **{len(multi_kind):,}** (inconsistent typing) e.g. {', '.join(f'`{x}`' for x in multi_kind.index[:8])}\n")
        if len(multi_kind):
            flags.append(f"{len(multi_kind):,} labels typed inconsistently across docs (>1 {kind_col})")
    prov = [c for c in df.columns if re.search(r"model|prompt|schema|version|run", c, re.I)]
    P(f"- Provenance columns (model/prompt/schema/version): **{prov or 'none'}** — add them upstream so results can be tied to a run\n")
    if R["label"]:
        distinct = lab.groupby(lab.str.lower()).nunique()
        P(f"- Labels differing only by case: **{(distinct > 1).sum():,}** (no normalization step) e.g. {', '.join(f'`{x}`' for x in distinct[distinct > 1].index[:6])}\n")

    # --- 5f strain name resolution (src/process_terms/full_scientific_name.py) ---
    P("\n### 5f. Strain name resolution (`Genus species STRAIN`)\n")
    fsn = load_full_scientific_name()
    if fsn is None:
        P("\n_`src/process_terms/full_scientific_name.py` not found relative to this script; skipped._\n")
    elif not ({"doc", "field", "label", "context"} <= set(df.columns)):
        P("\n_Requires doc/field/label/context columns; skipped._\n")
    else:
        named = fsn.add_full_names(df)
        stn = named[named["field"] == "strains"]
        n = len(stn)
        if n:
            src = stn["name_source"].str.split(":").str[0].replace("", "(unresolved)").value_counts()
            tbl = src.rename_axis("rule").reset_index(name="rows")
            tbl["pct"] = (tbl["rows"] / n * 100).round(1)
            P(f"\n- Strain rows: {n:,}; resolved: **{(stn['full_scientific_name'] != '').sum():,} ({(stn['full_scientific_name'] != '').mean()*100:.1f}%)**. Rules are applied in priority order (see the script docstring); no document-level fallback.\n")
            P(md_table(tbl))
            ex = stn[stn["full_scientific_name"] != ""].drop_duplicates("name_source").head(8)[["label", "full_scientific_name", "name_source"]]
            P("\n_One example per rule:_\n")
            P(md_table(ex))
            multi = stn[stn["full_scientific_name"] != ""].groupby(["doc", "assigned_taxon"])["label"].nunique()
            multi = multi[multi > 1]
            P(f"\n- (doc, taxon) pairs assigned to >1 distinct strain label: {len(multi):,} — mostly one strain under several collection accessions; the script prints a QC line for those not `=`-linked.\n")
            unres = stn[stn["full_scientific_name"] == ""]
            eq_shape = unres["context"].str.contains(r"=\s*\[\[", regex=True).sum()
            P(f"- Unresolved rows whose mention is an `=`-linked accession (primary designation itself unresolved): {eq_shape:,} of {len(unres):,}\n")
            flags.append(f"strain name resolution: {(stn['full_scientific_name'] != '').mean()*100:.1f}% of strain rows get a Genus species STRAIN name")
        else:
            P("\n_No strain rows._\n")

    # ---------------- FLAGS ----------------
    P("\n\n## 6. Flags\n")
    if flags:
        for f in flags:
            P(f"- ⚠️ {f}")
    else:
        P("- ✅ No automatic flags raised")
    P("")

    report = "\n".join(L)
    if args.out:
        args.out.write_text(report)
        print(f"wrote {args.out}", file=sys.stderr)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
