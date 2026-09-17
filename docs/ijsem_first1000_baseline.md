# IJSEM first-1,000 reviewed baseline

This document describes the inputs, versions, extraction parameters, output
schema, and run provenance for the reviewed `cborg_gpt41mini` baseline dated
**2026-08-24**. The same facts are available in machine-readable form in
[`config/ijsem_first1000_baseline_provenance.json`](../config/ijsem_first1000_baseline_provenance.json).

## Baseline identity and provenance

| Property | Value |
| --- | --- |
| Baseline label | `cborg_gpt41mini` |
| Review status | Reviewed baseline |
| Run date | `2026-08-24` |
| Run time/time zone | Not recorded; do not infer either from the date-stamped filename |
| Output | `data/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.tsv` |
| Output SHA-256 | `7facfae0aa2eb15c900bdaffc074efa1734f9f3a94a47adc05c08f02a83cb516` |
| Logical rows | 14,982 data rows plus one header |
| Corpus coverage | 1,000 documents and 1,000 distinct PMIDs |
| Producer repository | `https://github.com/CultureBotAI/auto-term-catalog` |
| Producer commit | `3fe168541e187316e6dee7ee2c7960a208d32101` |
| Artifact first committed in | `c7ee87135cc1c1aea041c332bb16806c01b83eed` |

The producer commit is the first committed end-to-end implementation that was
verified to recreate the reviewed TSV byte-for-byte from the saved extraction
and pinned inputs. The table itself first entered the repository in the
artifact commit. This distinction is explicit because the producer code was
committed after the original run date.

The run date has day precision only. No start time, finish time, or time zone
was retained for the original model run.

## Input abstracts

The input texts are IJSEM abstracts retrieved by PMID from the
[Europe PMC REST API](https://europepmc.org/RestfulWebService). For each row in
`config/ijsem_first1000_manifest.tsv`, the fetcher requests:

```text
GET https://www.ebi.ac.uk/europepmc/webservices/rest/search
query=EXT_ID:{pmid} AND SRC:MED
format=json
resultType=core
pageSize=1
```

The fetcher uses `abstractText`, decodes HTML entities, removes markup tags,
collapses whitespace, and trims the result. It then verifies the text against
the per-abstract SHA-256 in the manifest. The corpus version is therefore the
committed set of PMIDs, filenames, ordering, and text hashes—not the mutable
current Europe PMC response.

| Corpus property | Value |
| --- | --- |
| Manifest | `config/ijsem_first1000_manifest.tsv` |
| Manifest SHA-256 | `39460c40696513c7fa987484f29c76e229827cfd1dba84c383e2fbb20b8977c6` |
| Selection | First 1,000 bytewise-sorted source filenames in the reviewed IJSEM corpus |
| Abstract retrieval date | Not recorded |

Run `scripts/fetch_ijsem_abstracts.py` as shown in the main README to obtain
the inputs. The command fails on content drift. Do not use
`--allow-content-drift` when reproducing this baseline.

## Ontology and knowledge-graph inputs

### KG-Microbe merged graph

KG-Microbe documents its canonical merged artifact and release locations in
the [KG-Microbe repository](https://github.com/Knowledge-Graph-Hub/kg-microbe#build-and-release-artifacts).
The exact baseline archive was recorded as downloaded on
`2026-01-15T21:01:17Z` from:

```text
https://drive.usercontent.google.com/download?id=1SwkuuJjwVfNJk086pMvcZIy14cvJ8lNm&export=download
```

That archive does not contain a release tag, graph build commit, or provenance
file. Its version is therefore defined by its checksum and the checksums of its
two members. Component source versions, including the CHEBI and NCBITaxon
versions incorporated into the graph, are not recoverable from the archive.
A current KG-Microbe build is not an exact substitute.

| Artifact | SHA-256 | Bytes | Logical data rows |
| --- | --- | ---: | ---: |
| `merged-kg.tar.gz` | `8424fac29b07c4bd15a6d2194a43995433c459eb687338176719f08aacd1b917` | 214,885,350 | — |
| `merged-kg_nodes.tsv` | `fd3d590cd177d2269ac23bc5272004ec0b7ed5e640ff2a603870444457546b8e` | 212,932,944 | 1,546,598 |
| `merged-kg_edges.tsv` | `1c6070a261318cd8e95b3dad721905747d7b8b059c0f9b3ad01f4f47dbf70552` | 1,085,378,218 | 6,854,490 |

If the recorded archive link is unavailable, request the checksum-pinned
archive from the KG-Microbe/CultureBotAI maintainers. Labeling it merely as a
`2026-01-14` or `2026-01-15` release would be misleading; those are observed
file/acquisition dates, not an embedded upstream release version.

### METPO

The baseline used METPO with declared ontology version `2026-06-12` and
version IRI `https://w3id.org/metpo/releases/2026-06-12/metpo.owl`. The exact
bytes come from the later artifact-regeneration commit
[`07a05248b6f9080d7bb07dd7edc06c12520fb7de`](https://github.com/berkeleybop/metpo/commit/07a05248b6f9080d7bb07dd7edc06c12520fb7de),
which retained the `2026-06-12` ontology version:

```bash
curl -L \
  https://raw.githubusercontent.com/berkeleybop/metpo/07a05248b6f9080d7bb07dd7edc06c12520fb7de/metpo.owl \
  -o metpo.owl
```

| Property | Value |
| --- | --- |
| Declared version | `2026-06-12` |
| Artifact revision | `07a05248b6f9080d7bb07dd7edc06c12520fb7de` |
| SHA-256 | `8b6f8fe0510a698579e532658c8ace05da2550093365df9ca83feb0741778415` |
| Bytes | 1,115,523 |

The tagged `2026-06-12` file has different bytes. Use the commit-pinned URL and
checksum above for exact baseline reproduction.

### Verify local input files

```bash
shasum -a 256 "$MERGED_KG_NODES" "$MERGED_KG_EDGES" "$METPO_OWL"
```

The three results must respectively match the node, edge, and METPO hashes
above before attempting an exact replay.

## Model, prompt, and extraction parameters

| Parameter | Reviewed-baseline value |
| --- | --- |
| Baseline/model label | `cborg_gpt41mini` |
| API endpoint | [`https://api.cborg.lbl.gov`](https://cborg.lbl.gov/api_examples/) |
| OntoGPT model provider | `openai` |
| Requested model route | `openai/gpt-4.1-mini` |
| Temperature | `0.0` |
| Documents | `1000` |
| Batch size | `100` |
| Output format | Multi-document YAML |
| OntoGPT version | `1.0.16` |
| PyYAML version | `6.0.3` |
| Template | `src/templates/chemical_utilization_no_grounding.yaml` |
| Template SHA-256 | `4fb6175377070c13739f3f7d64d3849aa9148e69f2c971bac1b25ea31f9e65ef` |
| OntoGPT grounding | Disabled; grounding is performed by repository scripts |

The template is the complete prompt/schema source and lists every allowed
chemical-utilization and strain relationship. The run requested the CBORG
route `openai/gpt-4.1-mini`. A dated backend model snapshot was not retained in
the response metadata, so the provenance does not claim that a particular
provider snapshot was proven. The upstream GPT-4.1 mini family has a dated
`gpt-4.1-mini-2025-04-14` snapshot, but that fact alone does not establish what
CBORG served for this run.

Post-extraction parameters were:

| Parameter | Value |
| --- | --- |
| Mention matching | Case-insensitive literal match, then flexible whitespace/sign matching, then stored OntoGPT spans |
| Context window | 50 characters on each side of a located mention |
| Entity normalization | Unicode NFKC, case-fold, trim, and whitespace collapse |
| KG match | Exact normalized primary label or synonym |
| Preferred identifiers | CHEBI for chemicals; NCBITaxon for taxa and strains |
| METPO relationships | Strict exact normalized label/synonym match |
| Maximum incident edge evidence | 5 entries per grounded identifier |
| Growth-condition expansion | Enabled for NaCl, temperature, and pH observations |
| Deterministic environment | `LC_ALL=C`, `PYTHONHASHSEED=0`, `TZ=UTC` |

## Output schema

The output is UTF-8 TSV written with a header. Values containing tabs,
newlines, or quotes use standard CSV quoting with tab as the delimiter. Count
records with a TSV/CSV parser rather than `wc -l`, because source context may
contain embedded newlines.

| Column | Meaning |
| --- | --- |
| `doc` | Deterministic 1-based document number after bytewise source-filename ordering. |
| `source_file` | Manifest/source abstract filename. |
| `pmid` | PubMed identifier parsed from `source_file`. |
| `field` | Originating extraction or expansion field, such as `strains`, `study_taxa`, `chemical_utilization_object`, `temperature_observation`, or `pH_observation`. |
| `kind` | Row class: `strain`, `taxon_candidate`, `chemical`, or `phenotype_observation`. |
| `entity_id` | OntoGPT entity identifier, normally an `AUTO:` identifier before KG grounding. |
| `label` | Extracted mention or generated observation label represented by this row. |
| `original_spans` | Semicolon-separated zero-based half-open `start:end` offsets in the source abstract. |
| `context` | Source snippet with the matched mention and relevant relationship subject enclosed in `[[...]]`. |
| `relationship_subject_id` | OntoGPT identifier for the strain/subject of a relationship. |
| `relationship_subject_label` | Human-readable strain/subject label. |
| `chemical_relationship` | Extracted predicate or generated environmental-observation predicate before display-label normalization. |
| `chemical_level_type` | Observation subtype: blank, `chemical_name`, `concentration`, `optimum`, `range`, or `growth`. |
| `chemical_base_label` | Base chemical or environmental variable, for example `NaCl`, `temperature`, or `pH`. |
| `chebi_label` | Chemical text used/displayed for CHEBI-related rows; blank for nonchemical environmental observations. |
| `chemicals_utilized` | Binary `1` when the row represents a chemical-utilization object, otherwise `0`. |
| `study_taxa` | Binary `1` when the row represents a focal study taxon, otherwise `0`. |
| `strains` | Binary `1` when the row represents a strain identifier, otherwise `0`. |
| `chemical_relationship_id` | METPO CURIE for the normalized relationship. |
| `chemical_relationship_label` | Preferred METPO relationship label. |
| `chemical_relationship_match_type` | How the relationship was assigned, such as METPO `label` or generated `kg_microbe_metpo`. |
| `grounded_id` | Best-ranked CHEBI, NCBITaxon, METPO, or kg-microbe identifier. |
| `grounded_ids` | Pipe-separated ordered set of all eligible exact normalized matches. |
| `kg_name` | Name associated with the selected grounding; observation rows may carry their generated observation label here. |
| `kg_category` | Biolink/KG category of the selected node or the observation category assigned by expansion. |
| `match_type` | Grounding method: blank, `name`, `synonym`, `context_concentration`, `context_optimum`, or `kg_microbe_metpo`. |
| `kg_edge_count` | Number of merged-KG edges incident on the selected grounded identifier. |
| `kg_edge_evidence` | Up to five pipe-separated `direction:predicate:neighbor` evidence entries used for audit/context. |

An empty grounding field means that the deterministic exact-match procedure
did not find an eligible node; it does not mean that the mention was absent
from the abstract.

## Reproduce and verify

Follow the setup and full-run commands in the main README. For a replay from a
saved OntoGPT YAML stream, use the documented `--extraction` and
`--documents-dir` arguments. Verify the resulting table with:

```bash
shasum -a 256 \
  data/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.tsv
```

An exact replay prints:

```text
7facfae0aa2eb15c900bdaffc074efa1734f9f3a94a47adc05c08f02a83cb516
```

A fresh model call is not expected to be byte-reproducible. Exact baseline
replay requires the saved OntoGPT extraction YAML, the manifest-verified
abstracts, and the checksum-pinned KG/METPO inputs.
