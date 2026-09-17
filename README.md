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

## Setup

The pipeline needs Python 3.11 or newer, network access to Europe PMC and the
configured model endpoint, and local snapshots of:

- `merged-kg_nodes.tsv`
- `merged-kg_edges.tsv`
- `metpo.owl`

Clone the repository and install the pinned extraction dependencies in an
isolated environment:

```bash
git clone git@github.com:CultureBotAI/auto-term-catalog.git
cd auto-term-catalog
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements-extraction.txt
```

### Environment variables and credentials

The default configuration calls the CBORG endpoint. It requires the following
credential at run time:

| Variable | Required | Purpose |
| --- | --- | --- |
| `CBORG_API_KEY` | Yes for a new default-config extraction | Authentication for `https://api.cborg.lbl.gov`; the runner passes it to OntoGPT as `OPENAI_API_KEY` in the child process because that is the variable expected by the OpenAI-compatible client. |
| `OPENAI_API_KEY` | Alternative | Accepted directly when it contains a credential valid for the API endpoint selected in the pipeline configuration. If both variables exist, `OPENAI_API_KEY` takes precedence. |

Europe PMC does not require an API key for this workflow. Grounding is local
and requires no credential.

For convenience, these non-secret path variables are used in the commands
below: `MERGED_KG_NODES`, `MERGED_KG_EDGES`, and `METPO_OWL`. They are shell
variables, not implicit pipeline configuration; the command passes their
values to the corresponding arguments.

Copy the example file, edit only the ignored `.env`, and load it into the
current shell:

```bash
cp .env.example .env
chmod 600 .env
# Edit .env and set CBORG_API_KEY plus the three absolute input paths.
set -a
source .env
set +a
```

`.env`, `.env.local`, and environment-specific local variants are ignored by
Git. `.env.example` contains variable names and placeholders only. Before
committing, confirm that no credential is staged:

```bash
git status --short
git diff --cached
```

Do not put API keys in the JSON configuration, command arguments, logs, or
committed shell scripts.

## Run the complete pipeline

This command fetches the manifest's IJSEM abstracts from Europe PMC, runs
OntoGPT, locates source mentions, grounds entities and relationships, expands
growth-condition observations, and exports the final table:

```bash
python3 scripts/run_ijsem_pipeline.py \
  --config config/ijsem_first1000_pipeline.json \
  --nodes "$MERGED_KG_NODES" \
  --edges "$MERGED_KG_EDGES" \
  --metpo "$METPO_OWL"
```

Default generated paths are:

| Artifact | Path |
| --- | --- |
| Verified abstracts | `work/ijsem_first1000/abstracts/` |
| OntoGPT batch inputs, outputs, and logs | `work/ijsem_first1000/ontogpt_batches/` |
| Combined OntoGPT extraction | `work/ijsem_first1000/chemical_utilization_ijsem_first1000_cborg_gpt41mini_no_grounding.yaml` |
| Extraction run metadata | The same path with `.run.json` appended |
| Flattened mention/entity table | `work/ijsem_first1000/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.entities.tsv` |
| Final grounded table | `data/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.tsv` |

The `work/` directory and logs are ignored. Preserve the combined extraction
YAML and its run metadata outside the repository if an exact model-run replay
must be retained.

### Run each stage separately

The orchestrator above is equivalent to these three commands:

```bash
python3 scripts/fetch_ijsem_abstracts.py \
  --manifest config/ijsem_first1000_manifest.tsv \
  --output-dir work/ijsem_first1000/abstracts

python3 scripts/run_ontogpt_extraction.py \
  --config config/ijsem_first1000_pipeline.json \
  --documents-dir work/ijsem_first1000/abstracts \
  --output work/ijsem_first1000/chemical_utilization_ijsem_first1000_cborg_gpt41mini_no_grounding.yaml

scripts/generate_merged_kg_grounded_tsv.sh \
  --extraction work/ijsem_first1000/chemical_utilization_ijsem_first1000_cborg_gpt41mini_no_grounding.yaml \
  --documents-dir work/ijsem_first1000/abstracts \
  --nodes "$MERGED_KG_NODES" \
  --edges "$MERGED_KG_EDGES" \
  --metpo "$METPO_OWL" \
  --max-documents 1000 \
  --max-edge-evidence 5 \
  --expand-growth-conditions \
  --entities-output work/ijsem_first1000/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.entities.tsv \
  --output data/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.tsv
```

The fetch stage checks every abstract against the committed manifest. If
Europe PMC content has changed, it exits instead of silently generating a
different corpus. `--allow-content-drift` is available on the fetch script for
an intentional manifest refresh.

You can validate the corpus and inspect the generated OntoGPT commands without
setting an API key or calling the model:

```bash
python3 scripts/run_ijsem_pipeline.py \
  --nodes "$MERGED_KG_NODES" \
  --edges "$MERGED_KG_EDGES" \
  --metpo "$METPO_OWL" \
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
  --nodes "$MERGED_KG_NODES" \
  --edges "$MERGED_KG_EDGES" \
  --metpo "$METPO_OWL" \
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
