---
name: review-extraction-table
description: Analyze and review an OntoGPT extraction + KG-grounding table (TSV/CSV in data/) for content, structure, and QC. Use when a new extraction/grounding table arrives (e.g. from the chemical_utilization pipeline), when asked to "review", "QC", "profile", or "catalog AUTO terms" from such a table, or before building a term catalog from it.
---

# Review an extraction table

These tables are the merged output of OntoGPT extraction over abstracts plus
KG-Microbe grounding. One row = one extracted entity mention in one document.
Typical schema (28 cols): `doc, source_file, pmid, field, kind, entity_id,
label, original_spans, context, relationship_subject_id, …, chemicals_utilized,
study_taxa, strains, chemical_relationship_id/label/match_type, grounded_id,
grounded_ids, kg_name, kg_category, match_type, kg_edge_count, kg_edge_evidence`.

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
- Expect grounding targets: CHEBI (chemicals), NCBITaxon (taxa), METPO
  (phenotype observations). Strains are essentially never grounded.

## Procedure

1. **Run the profiler** (pandas + tabulate required):
   ```bash
   python .claude/skills/review-extraction-table/scripts/profile_table.py data/<table>.tsv \
       --out reports/<table>.review.md --catalog-out reports/<table>.ungrounded_catalog.tsv
   ```
   It writes a Markdown report with sections: Structure, Content, QC,
   Ungrounded-term catalog, Flags. Create `reports/` if missing.

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
   - *Catalog*: what is in the ungrounded set, by bucket. Strain designations
     are expected and usually not catalog candidates; chemicals/media/enzymes
     missing from CHEBI are the interesting ones.

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
