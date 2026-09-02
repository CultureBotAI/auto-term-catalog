# Extraction table review: `chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.tsv`

- Size on disk: 7.4 MB
- Rows: 14,982
- Columns: 28


> **Provenance.** Every number in this report is computed by `.claude/skills/review-extraction-table/scripts/profile_table.py` (git a854581; pandas 2.3.3, Python 3.13.12) — deterministic pandas filters, group-bys and regex matches over the raw table. No count is hand-entered or model-generated; each section states what its check computes, and re-running the command below on the same table reproduces the numbers exactly. Only prose written *around* this report (interpretation, recommendations) comes from a reviewer.
>
> `python .claude/skills/review-extraction-table/scripts/profile_table.py data/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.tsv --out <report.md> [--catalog-out <catalog.tsv>] [--top N]`


## 1. Structure

### Columns

| column                           |   non_empty | pct_non_empty   |   n_unique | example                                                       |
|:---------------------------------|------------:|:----------------|-----------:|:--------------------------------------------------------------|
| doc                              |       14982 | 100.0%          |       1000 | 1                                                             |
| source_file                      |       14982 | 100.0%          |       1000 | 00001-41779015-abstract.txt                                   |
| pmid                             |       14982 | 100.0%          |       1000 | 41779015                                                      |
| field                            |       14982 | 100.0%          |          5 | strains                                                       |
| kind                             |       14982 | 100.0%          |          4 | strain                                                        |
| entity_id                        |       14982 | 100.0%          |      11006 | AUTO:Gardnerella%20vaginalis%201400E                          |
| label                            |       14982 | 100.0%          |      11006 | Gardnerella vaginalis 1400E                                   |
| original_spans                   |       14668 | 97.9%           |      12321 | 1040:1067                                                     |
| context                          |       14668 | 97.9%           |      13803 | ...T, Marseille-QA0894T and Marseille-Q2328T against [[Gardn  |
| relationship_subject_id          |        4886 | 32.6%           |       1061 | AUTO:Ax23T                                                    |
| relationship_subject_label       |        4886 | 32.6%           |       1061 | Ax23T                                                         |
| chemical_relationship            |        4886 | 32.6%           |         24 | produces                                                      |
| chemical_level_type              |        4886 | 32.6%           |          6 | chemical_name                                                 |
| chemical_base_label              |        4886 | 32.6%           |        557 | CH4                                                           |
| chebi_label                      |        2352 | 15.7%           |        671 | CH4                                                           |
| chemicals_utilized               |       14982 | 100.0%          |          2 | 0                                                             |
| study_taxa                       |       14982 | 100.0%          |          2 | 0                                                             |
| strains                          |       14982 | 100.0%          |          2 | 1                                                             |
| chemical_relationship_id         |        4886 | 32.6%           |         24 | METPO:2000202                                                 |
| chemical_relationship_label      |        4886 | 32.6%           |         24 | produces                                                      |
| chemical_relationship_match_type |        4886 | 32.6%           |          3 | label                                                         |
| grounded_id                      |        8263 | 55.2%           |       3744 | NCBITaxon:698956                                              |
| grounded_ids                     |        8263 | 55.2%           |       3755 | NCBITaxon:698956                                              |
| kg_name                          |        8263 | 55.2%           |       4050 | Gardnerella vaginalis 1400E                                   |
| kg_category                      |        8263 | 55.2%           |         14 | biolink:OrganismTaxon                                         |
| match_type                       |        8263 | 55.2%           |          6 | name                                                          |
| kg_edge_count                    |       14982 | 100.0%          |        329 | 9                                                             |
| kg_edge_evidence                 |        6116 | 40.8%           |       3433 | out:biolink:subclass_of:NCBITaxon:2702\|out:biolink:has_pheno |


- Documents: 1,000

- PMIDs: 1,000


## 2. Content


### `field`

| field                       |   rows |
|:----------------------------|-------:|
| strains                     |   5980 |
| study_taxa                  |   4116 |
| chemical_utilization_object |   2739 |
| temperature_observation     |   1144 |
| pH_observation              |   1003 |


### `kind`

| kind                  |   rows |
|:----------------------|-------:|
| strain                |   5980 |
| taxon_candidate       |   4116 |
| chemical              |   2739 |
| phenotype_observation |   2147 |


### `match_type`

| match_type            |   rows |
|:----------------------|-------:|
| (empty)               |   6719 |
| name                  |   4665 |
| kg_microbe_metpo      |   2147 |
| synonym               |    875 |
| context_concentration |    431 |
| context_optimum       |    145 |


### `kg_category`

| kg_category                                                              |   rows |
|:-------------------------------------------------------------------------|-------:|
| (empty)                                                                  |   6719 |
| biolink:OrganismTaxon                                                    |   3689 |
| biolink:OntologyClass                                                    |   2147 |
| biolink:ChemicalEntity\|biolink:ChemicalSubstance\|biolink:SmallMolecule |   1209 |
| biolink:ChemicalEntity\|biolink:SmallMolecule                            |    856 |
| biolink:SmallMolecule                                                    |    110 |
| biolink:ChemicalEntity                                                   |     90 |
| biolink:ChemicalEntity\|biolink:Macromolecule                            |     79 |
| biolink:ChemicalSubstance\|biolink:SmallMolecule                         |     62 |
| biolink:ChemicalEntity\|biolink:ChemicalSubstance\|biolink:Macromolecule |     14 |
| biolink:ChemicalRole\|biolink:ChemicalSubstance                          |      3 |
| biolink:ChemicalSubstance\|biolink:Macromolecule                         |      2 |
| biolink:AnatomicalEntity\|biolink:ChemicalEntity                         |      1 |
| biolink:ChemicalRole\|biolink:SmallMolecule                              |      1 |


### `chemical_level_type`

| chemical_level_type   |   rows |
|:----------------------|-------:|
| (empty)               |  10096 |
| chemical_name         |   2163 |
| range                 |   1113 |
| optimum               |   1058 |
| concentration         |    431 |
| growth                |    121 |


### `chemical_relationship_match_type`

| chemical_relationship_match_type   |   rows |
|:-----------------------------------|-------:|
| (empty)                            |  10096 |
| kg_microbe_metpo                   |   2723 |
| label                              |   2163 |


### field × kind

| field                       |   chemical |   phenotype_observation |   strain |   taxon_candidate |
|:----------------------------|-----------:|------------------------:|---------:|------------------:|
| chemical_utilization_object |       2739 |                       0 |        0 |                 0 |
| pH_observation              |          0 |                    1003 |        0 |                 0 |
| strains                     |          0 |                       0 |     5980 |                 0 |
| study_taxa                  |          0 |                       0 |        0 |              4116 |
| temperature_observation     |          0 |                    1144 |        0 |                 0 |


### entity_id prefixes

| prefix   |   rows |
|:---------|-------:|
| AUTO     |  14982 |


- Unique entity IDs: 11,006


### grounded_id prefixes

| prefix               |   rows |
|:---------------------|-------:|
| NCBITaxon            |   3660 |
| CHEBI                |   2348 |
| METPO                |   2147 |
| mediadive.ingredient |     43 |
| kgmicrobe.strain     |     29 |
| CAS-RN               |     27 |
| PubChem              |      6 |
| mediadive.medium     |      1 |
| UBERON               |      1 |
| mediadive.solution   |      1 |


### Top grounded terms (top 30)

| label                      | grounded_id   | kg_category                                                              | match_type       |   rows |
|:---------------------------|:--------------|:-------------------------------------------------------------------------|:-----------------|-------:|
| NaCl                       | CHEBI:26710   | biolink:ChemicalEntity\|biolink:ChemicalSubstance\|biolink:SmallMolecule | synonym          |    367 |
| pH optimum 7.0             | METPO:1001013 | biolink:OntologyClass                                                    | kg_microbe_metpo |    143 |
| temperature optimum 30 °C  | METPO:1001001 | biolink:OntologyClass                                                    | kg_microbe_metpo |    128 |
| glucose                    | CHEBI:17234   | biolink:ChemicalEntity\|biolink:SmallMolecule                            | name             |     77 |
| temperature optimum 37 °C  | METPO:1001001 | biolink:OntologyClass                                                    | kg_microbe_metpo |     74 |
| temperature optimum 28 °C  | METPO:1001001 | biolink:OntologyClass                                                    | kg_microbe_metpo |     73 |
| temperature optimum 25 °C  | METPO:1001001 | biolink:OntologyClass                                                    | kg_microbe_metpo |     51 |
| pH range 6.0-9.0           | METPO:1001015 | biolink:OntologyClass                                                    | kg_microbe_metpo |     50 |
| pH optimum 8.0             | METPO:1001013 | biolink:OntologyClass                                                    | kg_microbe_metpo |     36 |
| temperature range 15-37 °C | METPO:1001003 | biolink:OntologyClass                                                    | kg_microbe_metpo |     36 |
| acetate                    | CHEBI:30089   | biolink:ChemicalEntity\|biolink:SmallMolecule                            | name             |     34 |
| temperature range 10-40 °C | METPO:1001003 | biolink:OntologyClass                                                    | kg_microbe_metpo |     32 |
| nitrate                    | CHEBI:17632   | biolink:ChemicalEntity\|biolink:ChemicalSubstance\|biolink:SmallMolecule | name             |     32 |
| pH range 6.0-10.0          | METPO:1001015 | biolink:OntologyClass                                                    | kg_microbe_metpo |     32 |
| methanol                   | CHEBI:17790   | biolink:ChemicalEntity\|biolink:ChemicalSubstance\|biolink:SmallMolecule | name             |     30 |
| ribose                     | CHEBI:33942   | biolink:ChemicalEntity\|biolink:SmallMolecule                            | name             |     28 |
| pH range 6.0-8.0           | METPO:1001015 | biolink:OntologyClass                                                    | kg_microbe_metpo |     27 |
| temperature range 15-40 °C | METPO:1001003 | biolink:OntologyClass                                                    | kg_microbe_metpo |     27 |
| temperature range 20-40 °C | METPO:1001003 | biolink:OntologyClass                                                    | kg_microbe_metpo |     25 |
| pH optimum 7.0-8.0         | METPO:1001013 | biolink:OntologyClass                                                    | kg_microbe_metpo |     24 |
| pH optimum 6.0             | METPO:1001013 | biolink:OntologyClass                                                    | kg_microbe_metpo |     24 |
| pH optimum 7               | METPO:1001013 | biolink:OntologyClass                                                    | kg_microbe_metpo |     23 |
| methane                    | CHEBI:16183   | biolink:ChemicalEntity\|biolink:ChemicalSubstance\|biolink:SmallMolecule | name             |     22 |
| temperature range 4-37 °C  | METPO:1001003 | biolink:OntologyClass                                                    | kg_microbe_metpo |     22 |
| formate                    | CHEBI:15740   | biolink:ChemicalEntity\|biolink:SmallMolecule                            | name             |     21 |
| galactose                  | CHEBI:28260   | biolink:ChemicalEntity\|biolink:SmallMolecule                            | name             |     20 |
| temperature growth 30 °C   | METPO:1001002 | biolink:OntologyClass                                                    | kg_microbe_metpo |     20 |
| pH range 5.0-8.0           | METPO:1001015 | biolink:OntologyClass                                                    | kg_microbe_metpo |     19 |
| pH range 7.0-8.0           | METPO:1001015 | biolink:OntologyClass                                                    | kg_microbe_metpo |     19 |
| starch                     | CHEBI:28017   | biolink:ChemicalEntity\|biolink:Macromolecule                            | name             |     19 |



## 3. QC (all rows unless stated)


- Grounding coverage: **8,263 / 14,982 (55.2%)**


### Grounding by field

| field                       |   grounded |   ungrounded |   pct_grounded |
|:----------------------------|-----------:|-------------:|---------------:|
| chemical_utilization_object |       2427 |          312 |           88.6 |
| pH_observation              |       1003 |            0 |          100   |
| strains                     |         30 |         5950 |            0.5 |
| study_taxa                  |       3659 |          457 |           88.9 |
| temperature_observation     |       1144 |            0 |          100   |


### Labels grounded to >1 ID (0)

_(none)_


- Located rows sharing the same mention key ['doc', 'field', 'entity_id', 'original_spans']: **1,609** (314 span-less rows excluded from this check)

  - These differ only in relationship columns (relationship_subject_id, relationship_subject_label, chemical_relationship, chemical_relationship_id, chemical_relationship_label): one row per (mention, relationship) — expected, not a defect.

  - Span-less rows repeating the same (doc, field, entity): **25**, differing only in relationship columns — expected expansion.

- Fully identical rows: **0**



## 4. Ungrounded-term catalog (rows with empty grounded_id only)


- Ungrounded rows: 6,719; unique labels: 6,454


### By bucket

| bucket                       |   rows |
|:-----------------------------|-------:|
| strain (kind=strain)         |   5950 |
| taxon (not in NCBITaxon)     |    441 |
| chemical (not in CHEBI)      |    181 |
| growth medium / component    |    101 |
| enzyme / assay               |     29 |
| unspecified/placeholder      |     13 |
| culture-collection accession |      4 |


### chemical (not in CHEBI) — 110 unique labels (top 30)

| label                                      |   rows |   n_docs | fields                      | example_context                                                                                                          |
|:-------------------------------------------|-------:|---------:|:----------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| meso-diaminopimelic acid                   |     14 |       10 | chemical_utilization_object | ... 0-5 % NaCl and whole-cell hydrolysates contained [[meso-diaminopimelic acid]] as the cell-wall diamino acid. On the  |
| H2/CO2                                     |      7 |        5 | chemical_utilization_object | .... Dimethylamine, trimethylamine and methanethiol, [[H2/CO2]], formate, acetate, pyruvate, lactate and glucose ...     |
| dl-lactate                                 |      7 |        5 | chemical_utilization_object | ...-xylose, d-ribose, glycerol, ribitol, d-mannitol, [[dl-lactate]] and d-gluconate. Based on phylogenetic and phenot... |
| ll-diaminopimelic acid                     |      7 |        4 | chemical_utilization_object | ...Whole-cell hydrolysates of strain [[BI20T]] contained [[ll-diaminopimelic acid]] and whole-cell sugars contained gluc |
| carbon sources                             |      6 |        2 | chemical_utilization_object | ...xhibited high auxotrophy, being unable to use all [[carbon sources]] tested, likely due to genome reduction (4.6 Mbp) |
| methyl-β-d-glucopyranoside                 |      5 |        1 | chemical_utilization_object | ...f α-glucosidase activity and acid production from [[methyl-β-d-glucopyranoside]] and maltose. The two novel species c |
| indole acetic acid                         |      5 |        3 | chemical_utilization_object | ...ding enzymes for synthesizing plant hormones like [[indole acetic acid]] and gibberellic acid. Experimental validatio |
| soluble starch                             |      3 |        2 | chemical_utilization_object | ...rate utilization encompassed cellobiose, sucrose, [[soluble starch]], casein, glucose, xylan, ethanol, ribose, yeast  |
| tartaric acid                              |      3 |        1 | chemical_utilization_object |                                                                                                                          |
| carotenoid-type pigments                   |      3 |        2 | chemical_utilization_object | ...timally in 2% NaCl). Strain [[SZ-1-7T]] could produce [[carotenoid-type pigments]]. Strain 4WD22T grew from 20 to 45  |
| N-acetyl-glucosamine                       |      2 |        1 | chemical_utilization_object | ...itrate and utilized various carbohydrates but not [[N-acetyl-glucosamine]]; they differed in sorbitol assimilation. T |
| p-hydroxy-phenylacetic acid                |      2 |        1 | chemical_utilization_object | ...l-d-glucosamine, maltose, adipate, phenylacetate, [[p-hydroxy-phenylacetic acid]], Tween 40, glycyl-l-proline, d-malt |
| phosphatidylethanolamine (PE)              |      2 |        1 | chemical_utilization_object | ... major polar lipid identified in strain [[MSW6T]] was [[phosphatidylethanolamine (PE)]]. On the other hand, strain RS |
| mono- and oligosaccharides                 |      2 |        1 | chemical_utilization_object | ...y on a wide range of organic substrates including [[mono- and oligosaccharides]], amino acids and short-chained fatty |
| methyl-α-d-glucopyranoside                 |      2 |        1 | chemical_utilization_object | ...urease, β-glucosidase, assimilation of inulin and [[methyl-α-d-glucopyranoside]] and degradation of casein. Compared  |
| metal ions                                 |      2 |        1 | chemical_utilization_object | ...problems and restoring environments polluted with [[metal ions]] and/or benzoate. On the basis of the results of m... |
| multiple antibiotics                       |      2 |        1 | chemical_utilization_object | ... and ZM25. Strains ZM22T and [[Y6]] were resistant to [[multiple antibiotics]], whereas strains ZM23T, ZM24 and ZM25  |
| natural rubber                             |      2 |        1 | chemical_utilization_object | ...1T, were isolated using mineral salts medium with [[natural rubber]] as the sole carbon source. Polyphasic taxonomy p |
| fish gut fluid                             |      2 |        2 | chemical_utilization_object | ...[[BP47G]] grew on agar medium containing mannitol and [[fish gut fluid]] as the sole carbon sources. Clear colonies o |
| actidione                                  |      2 |        1 | chemical_utilization_object | ...owing the growth on streptomycin thallous acetate [[actidione]] medium was considered to result from a modificati...  |
| amoxicillin-clavulanic acid                |      2 |        1 | chemical_utilization_object | ...dicated that [[CDC186T]] and CDC192 were resistant to [[amoxicillin-clavulanic acid]] and tigecycline. On the basis o |
| dl-lactic acid                             |      2 |        2 | chemical_utilization_object | ...strain exhibited heterofermentative production of [[dl-lactic acid]] from glucose. Optimal growth was observed at 25- |
| poly(butylene succinate-co-adipate) (PBSA) |      2 |        1 | chemical_utilization_object | ...ed the ability to degrade biodegradable plastics, [[poly(butylene succinate-co-adipate) (PBSA)]] and poly(ε-caprolact |
| d,l-lactate                                |      2 |        1 | chemical_utilization_object | ...to lyse gelatin and sheep blood and to assimilate [[d,l-lactate]], along with their inability to acidify d-glucose .. |
| coral mucus                                |      2 |        1 | chemical_utilization_object | ... analysis indicated these two strains may utilize [[coral mucus]] or chitin. Based on above characteristics, these .. |
| poly(ε-caprolactone)                       |      2 |        1 | chemical_utilization_object | ...s, poly(butylene succinate-co-adipate) (PBSA) and [[poly(ε-caprolactone)]]. Phylogenetic analyses based on the 16S rR |
| sugars                                     |      2 |        2 | chemical_utilization_object | ...3 mol%. The isolate did not grow using any tested [[sugars]] but grew well on arginine and glycine. It is capa...     |
| soluble phosphorus                         |      2 |        1 | chemical_utilization_object | ...s and produce siderophores, for which the maximum [[soluble phosphorus]] concentrations could reach 510.03±7.11 and 5 |
| α-hydroxy butyric acid                     |      2 |        1 | chemical_utilization_object | ...-l-proline, d-maltose, d-galactonic acid lactone, [[α-hydroxy butyric acid]], myo-inositol, sucrose, l-histidine, d-m |
| short-chained fatty acids                  |      2 |        1 | chemical_utilization_object | ...uding mono- and oligosaccharides, amino acids and [[short-chained fatty acids]]. MK-8 was identified as the major res |


### enzyme / assay — 12 unique labels (top 12)

| label                                           |   rows |   n_docs | fields                      | example_context                                                                                                          |
|:------------------------------------------------|-------:|---------:|:----------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| oxidase                                         |      9 |        5 | chemical_utilization_object | ...polyphasic approach. The cells were catalase- and [[oxidase]]-positive and rod-shaped. The five novel strains w...    |
| urease                                          |      6 |        5 | chemical_utilization_object | ...closely related species by the (delayed) positive [[urease]] reaction in the API20NE test and by weak growth o...     |
| catalase activity                               |      2 |        1 | chemical_utilization_object | ... bacterial isolates showed positive reactions for [[catalase activity]], Tween 80 hydrolysis and tellurite reduction. |
| β-glucuronidase                                 |      2 |        2 | chemical_utilization_object | ... and trehalose, as well as negative reactions for [[β-glucuronidase]], mannose, inositol and glycerol. Genotypic and  |
| β-glucosidase                                   |      2 |        1 | chemical_utilization_object | ... with respect to their ability to produce urease, [[β-glucosidase]], assimilation of inulin and methyl-α-d-glucopyran |
| 1-aminocyclopropane-1-carboxylic acid deaminase |      2 |        1 | chemical_utilization_object | ... of producing indole acetic acid, siderophore and [[1-aminocyclopropane-1-carboxylic acid deaminase]], and also showe |
| nitrogenase                                     |      1 |        1 | chemical_utilization_object | ...of methanogene. The nif cluster, encompassing the [[nitrogenase]] genes, was found in every N2-fixing strain within.. |
| α-glucosidase                                   |      1 |        1 | chemical_utilization_object | ...re differentiated by their positive reactions for [[α-glucosidase]], l-arabinose and trehalose, as well as negative r |
| α-arabinosidase activity                        |      1 |        1 | chemical_utilization_object | ...dicola, including strain [[21CYCFAH17_ST]], exhibited [[α-arabinosidase activity]], whereas strain 25CYCFAH16T and ot |
| urease substrate                                |      1 |        1 | chemical_utilization_object |                                                                                                                          |
| protease                                        |      1 |        1 | chemical_utilization_object | A novel [[protease]]-producing and cellulose-degrading actinobacterium...                                                |
| 1-aminocyclopropane-1-carboxylate deaminase     |      1 |        1 | chemical_utilization_object | ...cytokinin and auxin plant hormones and to produce [[1-aminocyclopropane-1-carboxylate deaminase]]. The DNA G+C conten |


### growth medium / component — 48 unique labels (top 30)

| label                                                                   |   rows |   n_docs | fields                      | example_context                                                                                                          |
|:------------------------------------------------------------------------|-------:|---------:|:----------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| nutrient agar                                                           |      6 |        3 | chemical_utilization_object | ... required for growth. Best growth was observed on [[nutrient agar]] or marine agar media. The strains contained dipho |
| R2A agar                                                                |      6 |        4 | chemical_utilization_object | ... performed on these strains. Both strains grow on [[R2A agar]] forming mucous, bright yellow colonies, developin...   |
| tryptic soy agar                                                        |      6 |        3 | chemical_utilization_object | ...rization. Strain [[MMS21-DH1MA12T]] grew optimally in [[tryptic soy agar]], forming yellow-coloured, convex and smoot |
| marine agar                                                             |      5 |        3 | chemical_utilization_object | ...te, round, smooth and convex after cultivating on [[marine agar]] at 30 °C for 48 h. Cells were catalase and oxidas.. |
| R2A medium                                                              |      4 |        4 | chemical_utilization_object | ...rea. The novel bacterial strain grew optimally in [[R2A medium]] under the following conditions: 0 % (w/v) NaCl, p... |
| marine agar 2216                                                        |      4 |        2 | chemical_utilization_object | ...4T, SYSU T00242T and SYSU T00266T occurred on the [[marine agar 2216]] with pH 8.0 at 37 °C. In addition, the major f |
| 5% sheep blood                                                          |      4 |        1 | chemical_utilization_object | ...e strains grew optimally on tryptic soy agar with [[5% sheep blood]] solid medium and in fastidious bacteria broth. C |
| fastidious bacteria broth                                               |      4 |        1 | chemical_utilization_object | ... soy agar with 5% sheep blood solid medium and in [[fastidious bacteria broth]]. Colonies on tryptic soy agar with 5% |
| brain heart infusion agar supplemented with 5% defibrinated sheep blood |      4 |        1 | chemical_utilization_object | ...700, Y2011T and Y2014 exhibited optimal growth on [[brain heart infusion agar supplemented with 5% defibrinated sheep |
| Reasoner's 2A agar                                                      |      4 |        3 | chemical_utilization_object | ...spectively. Furthermore, this strain grew well on [[Reasoner's 2A agar]] but not on nutrient broth agar or Luria-Bert |
| peptone                                                                 |      4 |        4 | chemical_utilization_object | ...i.e. a mixture of 20 proteinogenic amino acids or [[peptone]]) and thioglycolate as reduced sulphur source. Str...    |
| Reasoner's 2A medium                                                    |      4 |        4 | chemical_utilization_object | ...f Korea. Growth of strain [[EMRT-3T]] was observed in [[Reasoner's 2A medium]] at 10-35 °C (optimum, 25-30 °C) and pH |
| serum                                                                   |      3 |        1 | chemical_utilization_object | ...pneumonia-like organisms medium supplemented with [[serum]] and urea under aerobic and anaerobic atmospheric ...      |
| human milk oligosaccharides                                             |      3 |        1 | chemical_utilization_object | ...ilities for carbohydrate metabolism, particularly [[human milk oligosaccharides]] utilization. Thus, based on these f |
| human milk oligosaccharide                                              |      2 |        1 | chemical_utilization_object | ...latum subsp. puerorum harboured genes involved in [[human milk oligosaccharide]] (HMO) and urea metabolism, consisten |
| Reasoner's 2A                                                           |      2 |        1 | chemical_utilization_object | ... and ASV81T grew optimally at pH 7.0 and 28 °C on [[Reasoner's 2A]]. Strain ASV81T produced capsules, but [[ASV49T]]  |
| de Man-Rogosa-Sharpe agar                                               |      2 |        1 | chemical_utilization_object | ...ere obtained after culturing a strawberry leaf on [[de Man-Rogosa-Sharpe agar]]. Based on 16S rRNA gene and rpoA gene |
| blood agar                                                              |      2 |        2 | chemical_utilization_object | ...onvex and alpha-haemolytic. The bacterium grew on [[blood agar]] but not on Brain Heart Infusion (BHI) and Mueller... |
| Tryptone soya agar (TSA)                                                |      2 |        1 | chemical_utilization_object | ... two strains grew best at 28 °C on the plate with [[Tryptone soya agar (TSA)]]. Cells formed circular, convex, transl |
| sheep blood                                                             |      2 |        1 | chemical_utilization_object | ...cter species by their ability to lyse gelatin and [[sheep blood]] and to assimilate d,l-lactate, along with their i.. |
| MacConkey agar                                                          |      1 |        1 | chemical_utilization_object | ...ed rod. It grew on blood agar, chocolate agar and [[MacConkey agar]] incubated at 37 °C in an aerobic environment aft |
| V8 juice agar                                                           |      1 |        1 | chemical_utilization_object | ...eliospores on potato dextrose agar (PDA) and 10 % [[V8 juice agar]], but teliospore germination with basidia was not  |
| TSB                                                                     |      1 |        1 | chemical_utilization_object | ...Strain [[MA9T]] grew at 10-37 °C and at pH 6.0-9.5 on [[TSB]]. Menaquinone MK-7 was the predominant respiratory...    |
| marine medium                                                           |      1 |        1 | chemical_utilization_object | ...he genus Ruegeria. Growth occurred at 15-37 °C on [[marine medium]] in the presence of 0.5-10 % (w/v) NaCl and at pH  |
| lysogeny broth agar                                                     |      1 |        1 | chemical_utilization_object | ...ain grew on tryptic soy agar, Reasoner's 2A agar, [[lysogeny broth agar]] and nutrient agar. The average nucleotide i |
| milk proteins                                                           |      1 |        1 | chemical_utilization_object | ... tepidum, the new species consistently hydrolyzed [[milk proteins]], a feature implicated in cheese spoilage. Consequ |
| peptone-yeast-glucose broth                                             |      1 |        1 | chemical_utilization_object | ...-product from growth in peptone-yeast extract and [[peptone-yeast-glucose broth]]. The G+C content of DNA from strain |
| peptone-yeast extract                                                   |      1 |        1 | chemical_utilization_object | ...te, was a fermentative end-product from growth in [[peptone-yeast extract]] and peptone-yeast-glucose broth. The G+C  |
| nutrient broth medium                                                   |      1 |        1 | chemical_utilization_object | ...s. The novel bacterial strain grew optimally in a [[nutrient broth medium]] under the following conditions: 1-2% (w/v |
| nitrogen-free growth medium                                             |      1 |        1 | chemical_utilization_object | ...vesicles. N2-fixing vesicles are also produced in [[nitrogen-free growth medium]], in addition to hyphae and sporangi |


### strain (kind=strain) — 5,846 unique labels


_Strain designations are per-paper identifiers; a ranked list is not informative. Composition instead. Base = unique labels in this bucket; the first table is a partition (sums to 100%), the second lists overlapping properties._

| class (mutually exclusive)                                                                | labels        |
|:------------------------------------------------------------------------------------------|:--------------|
| culture-collection accession (DSM/ATCC/JCM/KCTC/CGMCC/…)                                  | 2,225 (38.1%) |
| Genus species / sp. / aff. + designation                                                  | 92 (1.6%)     |
| phrase (`strain …`, `13 isolates of …`, `strain_of`)                                      | 64 (1.1%)     |
| bare code, no whitespace (`LC2-13A`, `zg-579T`)                                           | 2,403 (41.1%) |
| lab/collection prefix + code, prefix not in COLLECTION_RE (`YIM 65594T`, `MCCC 1K00261T`) | 982 (16.8%)   |
| other (with whitespace, no recognised pattern)                                            | 80 (1.4%)     |


| cross-cutting property     | labels        |
|:---------------------------|:--------------|
| type-strain suffix `T`/`ᵀ` | 5,009 (85.7%) |
| contains whitespace        | 3,370 (57.6%) |
| seen in >1 document        | 97 (1.7%)     |


_Examples of 'other':_ `SaT`, `MK-MG`, `MCT`, `MI-GT`, `NCAIM B 02678T`, `MobHT (=DSM 21220T= NBRC 104160T)`, `MobHT`, `MT/JULY 2010T`


_Strain labels seen in >1 document (top 10) — the only ones worth cataloguing:_

| label       |   rows |   n_docs | fields   | example_context                                                                                                          |
|:------------|-------:|---------:|:---------|:-------------------------------------------------------------------------------------------------------------------------|
| B1T         |      4 |        4 | strains  | A novel Gram-positive strain, [[B1T]], was isolated from uranium-contaminated soil. The...; ... on the 16S rRNA gene seq |
| G39T        |      3 |        3 | strains  | ...cifica NZ-96T (99.3%), Qipengyuania profundimaris [[G39T]] (99.1%) and Qipengyuania citrea RE35F/1T (98.8%)....       |
| NEAU-KD1T   |      3 |        3 | strains  | ...3T was most closely related to Mumia xiangluensis [[NEAU-KD1T]] (99.2%) and Mumia quercus NEAU-365T (98.9%). The ...  |
| LNNU 24178T |      3 |        3 | strains  | ...nd showed a high similarity to Luteimonas suaedae [[LNNU 24178T]] (99.01%), Luteimonas endophytica RD2P54T (98.80%).. |
| NJ-26T      |      3 |        3 | strains  | ...grouped strain LB-N7T with Flavobacterium cheniae [[NJ-26T]], Flavobacterium odoriferum HXWNR29T, Flavobacteri...     |
| WM1T        |      3 |        3 | strains  | ...SM 12857T) (98.72%), Lacrimispora saccharolyticum [[WM1T]] (98.29%) and Lacrimispora xylanolytica sy1 (98.22...       |
| SM1973T     |      2 |        2 | strains  | ... sequence similarity) and Spartinivicinus marinus [[SM1973T]] (98.0 % sequence similarity). The predominant cel...; . |
| NZ-96T      |      2 |        2 | strains  | ...ia aerophila GH25T (99.3%), Qipengyuania pacifica [[NZ-96T]] (99.3%), Qipengyuania profundimaris G39T (99.1%) ...; .. |
| DHG64T      |      2 |        2 | strains  | ...nd 98.3 % with the same species Trinickia mobilis [[DHG64T]], respectively, and 98.4 % between themselves. In ...; .. |
| KCTC 25755T |      2 |        2 | strains  | ...a phocaeensis DSM 103159T, Olsenella urininfantis [[KCTC 25755T]] and Olsenella absiana KCTC 25800T with 96.6-96.7%.. |


### unspecified/placeholder — 6 unique labels (top 6)

| label           |   rows |   n_docs | fields                                 | example_context   |
|:----------------|-------:|---------:|:---------------------------------------|:------------------|
| (unspecified)   |      3 |        3 | chemical_utilization_object,study_taxa |                   |
| <unspecified>   |      3 |        3 | study_taxa                             |                   |
| [not specified] |      2 |        2 | study_taxa                             |                   |
| [Not specified] |      2 |        2 | study_taxa                             |                   |
| (not specified) |      2 |        2 | study_taxa                             |                   |
| [unspecified]   |      1 |        1 | study_taxa                             |                   |


### taxon (not in NCBITaxon) — 437 unique labels (top 30)

| label                            |   rows |   n_docs | fields     | example_context                                                                                                          |
|:---------------------------------|-------:|---------:|:-----------|:-------------------------------------------------------------------------------------------------------------------------|
| Rhizobium leguminosarum complex  |      2 |        2 | study_taxa | ...rrs sequences placed all three strains within the [[Rhizobium leguminosarum complex]]. Further phylogeny, based on 1  |
| Yamadazyma koratensis            |      2 |        2 | study_taxa | ...re: PYCC 9797). The MycoBank number is MB 849637. [[Yamadazyma koratensis]] f.a., sp. nov. is proposed for the second |
| Bifidobacterium asteroides group |      2 |        2 | study_taxa | ...that strains F806-1T and F814-1.1 belonged to the [[Bifidobacterium asteroides group]] and were most closely related  |
| Mesorhizobium terrae             |      2 |        2 | study_taxa | ...nalysis, positioned strain IRAMC:0171T closest to [[Mesorhizobium terrae]] KCTC 72278T and 'Mesorhizobium hungaricum' |
| 'Candidatus Methanomethylicia'   |      1 |        1 | study_taxa | ...hat strain LWZ-6T belonged to the candidate class [['Candidatus Methanomethylicia']], which lacks cultivated represen |
| Methanocaldococcus abyssi        |      1 |        1 | study_taxa | ...AT represents a novel species, for which the name [[Methanocaldococcus abyssi]] sp. nov. is proposed. The type strain |
| Methylobacter arcticus           |      1 |        1 | study_taxa | ...within the genus Methylobacter for which the name [[Methylobacter arcticus]] sp. nov. is proposed, with strain G7T (D |
| Microbulbifer jejuensis          |      1 |        1 | study_taxa | ...sp. nov. (2201CG32-9T=KACC 23829T=JCM 37223T) and [[Microbulbifer jejuensis]] sp. nov. (2304DJ12-6T=KACC 23832T=MCCC  |
| Microbulbifer discodermiae       |      1 |        1 | study_taxa | ...olyphasic taxonomic approach, for which the names [[Microbulbifer discodermiae]] sp. nov. (2201CG32-9T=KACC 23829T=JC |
| Microbaculum mangrovi            |      1 |        1 | study_taxa | ...enus Microbaculum, for which the proposed name is [[Microbaculum mangrovi]] FT89T (=MCCC 1K08485T=KCTC 8079T).        |
| Microbacterium salitolerans      |      1 |        1 | study_taxa | ...s of the genus Microbacterium, for which the name [[Microbacterium salitolerans]] sp. nov. is proposed. The type stra |
| Microbacterium luticellae        |      1 |        1 | study_taxa | ...nce supports the proposal of three novel species: [[Microbacterium luticellae]] sp. nov. (type strain YY-01T=GDMCC 1. |
| Microbacterium hydrocarboxydans  |      1 |        1 | study_taxa | ...lassium CCTCC AB 2020140T, followed by 97.5% with [[Microbacterium hydrocarboxydans]] DSM 16089T and 97.3% with Micro |
| Microbacterium daqui             |      1 |        1 | study_taxa | ...type strain YY-02T=GDMCC 1.5103T=KCTC 59479T) and [[Microbacterium daqui]] sp. nov. (type strain YY-03T=GDMCC 1.5104T |
| Microbacterium alcoholitolerans  |      1 |        1 | study_taxa | .... (type strain YY-01T=GDMCC 1.5102T=KCTC 59478T), [[Microbacterium alcoholitolerans]] sp. nov. (type strain YY-02T=GD |
| Metschnikowia sanitii            |      1 |        1 | study_taxa | ...ins represent a novel species, for which the name [[Metschnikowia sanitii]] f.a., sp. nov. is proposed. The holotype  |
| Metschnikowia ratanii            |      1 |        1 | study_taxa | ...nfirming its novelty. The species is described as [[Metschnikowia ratanii]] sp. nov., with strain MCC 10123 as the ex |
| Methylomonas stagni              |      1 |        1 | study_taxa | ...novel species of Methylomonas, for which the name [[Methylomonas stagni]] sp. nov. is proposed. The type strain is CM |
| Methylomonadaceae                |      1 |        1 | study_taxa | ...ol%. Strain G7T represents a member of the family [[Methylomonadaceae]] of the class Gammaproteobacteria. It displaye |
| Methylobacterium synurae         |      1 |        1 | study_taxa | ...of the genus Methylobacterium, for which the name [[Methylobacterium synurae]] sp. nov. is proposed. The type strain  |
| Micromonospora aurantinigra      |      1 |        1 | study_taxa | ...udy revealed that PPF5-17T was closely related to [[Micromonospora aurantinigra]] DSM 44815T in the phylogenomic tree |
| Micromonospora lacuserhaii       |      1 |        1 | study_taxa | ...TC 59310T), representing the desert isolates, and [[Micromonospora lacuserhaii]] sp. nov. (type strain CPCC 205547T=E |
| Micromonospora mangrovicola      |      1 |        1 | study_taxa | .... nov. (type strain=TBRC 19727ᵀ=NBRC 117248ᵀ) and [[Micromonospora mangrovicola]] sp. nov. (type strain=TBRC 19729ᵀ=N |
| Mrakia amundsenii                |      1 |        1 | study_taxa | ...polaris sp. nov. (MycoBank number: MB 852063) and [[Mrakia amundsenii]] sp. nov. (MycoBank number: MB 852064) are pro |
| Mucilaginibacter sediminis       |      1 |        1 | study_taxa | ...reus sp. nov. (AW1-3T=KACC 23848T=JCM 37500T) and [[Mucilaginibacter sediminis]] sp. nov. (AW1-7T=KACC 23849T=JCM 375 |
| Mucilaginibacter metallidurans   |      1 |        1 | study_taxa | ...of the genus Mucilaginibacter, for which the name [[Mucilaginibacter metallidurans]] sp. nov. is proposed. The type s |
| Mucilaginibacter aureus          |      1 |        1 | study_taxa | ...otaxonomic and genomic characteristics, the names [[Mucilaginibacter aureus]] sp. nov. (AW1-3T=KACC 23848T=JCM 37500T |
| Mrakia polaris                   |      1 |        1 | study_taxa | ... novel species within the genus Mrakia. The names [[Mrakia polaris]] sp. nov. (MycoBank number: MB 852063) and Mrakia |
| Micromonospora orduensis S2509T  |      1 |        1 | study_taxa | ...d that isolate STR1-7T is most closely related to [[Micromonospora orduensis S2509T]], and isolate STR1S-6 T forms a  |
| Montipora capitata               |      1 |        1 | study_taxa | ...ed from apparently healthy fragments of the coral [[Montipora capitata]], which were resistant to Vibrio coralliilyti |


### culture-collection accession — 4 unique labels (top 4)

| label          |   rows |   n_docs | fields     | example_context                                                                                                          |
|:---------------|-------:|---------:|:-----------|:-------------------------------------------------------------------------------------------------------------------------|
| KCTC 25794T    |      1 |        1 | study_taxa | ...orci sp. nov. (type strain P01025T=CGMCC 1.18060T=[[KCTC 25794T]]) are proposed.                                      |
| KCTC 25793T    |      1 |        1 | study_taxa | ...orci sp. nov. (type strain P01024T=CGMCC 1.18055T=[[KCTC 25793T]]) and Flintibacter porci sp. nov. (type strain P01.. |
| CGMCC 1.18060T |      1 |        1 | study_taxa | ... Flintibacter porci sp. nov. (type strain P01025T=[[CGMCC 1.18060T]]=KCTC 25794T) are proposed.                       |
| CGMCC 1.18055T |      1 |        1 | study_taxa | ...lavonifractor porci sp. nov. (type strain P01024T=[[CGMCC 1.18055T]]=KCTC 25793T) and Flintibacter porci sp. nov. (ty |


Full catalog written to `reports/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.ungrounded_catalog.tsv`



## 5. Extraction quality (all rows unless stated)


### 5a. False-positive candidates (grounded, but suspicious)


_Precision proxies. Each table is a review queue, not a verdict._


**Synonym matches on 1–2-character labels** (7 unique) — element symbols vs one-letter amino-acid codes collide here:

| label   | kg_name         | grounded_id   |   rows | example_context                                                                                                      |
|:--------|:----------------|:--------------|-------:|:---------------------------------------------------------------------------------------------------------------------|
| H2      | dihydrogen      | CHEBI:18276   |     11 | ...d coccoidal and grew separately on [[H2]]/CO2 and formate. [[Ax23T]] grew on NH4 + and by fixin...; ...ed per ... |
| N2      | dinitrogen      | CHEBI:17997   |      3 | ...x23T]] grew on NH4 + and by fixing [[N2]], but did not grow on NO3 -. The isolate grew at t...                    |
| O2      | dioxygen        | CHEBI:15379   |      2 | ...nomes of both strains encoded high [[O2]] affinity cbb3-type cytochrome c oxidase genes but...                    |
| CO      | carbon monoxide | CHEBI:17245   |      1 | ..., was isolated from the top of the [[co]]vering soil of an active charcoal-burning pile. Th...; ...rom the top... |
| Ca      | calcium atom    | CHEBI:22984   |      1 | ... of sorghum. The taxonomic classifi[[ca]]tion of this novel isolate was investigated by usi...; ...logenetic a... |
| K       | lysine          | CHEBI:25094   |      1 | ...rowth-promoting activities such as [[K]], Ca and Si solubilization, and the production of ...; ...lubilization... |
| Si      | silicon atom    | CHEBI:27573   |      1 | ...e-solubilizing bacterial strain, de[[si]]gnated [[C3T]], was isolated from the rhizosphere of s...; ...rom the... |


**No word overlap between label and kg_name** (87 unique; top 30) — formulas and true synonyms are fine, look for meaning changes:

| label                      | kg_name                        | grounded_id   | match_type   |   rows | example_context                                                                                                      |
|:---------------------------|:-------------------------------|:--------------|:-------------|-------:|:---------------------------------------------------------------------------------------------------------------------|
| thiosulphate               | thiosulfate                    | CHEBI:16094   | synonym      |     18 | ...ated with carbohydrate metabolism, [[thiosulphate]] oxidation and [NiFe]-hydrogenases. Based on compr...          |
| NaCl                       | 1% sodium chloride             | CHEBI:26710   | synonym      |     16 | ...grown at 28 ℃, pH 7.0 and 3% (w/v) [[NaCl]] and possessed Q-10 as the respiratory quinone. Th...                  |
| nitrogen                   | dinitrogen                     | CHEBI:17997   | synonym      |     12 | ...isolates were capable of symbiotic [[nitrogen]] fixation with P. vulgaris. Based on genomic and p...              |
| oxygen                     | dioxygen                       | CHEBI:15379   | synonym      |     11 | ...uding an I.2.C-type catechol 2,3-di[[oxygen]]ase (C23O) gene. The strain was able to degrade be...                |
| sulphate                   | sulfate                        | CHEBI:16189   | synonym      |     10 | ...anaerobically by using nitrate and [[sulphate]] as electron acceptors. The 16S rRNA gene sequence...              |
| aesculin                   | esculin                        | CHEBI:4853    | synonym      |      9 | ...NaCl. Cells were able to hydrolyse [[aesculin]], gelatin, and Tween 20. According to the 16S rRNA...              |
| sulphite                   | sulfite                        | CHEBI:17359   | synonym      |      8 | ...rate as electron acceptors but not [[sulphite]], thiosulphate or iron(III) provided as ferrihydri...              |
| d-glucose                  | D-fructose                     | CHEBI:17634   | synonym      |      7 | ...ly, the strains actively fermented [[d-glucose]] and d-fructose. They exhibited tolerance to high ...             |
| siderophores               | siderophore                    | CHEBI:26672   | synonym      |      6 | ...uction of indole-3-acetic acid and [[siderophores]] and 1-aminocyclopropane-1-carboxylate deaminase a...          |
| 1,2-propanediol            | 1,2-propandiol                 | CHEBI:16997   | synonym      |      5 | ...etabolic signatures concerning the [[1,2-propanediol]] and hydroxycinnamic acid metabolism. The gene ald...; .... |
| Fe(III)                    | ferric iron                    | CHEBI:29034   | synonym      |      5 | ...by hydrogen oxidation coupled with [[Fe(III)]] reduction. Phylogenetic analysis based on 16S rRN...               |
| sulphide                   | sulfide                        | CHEBI:15138   | synonym      |      4 | ...d sulphur compounds (thiosulphate, [[sulphide]], tetrathionate and elemental sulphur) as electron...              |
| ribitol                    | D-Adonitol                     | CHEBI:15963   | synonym      |      4 | ...l as their inability to assimilate [[ribitol]]. Physiological data for S. eucalypti were not ava...               |
| metals                     | metal atom                     | CHEBI:33521   | synonym      |      3 | ...transport systems for amino acids, [[metals]] and phosphate, as well as the ability to synthesi...                |
| molecular oxygen           | dioxygen                       | CHEBI:15379   | synonym      |      3 | ...e, sulphate, elemental sulphur and [[molecular oxygen]] were capable of serving as the sole electron acce...      |
| orthovanadate              | vanadate                       | CHEBI:46442   | synonym      |      3 | ...tellurite, tellurate, selenite and [[orthovanadate]] as terminal electron acceptors. While facultative...; ...... |
| ubiquinone-10              | coenzyme Q10                   | CHEBI:46245   | synonym      |      2 | ...spectively. Both strains contained [[ubiquinone-10]] as the sole respiratory quinone. The major fatty ...         |
| monomethylamine            | methylamine                    | CHEBI:16830   | synonym      |      2 | ...regates. They reduced methanol and [[monomethylamine]] into methane, using H2 as an electron donor. Dime...       |
| carbohydrates              | carbohydrate                   | CHEBI:16646   | synonym      |      2 | ...%). [[AMB_02T]] grew with formate, [[carbohydrates]] and aa, including asparagine, histidine, tryptone...         |
| NH4Cl                      | ammonium chloride              | CHEBI:31206   | synonym      |      2 | ... the species tolerated up to 0.8 M [[NH4Cl]] and 0.5 M NaCl. The major cellular fatty acids we...                 |
| aromatic hydrocarbons      | arene                          | CHEBI:33658   | synonym      |      2 | ...ce of genes for the degradation of [[aromatic hydrocarbons]] suggests a potential role in the bioremediation o... |
| alkanes                    | alkane                         | CHEBI:18310   | synonym      |      2 | ...erial strains which can metabolize [[alkanes]] and polycyclic aromatic hydrocarbons were isolate...; ...rew op... |
| dimethylsulfoniopropionate | S,S-dimethyl-beta-propiothetin | CHEBI:16457   | synonym      |      2 | ...tes but contained genes related to [[dimethylsulfoniopropionate]] catabolism. The results of the polyphasic ta... |
| molecular hydrogen         | dihydrogen                     | CHEBI:18276   | synonym      |      2 | ...naerobic chemolithoautotroph using [[molecular hydrogen]] and elemental sulphur as the sole electron donor....    |
| antibiotics                | antimicrobial agent            | CHEBI:33281   | synonym      |      2 | ...l specialized metabolites, notably [[antibiotics]] and compounds that promote plant growth, as well ...           |
| MgCl2                      | magnesium dichloride           | CHEBI:6636    | synonym      |      2 | ...erved at 40 °C, 3.4 M NaCl, 0.03 M [[MgCl2]] and pH 7.5, while that of strain [[GSL13T]] was at 37...; ... of ... |
| acetol                     | hydroxyacetone                 | CHEBI:27957   | synonym      |      2 | ...h as ethanol, 2-propanol, acetone, [[acetol]] and propane-1,2-diol were used as alternative ele...                |
| propane-1,2-diol           | 1,2-propandiol                 | CHEBI:16997   | synonym      |      2 | ...l, 2-propanol, acetone, acetol and [[propane-1,2-diol]] were used as alternative electron donors and carb...      |
| NH4+                       | ammonium                       | CHEBI:28938   | synonym      |      1 | ... separately on H2/CO2 and formate. [[Ax23T]] grew on [[NH4 +]] and by fixing N2, but did not grow on NO3 -. Th... |
| nitrogenous compounds      | nitrogen molecular entity      | CHEBI:51143   | synonym      |      1 | ...erol, sucrose, maltose and various [[nitrogenous compounds]]. It fermented glucose into acetate, butyrate, lac... |


**Stereo/configuration prefix differs between label and kg_name** (0 unique) — D/L, R/S (incl. `(2R,3S)`), (+)/(−), cis/trans/E/Z, α/β (anomeric *or* positional) flips *within one nomenclature system* change the compound (`l-arabinose`→D-arabinose); D↔R/S are different systems and are not compared (D-lactate ≡ (R)-lactate):

_(none)_


**Stereo prefix on one side only** (8 unique). Generic→specific (`maltose`→D-maltose) is usually acceptable; specific→generic (`d-lactose`→lactose) means the grounding dropped a descriptor the extractor captured — check:

| label                | kg_name                           | grounded_id   | match_type   | direction                                        |   rows | example_context                                                                                                      |
|:---------------------|:----------------------------------|:--------------|:-------------|:-------------------------------------------------|-------:|:---------------------------------------------------------------------------------------------------------------------|
| maltose              | D-maltose                         | CHEBI:17306   | synonym      | label generic → kg specific                      |     18 | ...se, cellobiose, glycerol, sucrose, [[maltose]] and various nitrogenous compounds. It fermented g...               |
| amino acids          | alpha-amino acid                  | CHEBI:33704   | synonym      | label generic → kg specific                      |      8 | ...a broad spectrum of carbohydrates, [[amino acids]] and organic acids, including glucose, cellobiose,...           |
| alanine              | dl-alanine                        | CHEBI:16449   | synonym      | label generic → kg specific                      |      4 | ...cose, rhamnose, arabinose, ribose, [[alanine]], glycine and glycerol. The major fermentation pro...               |
| fructose-6-phosphate | beta-D-fructofuranose 6-phosphate | CHEBI:16084   | synonym      | label generic → kg specific                      |      3 | ...bility among Rothia species to use [[fructose-6-phosphate]] as a sole carbon source. [[RSM42T]] also exhibits ... |
| adonitol             | D-Adonitol                        | CHEBI:15963   | synonym      | label generic → kg specific                      |      1 | ...arbon sources including acetamide, [[adonitol]], amygdalin, l-arabinose, citric acid, glucose, ma...              |
| d-lactose            | lactose                           | CHEBI:17716   | synonym      | label specific → kg generic (descriptor dropped) |      2 | ...atalase or ferment d-trehalose and [[d-lactose]]. Taxon II, represented by 11 isolates, showed the...; ...its ... |
| glycyl-l-proline     | glycine-proline                   | CHEBI:70744   | synonym      | label specific → kg generic (descriptor dropped) |      2 | ...droxy-phenylacetic acid, Tween 40, [[glycyl-l-proline]], d-maltose, d-galactonic acid lactone, α-hydroxy ...      |
| d-melibiose          | melibiose                         | CHEBI:28053   | synonym      | label specific → kg generic (descriptor dropped) |      1 | ...amnose, d-galactose, d-lactose and [[d-melibiose]]. The names Listeria tempestatis sp. nov. and List...           |


**kind / kg_category mismatch** (0 unique):

_(none)_


- Chemical rows whose *label* carries a value/concentration (e.g. `12.5% NaCl`): **398** — value belongs in `chemical_level_type`/`context`, not the term label


### 5b. Label triage: noise vs real terms outside the chemical slot


**Noise: labels that are not real terms** (drop or fix upstream):

| noise type                                              |   rows |   of which grounded | examples                                                                                                                                                                                                           |
|:--------------------------------------------------------|-------:|--------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| value/unit only                                         |      0 |                   0 |                                                                                                                                                                                                                    |
| placeholder                                             |     13 |                   0 | `<unspecified>`, `(unspecified)`, `(not specified)`, `[not specified]`, `[Not specified]`, `[unspecified]`                                                                                                         |
| ≥6 words (verbose label; often value/context leaked in) |     33 |                  26 | `brain heart infusion agar supplemented w`, `0.5 % (w/v; optimum, 0 %) NaCl`, `up to 3.5 % (w/v) NaCl`, `up to 12 % (w/v) NaCl`, `optimum 0% sodium chloride (NaCl, w/v)`, `multi locus sequence type 598 strains` |


- Rows matching ≥1 noise pattern: **46 / 14,982 (0.3%)**


**Real terms in the chemical slot with a different modeling target** — not noise; route, don't drop:

| modeling target                                              |   rows |   of which grounded | examples                                                                                              |
|:-------------------------------------------------------------|-------:|--------------------:|:------------------------------------------------------------------------------------------------------|
| abstract class (model as a class of chemicals)               |     43 |                  14 | `carbon sources`, `aromatic compounds`, `metals`, `fish gut fluid`, `sugars`, `aromatic hydrocarbons` |
| enzyme activity / assay (function or assay → METPO, see §5d) |     51 |                  15 | `catalase`, `oxidase`, `H2/CO2`, `urease`, `indole`, `β-glucuronidase`                                |
| growth medium / complex component (→ MediaDive)              |    147 |                  46 | `yeast extract`, `casein`, `tryptone`, `R2A agar`, `tryptic soy agar`, `nutrient agar`                |


- Rows in a retarget bucket: **240 / 14,982 (1.6%)** — 4 of these also match a noise pattern (verbose media labels)


### 5c. Incomplete or truncated extraction (recall proxies)


_The table has no source text, so these are proxies from `context` snippets; confirm against abstracts._


- Rows per document: min 2, p10 7, median 14, p90 24, max 59

- Documents with ≤3 rows (half of p10; possible failed/empty extraction): **11**, of which 11 contain only strain/taxon rows: 126, 159, 171, 227, 288, 351, 372, 402, 429, 602


**Documents with no rows per field:**

| field                       |   docs_with_0_rows |   pct_docs |
|:----------------------------|-------------------:|-----------:|
| chemical_utilization_object |                389 |       38.9 |
| pH_observation              |                541 |       54.1 |
| strains                     |                  7 |        0.7 |
| study_taxa                  |                  0 |        0   |
| temperature_observation     |                493 |       49.3 |


**Field cue present in other rows' context, but field empty** (strong truncation signal):

| field                       |   docs with cue in context but 0 rows | per cue                                                             | examples                    |
|:----------------------------|--------------------------------------:|:--------------------------------------------------------------------|:----------------------------|
| temperature_observation     |                                     8 | °C:5, temperature:2, ℃:1                                            | 144, 15, 357, 553, 61, 66   |
| pH_observation              |                                    29 | pH:29                                                               | 136, 137, 144, 146, 15, 191 |
| chemical_utilization_object |                                    61 | NaCl:51, ferment:5, glucose:2, utiliz:2, hydroly:2, carbon source:1 | 100, 111, 123, 13, 139, 179 |


- Spans that start/end on whitespace or an opening bracket (span offset error, e.g. `5.0-11.0[[ (optimum pH 7.0]])`): **479 mentions / 530 rows**


- Mentions where the token continues across the `[[…]]` boundary (span locator matched a substring inside a longer word, e.g. `glu[[co]]se`; `]]T` type-strain superscripts ignored): **116 mentions / 148 rows**

| label                     | snippet                                                                         |
|:--------------------------|:--------------------------------------------------------------------------------|
| Dysgonomonas              | hagoides and (iii) Pseudo[[dysgonomonas]] gen. nov. represented by              |
| Coprococcus comes         | Allocoprococcus, as Allo[[coprococcus comes]] gen. nov., comb. nov. Al          |
| Qipengyuania triglochinis | hinis sp. nov. and Alteri[[qipengyuania triglochinis]] sp. nov. are proposed. T |
| Micromonospora            | in a distinct lineage of [[Micromonospora]]ceae, separate from the f            |
| Vibrio                    | ember of the genus Bdello[[vibrio]] based on its 16S rRNA ge                    |
| Fodinibius salipaludis    | e reclassification of Ali[[fodinibius salipaludis]] as Fodinibius salipaludi    |
| Chlamydia                 | The [[Chlamydia]]ceae is a family of stric                                      |
| chitin                    | A novel [[chitin]]olytic bacterium, designa                                     |
| Lactococcus               | for which the name Pseudo[[lactococcus]] is proposed. Three lacti               |
| methylamine               | methanol, methylamine, di[[methylamine]], trimethylamine, dimethy               |
| CO                        | ated from the top of the [[co]]vering soil of an active                         |
| sulfate                   | elemental sulfur and thio[[sulfate]] as alternate electron ac                   |
| Ca                        | m. The taxonomic classifi[[ca]]tion of this novel isolat                        |
| K                         | biogenesis and IAA, cyto[[k]]inin and gamma-aminobutyr                          |
| phosphate                 | he ability to solubilize [[phosphate]]s, stain [[C3T]] exhibite                 |

- Rows with empty `original_spans` (mention not located in text): **314**


### 5d. METPO / vocabulary gaps


**Relationship types used** (23):

| chemical_relationship               |   rows | metpo_id      |
|:------------------------------------|-------:|:--------------|
| has range temperature observation   |    558 | METPO:2000055 |
| has range pH observation            |    555 | METPO:2000503 |
| has optimum temperature observation |    506 | METPO:2000053 |
| uses_for_growth                     |    470 | METPO:2000012 |
| has optimum pH observation          |    407 | METPO:2000501 |
| tolerates                           |    366 | METPO:2000064 |
| produces                            |    332 | METPO:2000202 |
| has range NaCl observation          |    307 | METPO:2000509 |
| does_not_use_for_growth             |    226 | METPO:2000038 |
| uses_as_carbon_source               |    172 | METPO:2000006 |
| requires_for_growth                 |    156 | METPO:2000018 |
| has optimum NaCl observation        |    145 | METPO:2000507 |
| has growth NaCl observation         |    124 | METPO:2000508 |
| hydrolyzes                          |     92 | METPO:2000013 |
| has growth temperature observation  |     80 | METPO:2000054 |
| degrades                            |     72 | METPO:2000007 |
| ferments                            |     65 | METPO:2000011 |
| reduces                             |     64 | METPO:2000017 |
| uses_as_electron_donor              |     54 | METPO:2000009 |
| uses_as_electron_acceptor           |     45 | METPO:2000008 |
| has growth pH observation           |     41 | METPO:2000502 |
| uses_as_energy_source               |     37 | METPO:2000010 |
| oxidizes                            |     12 | METPO:2000016 |


**Relationship types with no METPO id** (0) — candidate new METPO relations:

_(none)_


**Ungrounded enzyme-activity / assay labels** (13 unique; top 30) — these are functions or assays (catalase, urease, β-glucuronidase, H2/CO2), real results reported in the chemical slot; candidates for METPO function/assay classes:

| label                                           |   rows |   n_docs |
|:------------------------------------------------|-------:|---------:|
| oxidase                                         |      9 |        5 |
| H2/CO2                                          |      7 |        5 |
| urease                                          |      6 |        5 |
| 1-aminocyclopropane-1-carboxylic acid deaminase |      2 |        1 |
| catalase activity                               |      2 |        1 |
| β-glucosidase                                   |      2 |        1 |
| β-glucuronidase                                 |      2 |        2 |
| 1-aminocyclopropane-1-carboxylate deaminase     |      1 |        1 |
| nitrogenase                                     |      1 |        1 |
| protease                                        |      1 |        1 |
| urease substrate                                |      1 |        1 |
| α-arabinosidase activity                        |      1 |        1 |
| α-glucosidase                                   |      1 |        1 |


**Ungrounded specific chemicals seen in ≥2 rows** (23) — CHEBI synonym / lexical-index gaps:

| label                                      |   rows |
|:-------------------------------------------|-------:|
| meso-diaminopimelic acid                   |     14 |
| ll-diaminopimelic acid                     |      7 |
| dl-lactate                                 |      7 |
| indole acetic acid                         |      5 |
| methyl-β-d-glucopyranoside                 |      5 |
| carotenoid-type pigments                   |      3 |
| tartaric acid                              |      3 |
| soluble starch                             |      3 |
| p-hydroxy-phenylacetic acid                |      2 |
| poly(butylene succinate-co-adipate) (PBSA) |      2 |
| d,l-lactate                                |      2 |
| phosphatidylethanolamine (PE)              |      2 |
| natural rubber                             |      2 |
| dl-lactic acid                             |      2 |
| actidione                                  |      2 |
| mono- and oligosaccharides                 |      2 |
| methyl-α-d-glucopyranoside                 |      2 |
| amoxicillin-clavulanic acid                |      2 |
| poly(ε-caprolactone)                       |      2 |
| N-acetyl-glucosamine                       |      2 |
| short-chained fatty acids                  |      2 |
| α-hydroxy butyric acid                     |      2 |
| soluble phosphorus                         |      2 |


### 5e. Process and prompt-instruction gaps


_Signals that the extraction agent is not following (or is not given) a consistent instruction. Needs the prompt/schema to confirm. Each bullet names its computation so the count can be re-derived from the table._


- Placeholder spellings: **6** variants (`<unspecified>`, `(unspecified)`, `(not specified)`, `[not specified]`, `[Not specified]`, `[unspecified]`) — prompt should say *omit* rather than emit a placeholder, or fix one spelling _(distinct labels matching the anchored regex `unspecified|not specified|not stated|unknown|none|n/a`)_

- Fields present: ['chemical_utilization_object', 'pH_observation', 'strains', 'study_taxa', 'temperature_observation']; expected-but-absent: none; unexpected: none _(distinct `field` values vs the expected slot list)_

- Labels assigned to more than one `kind` across documents: **15** (inconsistent typing) e.g. `(unspecified)`, `Alt4`, `Burkholderiaceae bacterium PBA`, `CGMCC 1.18055T`, `CGMCC 1.18060T`, `Candida aff. naeodendra/diddensiae Y151`, `Candida sp. GE19S08`, `KCTC 25793T` _(group rows by label, count labels with >1 distinct `kind`)_

- Provenance columns (model/prompt/schema/version): **none** — add them upstream so results can be tied to a run _(column names searched for model/prompt/schema/version/run)_

- Labels differing only by case: **1** (no normalization step) e.g. `[not specified]` _(lowercased labels with >1 distinct original spelling)_


### 5f. Strain name resolution (`Genus species STRAIN`)


- Strain rows: 5,980; resolved: **2,640 (44.1%)**. Rules are applied in priority order (see the script docstring); no document-level fallback.

| rule                     |   rows |   pct |
|:-------------------------|-------:|------:|
| (unresolved)             |   3340 |  55.9 |
| preceding_binomial       |   1558 |  26.1 |
| equivalence              |    563 |   9.4 |
| sp_nov                   |    242 |   4   |
| type_strain_novel        |    207 |   3.5 |
| preceding_binomial_genus |     65 |   1.1 |
| preceding_genus_sp       |      5 |   0.1 |


_One example per rule:_

| label                        | full_scientific_name                      | name_source              |
|:-----------------------------|:------------------------------------------|:-------------------------|
| Gardnerella vaginalis 6119V5 | Gardnerella vaginalis 6119V5              | preceding_binomial       |
| Marseille-Q2328T             | Gardnerella massiliensis Marseille-Q2328T | sp_nov                   |
| DSM 110680T                  | Occallatibacter bavaricus DSM 110680T     | equivalence:JP12T        |
| RSM42T                       | Rothia similimucilaginosa RSM42T          | type_strain_novel        |
| EGH7T                        | Faecalimonas umbilicata EGH7T             | preceding_binomial_genus |
| MTP4                         | Methanosarcina sp. MTP4                   | preceding_genus_sp       |


- (doc, taxon) pairs assigned to >1 distinct strain label: 400 — mostly one strain under several collection accessions; the script prints a QC line for those not `=`-linked.

- Unresolved rows whose mention is an `=`-linked accession (primary designation itself unresolved): 1,667 of 3,340



## 6. Flags


_Each flag is emitted by one of the checks above; its count is defined (and re-derivable) in that section._

- ⚠️ field `strains` is only 0.5% grounded (5,950 ungrounded rows)
- ⚠️ kg_edge_count not populated for all 2,147 rows with match_type=kg_microbe_metpo (edge stats missing for this grounding path, not necessarily orphan nodes)
- ⚠️ 13 rows (all rows, grounded or not) with placeholder labels (unspecified/unknown/NA)
- ⚠️ 7 distinct 1–2-char labels grounded by synonym (check for symbol/amino-acid collisions, e.g. K→lysine)
- ⚠️ 11 docs have ≤3 rows (11 with only strain/taxon rows) — check for failed extraction
- ⚠️ 8 docs mention temperature_observation cues in context but have no temperature_observation row
- ⚠️ 29 docs mention pH_observation cues in context but have no pH_observation row
- ⚠️ 61 docs mention chemical_utilization_object cues in context but have no chemical_utilization_object row
- ⚠️ 479 mentions have a span offset error (leading/trailing whitespace inside [[…]])
- ⚠️ 116 mentions whose span is a substring inside a longer word (locator defect; check original_spans upstream)
- ⚠️ 314 rows have no original_spans (entity asserted without a located mention)
- ⚠️ 15 labels typed inconsistently across docs (>1 kind)
- ⚠️ strain name resolution: 44.1% of strain rows get a Genus species STRAIN name
