#!/usr/bin/env python3
"""Assert the smoke export and review report exercise the expected contracts."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


EXPECTED_COLUMNS = [
    "doc", "source_file", "pmid", "field", "kind", "entity_id", "label",
    "original_spans", "context", "relationship_subject_id",
    "relationship_subject_label", "chemical_relationship",
    "chemicals_utilized", "study_taxa", "strains",
    "chemical_relationship_id", "chemical_relationship_label",
    "chemical_relationship_match_type", "grounded_id", "grounded_ids",
    "kg_name", "kg_category", "match_type", "kg_edge_count",
    "kg_edge_evidence",
]

EXPECTED_GROUNDING = {
    "TEST-1T": "kgmicrobe.strain:TEST-1T",
    "Testibacter exampleii": "NCBITaxon:999999",
    "glucose": "CHEBI:17234",
    "NaCl": "CHEBI:26710",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", required=True, type=Path)
    parser.add_argument("--abstract", required=True, type=Path)
    parser.add_argument("--review", required=True, type=Path)
    args = parser.parse_args()

    with args.table.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        assert reader.fieldnames == EXPECTED_COLUMNS, reader.fieldnames
        rows = list(reader)

    assert len(rows) == 4, len(rows)
    assert {row["pmid"] for row in rows} == {"99999999"}
    assert {row["label"] for row in rows} == set(EXPECTED_GROUNDING)
    assert {row["field"] for row in rows} == {
        "strains",
        "study_taxa",
        "chemical_utilization_object",
    }

    abstract = args.abstract.read_text(encoding="utf-8").strip()
    for row in rows:
        assert row["grounded_id"] == EXPECTED_GROUNDING[row["label"]], row
        assert row["original_spans"], row
        for span in row["original_spans"].split("; "):
            start, end = map(int, span.split(":"))
            assert abstract[start:end].casefold() == row["label"].casefold(), row
        assert f"[[{row['label']}]]" in row["context"], row

    chemicals = {
        row["label"]: row
        for row in rows
        if row["field"] == "chemical_utilization_object"
    }
    assert chemicals["glucose"]["chemical_relationship_id"] == "METPO:2000006"
    assert chemicals["NaCl"]["chemical_relationship_id"] == "METPO:2000014"
    assert all(row["chemicals_utilized"] == "1" for row in chemicals.values())
    assert next(row for row in rows if row["field"] == "study_taxa")["study_taxa"] == "1"
    assert next(row for row in rows if row["field"] == "strains")["strains"] == "1"

    review = args.review.read_text(encoding="utf-8")
    for expected in (
        "# Extraction table review:",
        "Rows: 4",
        "Columns: 25",
        "## 1. Structure",
        "## 2. Content",
        "## 3. QC (all rows unless stated)",
    ):
        assert expected in review, expected

    print("Smoke assertions passed: extraction fixture, spans, grounding, export, and review consumption")


if __name__ == "__main__":
    main()
