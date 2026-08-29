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
        dups = df.duplicated(subset=key_cols, keep=False)
        P(f"\n- Rows sharing the same mention key {key_cols}: **{dups.sum():,}**\n")
        if dups.any():
            rel_cols = [c for c in df.columns if c.startswith("relationship_") or c.startswith("chemical_relationship")]
            differing = [c for c in df.columns if df[dups].groupby(key_cols)[c].nunique().gt(1).any()]
            if differing and set(differing) <= set(rel_cols) | {R["context"]}:
                P(f"  - These differ only in relationship columns ({', '.join(differing)}): one row per (mention, relationship) — expected, not a defect.\n")
            else:
                flags.append(f"{dups.sum():,} rows share a mention key but differ in non-relationship columns: {differing}")
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
                P(f"\n### {b} — {len(sub):,} unique labels (top {min(len(sub), 10)})\n")
                P(md_table(sub.drop(columns=["bucket"]), 10))
            else:
                P(f"\n### {b} — {len(sub):,} unique labels (top {min(len(sub), args.top)})\n")
                P(md_table(sub.drop(columns=["bucket"]), args.top))
        if args.catalog_out:
            cat.to_csv(args.catalog_out, sep="\t", index=False)
            P(f"\nFull catalog written to `{args.catalog_out}`\n")

    # ---------------- FLAGS ----------------
    P("\n\n## 5. Flags\n")
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
