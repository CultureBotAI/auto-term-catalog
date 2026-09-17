# auto-term-catalog

This repository extracts microbial phenotypes from IJSEM abstracts with
OntoGPT, locates each mention in its source abstract, grounds the result to
the merged KG, and exports review-ready TSV tables.

The checked-in 1,000-abstract result is
[`data/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.tsv`](data/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.tsv).
Its SHA-256 digest is recorded in
[`config/ijsem_first1000_artifacts.sha256`](config/ijsem_first1000_artifacts.sha256).

## Reproducible IJSEM pipeline

The full path from abstracts to the grounded table is:

1. `config/ijsem_first1000_manifest.tsv` fixes the ordered corpus by PMID,
   filename, and abstract SHA-256 digest.
2. `scripts/fetch_ijsem_abstracts.py` retrieves those abstracts from Europe
   PMC and refuses content that does not match the committed digest.
3. `scripts/run_ontogpt_extraction.py` batches the documents and runs OntoGPT
   with the committed template, model settings, and temperature.
4. `src/process_terms/extract_grounding_entities.py` associates each YAML
   document with its source PMID, finds literal mentions, and records character
   spans and surrounding context.
5. `src/process_terms/ground_entities_merged_kg.py` normalizes labels and
   synonyms, matches them to CHEBI, NCBITaxon, METPO, and kg-microbe strain
   nodes, and uses merged-KG edges as deterministic ranking/evidence context.
6. The two `scripts/expand_first100_*.py` programs add source-grounded
   concentration/optimum, salinity, temperature, and pH observations.
7. `scripts/generate_merged_kg_grounded_tsv.sh` joins these stages and writes
   the table used by the repository's review and downstream processing code.

The extraction settings are committed in
`config/ijsem_first1000_pipeline.json`:

| Setting | Value |
| --- | --- |
| OntoGPT template | `src/templates/chemical_utilization_no_grounding.yaml` |
| Model | `openai/gpt-4.1-mini` |
| API base | `https://api.cborg.lbl.gov` |
| Temperature | `0.0` |
| Batch size | `100` |
| Abstract count | `1000` |
| Maximum KG edge evidence rows | `5` |

### Install

Use Python 3.11 or newer and install the pinned extraction dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-extraction.txt
```

Download compatible `merged-kg_nodes.tsv`, `merged-kg_edges.tsv`, and
`metpo.owl` snapshots. Set the CBORG credential without writing it into the
repository:

```bash
export CBORG_API_KEY='...'
```

### Run from Europe PMC abstracts

```bash
python3 scripts/run_ijsem_pipeline.py \
  --nodes /path/to/merged-kg_nodes.tsv \
  --edges /path/to/merged-kg_edges.tsv \
  --metpo /path/to/metpo.owl
```

The fetch stage checks every abstract against the committed manifest. If
Europe PMC content has changed, it exits instead of silently generating a
different corpus. `--allow-content-drift` is available on the fetch script for
an intentional manifest refresh.

You can inspect all OntoGPT commands without calling the model:

```bash
python3 scripts/run_ijsem_pipeline.py \
  --nodes /path/to/merged-kg_nodes.tsv \
  --edges /path/to/merged-kg_edges.tsv \
  --metpo /path/to/metpo.owl \
  --documents-dir /path/to/verified/abstracts \
  --dry-run-extraction
```

### Replay grounding without another model call

To deterministically regenerate the final TSV from a saved OntoGPT YAML
stream, supply both the extraction and the verified source abstracts:

```bash
python3 scripts/run_ijsem_pipeline.py \
  --extraction /path/to/ontogpt-extraction.yaml \
  --documents-dir /path/to/verified/abstracts \
  --nodes /path/to/merged-kg_nodes.tsv \
  --edges /path/to/merged-kg_edges.tsv \
  --metpo /path/to/metpo.owl \
  --output /path/to/result_merged_kg_grounded.tsv
```

The corpus selection, mention-location, normalization, KG matching, merging,
and TSV ordering are deterministic. The committed corpus manifest and artifact
checksums make those portions auditable. A fresh LLM inference can still vary
despite temperature zero, so retain the generated OntoGPT YAML and run metadata
when exact replay of a model run is required.

## Grounding behavior

- YAML documents are paired with abstracts by exact normalized full-text
  equality, not by positional PMID assignment.
- Mention offsets use zero-based half-open `start:end` values in
  `original_spans` and retain matching context snippets.
- Grounding uses Unicode/case/whitespace-normalized exact names and synonyms.
- CHEBI is preferred for chemicals and NCBITaxon for taxa; exact primary-name
  matches precede synonym matches, then merged-KG connectivity and identifier
  order break ties.
- Chemical-utilization predicates must match a METPO object-property label or
  synonym in strict mode.
- Binary `chemicals_utilized`, `study_taxa`, and `strains` columns identify the
  role represented by each output row.

The review workflow is documented in
`.claude/skills/review-extraction-table/SKILL.md`; generated review reports are
written under `reports/`.
