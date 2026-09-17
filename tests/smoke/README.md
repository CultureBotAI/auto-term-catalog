# Offline end-to-end smoke test

This fixture represents one small OntoGPT extraction over an IJSEM-style
abstract. It exercises:

1. ingestion of the committed OntoGPT YAML extraction;
2. exact association with its PMID-labelled source abstract;
3. mention span and context location;
4. CHEBI, NCBITaxon, METPO, and kg-microbe strain grounding;
5. deterministic core TSV export; and
6. consumption by the existing `review-extraction-table` profiler.

It is intentionally offline: model inference is represented by the committed
`ontogpt_extraction.yaml` fixture, so the smoke test requires no credential,
network access, or nondeterministic model call. Live OntoGPT execution is
covered by the configuration/dry-run and full-run commands in the main README.
The fixture omits the baseline-specific optional growth-condition expansion,
which adds `chemical_level_type`, `chemical_base_label`, and `chebi_label` to
the 25-column core export; the review profiler intentionally accepts both
schemas.

From the repository root, install both requirement sets and run:

```bash
python3 -m pip install -r requirements-extraction.txt
python3 -m pip install -r .claude/skills/review-extraction-table/requirements.txt
tests/smoke/run_smoke_test.sh
```

By default, inspect the resulting table and review report at:

```text
work/smoke/smoke_merged_kg_grounded.tsv
work/smoke/smoke.review.md
```

Pass a directory as the first argument to write elsewhere. The runner performs
the export twice and byte-compares both the flattened entities and final table,
then asserts the spans against the source text, checks expected grounding and
METPO relationship IDs, and verifies the review report's structure and counts.
