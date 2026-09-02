---
name: review-extraction-table
description: Analyze and review an OntoGPT extraction + KG-grounding table (TSV/CSV in data/) for content, structure, and QC. Use when a new extraction/grounding table arrives (e.g. from the chemical_utilization pipeline), when asked to "review", "QC", "profile", or "catalog AUTO terms" from such a table, or before building a term catalog from it.
---

# Review an extraction table

These tables are the merged output of OntoGPT extraction over abstracts plus
KG-Microbe grounding. One row = one extracted entity mention in one document.
Typical schema (28 cols): `doc, source_file, pmid, field, kind, entity_id,
label, original_spans, context, relationship_subject_id,
relationship_subject_label, chemical_relationship, chemical_level_type,
chemical_base_label, chebi_label, chemicals_utilized, study_taxa, strains,
chemical_relationship_id, chemical_relationship_label,
chemical_relationship_match_type, grounded_id, grounded_ids, kg_name,
kg_category, match_type, kg_edge_count, kg_edge_evidence`.

Key facts about the format:
- `entity_id` is always `AUTO:<url-encoded label>` — an OntoGPT placeholder for
  an ungrounded term. **Grounding lives in `grounded_id`**, not `entity_id`.
- `field` = the schema slot (`strains`, `study_taxa`,
  `chemical_utilization_object`, `temperature_observation`, `pH_observation`);
  `kind` = entity type (`strain`, `taxon_candidate`, `chemical`,
  `phenotype_observation`).
- `match_type`: `name` / `synonym` (lexical), `kg_microbe_metpo` (phenotype →
  METPO class), `context_concentration` / `context_optimum` (value parsed from
  context). Empty = ungrounded.
- `context` shows the mention in `[[double brackets]]`.
- Grounding targets, by frequency: CHEBI (chemicals), NCBITaxon (taxa), METPO
  (phenotype observations), then a long tail of `mediadive.ingredient`,
  `kgmicrobe.strain` (e.g. `kgmicrobe.strain:DSM-14988`), `CAS-RN`, `PubChem`,
  `mediadive.medium/solution`. Anything else (e.g. `UBERON` for a chemical) is
  suspect. Strains are essentially never grounded (~0.5%).
- `chemical_relationship_match_type` uses a *different* vocabulary from
  `match_type` (`label` / `kg_microbe_metpo`); `chemical_level_type` is
  `chemical_name` / `range` / `optimum` / `concentration` / `growth`.
- `kg_edge_count` / `kg_edge_evidence` are only populated for lexical
  (name/synonym) groundings; METPO rows always show 0 — not a defect.

## Procedure

1. **Run the profiler** (`pip install -r .claude/skills/review-extraction-table/requirements.txt`):
   ```bash
   python .claude/skills/review-extraction-table/scripts/profile_table.py data/<table>.tsv \
       --out reports/<table>.review.md --catalog-out reports/<table>.ungrounded_catalog.tsv
   ```
   It writes a Markdown report with sections: 1 Structure, 2 Content, 3 QC,
   4 Ungrounded-term catalog, 5 Extraction quality, 6 Flags. Create `reports/` if missing. Commit the
   `.review.md`; the catalog `.tsv` is gitignored (regenerable in seconds).

   **Every number in the report is code-computed** — deterministic pandas
   filters, group-bys, and regex matches in `profile_table.py`; no count is
   hand-entered or model-generated. The report's *Provenance* block (in the
   header) records the git commit of the script and of
   `full_scientific_name.py` (which computes §5f), library versions, and a
   regeneration command, so any count can be reproduced or audited. If a
   reader asks "where does this number come from?", point at that block and
   the section's italic method note.

2. **Read the report and interpret — don't just paste it.** For each section
   answer:
   - *Structure*: does the schema match the expected columns? Any role the
     script couldn't resolve? Does doc count match what was promised
     (e.g. "first 1000 abstracts")?
   - *Content*: is the field/kind mix plausible? Which vocabularies were used
     for grounding? What are the dominant terms — do they make sense for the
     corpus (IJSEM → NaCl, glucose, temperature/pH optima)?
   - *QC*: grounding coverage per field; labels mapped to multiple IDs;
     `match_type=name` rows whose `kg_name` differs from `label`; duplicates;
     placeholder or over-long labels; malformed spans.
   - *Catalog*: what is in the ungrounded set, by bucket (ungrounded rows
     only — QC flags above count all rows). `strain (kind=strain)` is expected
     and usually not a catalog candidate, so it is summarised as a composition
     table (base = unique labels; partition sums to 100%, cross-cutting
     properties overlap) plus the few labels seen in >1 document; ungrounded taxa are mostly the novel
     species described by the paper itself; chemicals/media/enzymes missing
     from CHEBI/MediaDive are the interesting ones.

   - *Extraction quality (§5)* — these are review queues, not verdicts:
     - **5a false positives**: read every 1–2-char synonym match (element
       symbol vs amino-acid code, e.g. `K`→lysine) and every "no word
       overlap" row (sugars are the classic miss, e.g. `d-glucose`→D-fructose);
       each table carries an `example_context` snippet so you can judge the
       mention in place; kind/kg_category mismatches should be zero.
     - **5b label triage**: true noise (placeholders, value/unit-only labels,
       ≥6-word labels with values leaked in) is separated from *real* terms
       that just need a different modeling target: abstract class phrases
       (`carbon sources` — we do model abstract classes), enzyme
       activity/assay phrases (functions or assays → METPO, §5d), and growth
       media (→ MediaDive). Only the first group is noise to drop/fix; the
       second group is routing work, not extraction error.
     - **5c recall/truncation**: docs with ≤N rows; docs where a field cue
       (°C, pH, NaCl…) appears in *other rows'* context but the field has no
       row; span offset errors (`[[ (optimum pH 7.0]]`); spans that are a
       substring inside a longer word (`glu[[co]]se`, `Pseudo[[dysgonomonas]]`
       — the span *locator* matched by substring, so `original_spans` are
       wrong upstream and short symbols like CO/Si/K get bogus mentions);
       rows with no `original_spans`. Only the source abstracts can confirm
       true recall.
     - **5d METPO/vocabulary gaps**: relationship types without a METPO id;
       ungrounded enzyme-activity/assay labels (`oxidase`, `urease`,
       `H2/CO2`) — these are functions or assays, not chemicals, and are
       candidates for METPO function/assay classes; frequent ungrounded
       specific chemicals (CHEBI synonym gaps such as
       `meso-diaminopimelic acid`, `dl-lactate`).
     - **5e process/prompt gaps**: placeholder spelling variants (prompt should
       say *omit*), labels typed as more than one `kind`, no provenance
       columns (model/prompt/schema version), case-only label variants.
       Confirm against the actual extraction prompt and schema.
     - **5f strain name resolution**: share of `strains` rows that get a
       `Genus species STRAIN` name from `src/process_terms/full_scientific_name.py`
       and the rule breakdown; low resolution usually means the paper's novel
       species never appears next to its type strain in the extracted contexts.

3. **Spot-check by hand** — pick ~5 grounded rows and ~5 ungrounded rows per
   field with `grep`/pandas and confirm the grounding is right against the
   `context`. Report what you checked.

4. **Write up** findings as: summary numbers → notable issues (with row
   examples) → recommendations (re-grounding, synonym additions, schema
   fixes). File GitHub issues for real defects in the upstream pipeline.

## Extending the profiler

- New column names: add them to `ROLE_CANDIDATES` in `scripts/profile_table.py`.
- New QC rule: append to `flags` in the QC section and, if useful, a table.
- New ungrounded bucket: add a regex + branch in `bucket_ungrounded()`.
- New §5b bucket: add an entry to the `noise` dict (not a real term) or the
  `retarget` dict (real term, different modeling target); new field cue for
  the recall proxy: `FIELD_CUES`; new trait pattern: `TRAIT_RE`.
