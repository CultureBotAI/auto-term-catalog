# Extraction table review: `chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.tsv`

- Size on disk: 7.4 MB
- Rows: 14,982
- Columns: 28


## 1. Structure

### Columns

| column                           |   non_empty | pct_non_empty   |   n_unique | example                                                      |
|:---------------------------------|------------:|:----------------|-----------:|:-------------------------------------------------------------|
| doc                              |       14982 | 100.0%          |       1000 | 1                                                            |
| source_file                      |       14982 | 100.0%          |       1000 | 00001-41779015-abstract.txt                                  |
| pmid                             |       14982 | 100.0%          |       1000 | 41779015                                                     |
| field                            |       14982 | 100.0%          |          5 | strains                                                      |
| kind                             |       14982 | 100.0%          |          4 | strain                                                       |
| entity_id                        |       14982 | 100.0%          |      11006 | AUTO:Gardnerella%20vaginalis%201400E                         |
| label                            |       14982 | 100.0%          |      11006 | Gardnerella vaginalis 1400E                                  |
| original_spans                   |       14668 | 97.9%           |      12321 | 1040:1067                                                    |
| context                          |       14668 | 97.9%           |      13803 | ...T, Marseille-QA0894T and Marseille-Q2328T against [[Gardn |
| relationship_subject_id          |        4886 | 32.6%           |       1061 | AUTO:Ax23T                                                   |
| relationship_subject_label       |        4886 | 32.6%           |       1061 | Ax23T                                                        |
| chemical_relationship            |        4886 | 32.6%           |         24 | produces                                                     |
| chemical_level_type              |        4886 | 32.6%           |          6 | chemical_name                                                |
| chemical_base_label              |        4886 | 32.6%           |        557 | CH4                                                          |
| chebi_label                      |        2352 | 15.7%           |        671 | CH4                                                          |
| chemicals_utilized               |       14982 | 100.0%          |          2 | 0                                                            |
| study_taxa                       |       14982 | 100.0%          |          2 | 0                                                            |
| strains                          |       14982 | 100.0%          |          2 | 1                                                            |
| chemical_relationship_id         |        4886 | 32.6%           |         24 | METPO:2000202                                                |
| chemical_relationship_label      |        4886 | 32.6%           |         24 | produces                                                     |
| chemical_relationship_match_type |        4886 | 32.6%           |          3 | label                                                        |
| grounded_id                      |        8263 | 55.2%           |       3744 | NCBITaxon:698956                                             |
| grounded_ids                     |        8263 | 55.2%           |       3755 | NCBITaxon:698956                                             |
| kg_name                          |        8263 | 55.2%           |       4050 | Gardnerella vaginalis 1400E                                  |
| kg_category                      |        8263 | 55.2%           |         14 | biolink:OrganismTaxon                                        |
| match_type                       |        8263 | 55.2%           |          6 | name                                                         |
| kg_edge_count                    |       14982 | 100.0%          |        329 | 9                                                            |
| kg_edge_evidence                 |        6116 | 40.8%           |       3433 | out:biolink:subclass_of:NCBITaxon:2702|out:biolink:has_pheno |


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

| kg_category                                                            |   rows |
|:-----------------------------------------------------------------------|-------:|
| (empty)                                                                |   6719 |
| biolink:OrganismTaxon                                                  |   3689 |
| biolink:OntologyClass                                                  |   2147 |
| biolink:ChemicalEntity|biolink:ChemicalSubstance|biolink:SmallMolecule |   1209 |
| biolink:ChemicalEntity|biolink:SmallMolecule                           |    856 |
| biolink:SmallMolecule                                                  |    110 |
| biolink:ChemicalEntity                                                 |     90 |
| biolink:ChemicalEntity|biolink:Macromolecule                           |     79 |
| biolink:ChemicalSubstance|biolink:SmallMolecule                        |     62 |
| biolink:ChemicalEntity|biolink:ChemicalSubstance|biolink:Macromolecule |     14 |
| biolink:ChemicalRole|biolink:ChemicalSubstance                         |      3 |
| biolink:ChemicalSubstance|biolink:Macromolecule                        |      2 |
| biolink:AnatomicalEntity|biolink:ChemicalEntity                        |      1 |
| biolink:ChemicalRole|biolink:SmallMolecule                             |      1 |


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

| label                      | grounded_id   | kg_category                                                            | match_type       |   rows |
|:---------------------------|:--------------|:-----------------------------------------------------------------------|:-----------------|-------:|
| NaCl                       | CHEBI:26710   | biolink:ChemicalEntity|biolink:ChemicalSubstance|biolink:SmallMolecule | synonym          |    367 |
| pH optimum 7.0             | METPO:1001013 | biolink:OntologyClass                                                  | kg_microbe_metpo |    143 |
| temperature optimum 30 °C  | METPO:1001001 | biolink:OntologyClass                                                  | kg_microbe_metpo |    128 |
| glucose                    | CHEBI:17234   | biolink:ChemicalEntity|biolink:SmallMolecule                           | name             |     77 |
| temperature optimum 37 °C  | METPO:1001001 | biolink:OntologyClass                                                  | kg_microbe_metpo |     74 |
| temperature optimum 28 °C  | METPO:1001001 | biolink:OntologyClass                                                  | kg_microbe_metpo |     73 |
| temperature optimum 25 °C  | METPO:1001001 | biolink:OntologyClass                                                  | kg_microbe_metpo |     51 |
| pH range 6.0-9.0           | METPO:1001015 | biolink:OntologyClass                                                  | kg_microbe_metpo |     50 |
| pH optimum 8.0             | METPO:1001013 | biolink:OntologyClass                                                  | kg_microbe_metpo |     36 |
| temperature range 15-37 °C | METPO:1001003 | biolink:OntologyClass                                                  | kg_microbe_metpo |     36 |
| acetate                    | CHEBI:30089   | biolink:ChemicalEntity|biolink:SmallMolecule                           | name             |     34 |
| temperature range 10-40 °C | METPO:1001003 | biolink:OntologyClass                                                  | kg_microbe_metpo |     32 |
| nitrate                    | CHEBI:17632   | biolink:ChemicalEntity|biolink:ChemicalSubstance|biolink:SmallMolecule | name             |     32 |
| pH range 6.0-10.0          | METPO:1001015 | biolink:OntologyClass                                                  | kg_microbe_metpo |     32 |
| methanol                   | CHEBI:17790   | biolink:ChemicalEntity|biolink:ChemicalSubstance|biolink:SmallMolecule | name             |     30 |
| ribose                     | CHEBI:33942   | biolink:ChemicalEntity|biolink:SmallMolecule                           | name             |     28 |
| pH range 6.0-8.0           | METPO:1001015 | biolink:OntologyClass                                                  | kg_microbe_metpo |     27 |
| temperature range 15-40 °C | METPO:1001003 | biolink:OntologyClass                                                  | kg_microbe_metpo |     27 |
| temperature range 20-40 °C | METPO:1001003 | biolink:OntologyClass                                                  | kg_microbe_metpo |     25 |
| pH optimum 7.0-8.0         | METPO:1001013 | biolink:OntologyClass                                                  | kg_microbe_metpo |     24 |
| pH optimum 6.0             | METPO:1001013 | biolink:OntologyClass                                                  | kg_microbe_metpo |     24 |
| pH optimum 7               | METPO:1001013 | biolink:OntologyClass                                                  | kg_microbe_metpo |     23 |
| methane                    | CHEBI:16183   | biolink:ChemicalEntity|biolink:ChemicalSubstance|biolink:SmallMolecule | name             |     22 |
| temperature range 4-37 °C  | METPO:1001003 | biolink:OntologyClass                                                  | kg_microbe_metpo |     22 |
| formate                    | CHEBI:15740   | biolink:ChemicalEntity|biolink:SmallMolecule                           | name             |     21 |
| galactose                  | CHEBI:28260   | biolink:ChemicalEntity|biolink:SmallMolecule                           | name             |     20 |
| temperature growth 30 °C   | METPO:1001002 | biolink:OntologyClass                                                  | kg_microbe_metpo |     20 |
| pH range 5.0-8.0           | METPO:1001015 | biolink:OntologyClass                                                  | kg_microbe_metpo |     19 |
| pH range 7.0-8.0           | METPO:1001015 | biolink:OntologyClass                                                  | kg_microbe_metpo |     19 |
| starch                     | CHEBI:28017   | biolink:ChemicalEntity|biolink:Macromolecule                           | name             |     19 |



## 3. QC


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


- Rows sharing the same mention key ['doc', 'field', 'entity_id', 'original_spans']: **1,634**

  - These differ only in relationship columns (context, relationship_subject_id, relationship_subject_label, chemical_relationship, chemical_relationship_id, chemical_relationship_label): one row per (mention, relationship) — expected, not a defect.

- Fully identical rows: **0**



## 4. Ungrounded-term catalog


- Ungrounded rows: 6,719; unique labels: 6,454


### By bucket

| bucket                    |   rows |
|:--------------------------|-------:|
| strain designation        |   5957 |
| taxon (not in NCBITaxon)  |    435 |
| chemical (not in CHEBI)   |    187 |
| growth medium / component |     89 |
| enzyme / assay            |     29 |
| unspecified/placeholder   |     22 |


### chemical (not in CHEBI) — 112 unique labels (top 30)

| label                                      |   rows |   n_docs | fields                      | example_context                                                                                                          |
|:-------------------------------------------|-------:|---------:|:----------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| meso-diaminopimelic acid                   |     14 |       10 | chemical_utilization_object | ... 0-5 % NaCl and whole-cell hydrolysates contained [[meso-diaminopimelic acid]] as the cell-wall diamino acid. On the  |
| H2/CO2                                     |      7 |        5 | chemical_utilization_object | .... Dimethylamine, trimethylamine and methanethiol, [[H2/CO2]], formate, acetate, pyruvate, lactate and glucose ...     |
| dl-lactate                                 |      7 |        5 | chemical_utilization_object | ...-xylose, d-ribose, glycerol, ribitol, d-mannitol, [[dl-lactate]] and d-gluconate. Based on phylogenetic and phenot... |
| ll-diaminopimelic acid                     |      7 |        4 | chemical_utilization_object | ...Whole-cell hydrolysates of strain [[BI20T]] contained [[ll-diaminopimelic acid]] and whole-cell sugars contained gluc |
| carbon sources                             |      6 |        2 | chemical_utilization_object | ...xhibited high auxotrophy, being unable to use all [[carbon sources]] tested, likely due to genome reduction (4.6 Mbp) |
| indole acetic acid                         |      5 |        3 | chemical_utilization_object | ...ding enzymes for synthesizing plant hormones like [[indole acetic acid]] and gibberellic acid. Experimental validatio |
| methyl-β-d-glucopyranoside                 |      5 |        1 | chemical_utilization_object | ...f α-glucosidase activity and acid production from [[methyl-β-d-glucopyranoside]] and maltose. The two novel species c |
| soluble starch                             |      3 |        2 | chemical_utilization_object | ...rate utilization encompassed cellobiose, sucrose, [[soluble starch]], casein, glucose, xylan, ethanol, ribose, yeast  |
| carotenoid-type pigments                   |      3 |        2 | chemical_utilization_object | ...timally in 2% NaCl). Strain [[SZ-1-7T]] could produce [[carotenoid-type pigments]]. Strain 4WD22T grew from 20 to 45  |
| tartaric acid                              |      3 |        1 | chemical_utilization_object |                                                                                                                          |
| human milk oligosaccharides                |      3 |        1 | chemical_utilization_object | ...ilities for carbohydrate metabolism, particularly [[human milk oligosaccharides]] utilization. Thus, based on these f |
| actidione                                  |      2 |        1 | chemical_utilization_object | ...owing the growth on streptomycin thallous acetate [[actidione]] medium was considered to result from a modificati...  |
| metal ions                                 |      2 |        1 | chemical_utilization_object | ...problems and restoring environments polluted with [[metal ions]] and/or benzoate. On the basis of the results of m... |
| methyl-α-d-glucopyranoside                 |      2 |        1 | chemical_utilization_object | ...urease, β-glucosidase, assimilation of inulin and [[methyl-α-d-glucopyranoside]] and degradation of casein. Compared  |
| fish gut fluid                             |      2 |        2 | chemical_utilization_object | ...[[BP47G]] grew on agar medium containing mannitol and [[fish gut fluid]] as the sole carbon sources. Clear colonies o |
| multiple antibiotics                       |      2 |        1 | chemical_utilization_object | ... and ZM25. Strains ZM22T and [[Y6]] were resistant to [[multiple antibiotics]], whereas strains ZM23T, ZM24 and ZM25  |
| human milk oligosaccharide                 |      2 |        1 | chemical_utilization_object | ...latum subsp. puerorum harboured genes involved in [[human milk oligosaccharide]] (HMO) and urea metabolism, consisten |
| dl-lactic acid                             |      2 |        2 | chemical_utilization_object | ...strain exhibited heterofermentative production of [[dl-lactic acid]] from glucose. Optimal growth was observed at 25- |
| mono- and oligosaccharides                 |      2 |        1 | chemical_utilization_object | ...y on a wide range of organic substrates including [[mono- and oligosaccharides]], amino acids and short-chained fatty |
| d,l-lactate                                |      2 |        1 | chemical_utilization_object | ...to lyse gelatin and sheep blood and to assimilate [[d,l-lactate]], along with their inability to acidify d-glucose .. |
| coral mucus                                |      2 |        1 | chemical_utilization_object | ... analysis indicated these two strains may utilize [[coral mucus]] or chitin. Based on above characteristics, these .. |
| natural rubber                             |      2 |        1 | chemical_utilization_object | ...1T, were isolated using mineral salts medium with [[natural rubber]] as the sole carbon source. Polyphasic taxonomy p |
| amoxicillin-clavulanic acid                |      2 |        1 | chemical_utilization_object | ...dicated that [[CDC186T]] and CDC192 were resistant to [[amoxicillin-clavulanic acid]] and tigecycline. On the basis o |
| N-acetyl-glucosamine                       |      2 |        1 | chemical_utilization_object | ...itrate and utilized various carbohydrates but not [[N-acetyl-glucosamine]]; they differed in sorbitol assimilation. T |
| Reasoner's 2A                              |      2 |        1 | chemical_utilization_object | ... and ASV81T grew optimally at pH 7.0 and 28 °C on [[Reasoner's 2A]]. Strain ASV81T produced capsules, but [[ASV49T]]  |
| p-hydroxy-phenylacetic acid                |      2 |        1 | chemical_utilization_object | ...l-d-glucosamine, maltose, adipate, phenylacetate, [[p-hydroxy-phenylacetic acid]], Tween 40, glycyl-l-proline, d-malt |
| poly(ε-caprolactone)                       |      2 |        1 | chemical_utilization_object | ...s, poly(butylene succinate-co-adipate) (PBSA) and [[poly(ε-caprolactone)]]. Phylogenetic analyses based on the 16S rR |
| short-chained fatty acids                  |      2 |        1 | chemical_utilization_object | ...uding mono- and oligosaccharides, amino acids and [[short-chained fatty acids]]. MK-8 was identified as the major res |
| poly(butylene succinate-co-adipate) (PBSA) |      2 |        1 | chemical_utilization_object | ...ed the ability to degrade biodegradable plastics, [[poly(butylene succinate-co-adipate) (PBSA)]] and poly(ε-caprolact |
| soluble phosphorus                         |      2 |        1 | chemical_utilization_object | ...s and produce siderophores, for which the maximum [[soluble phosphorus]] concentrations could reach 510.03±7.11 and 5 |


### enzyme / assay — 12 unique labels (top 12)

| label                                           |   rows |   n_docs | fields                      | example_context                                                                                                          |
|:------------------------------------------------|-------:|---------:|:----------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| oxidase                                         |      9 |        5 | chemical_utilization_object | ...polyphasic approach. The cells were catalase- and [[oxidase]]-positive and rod-shaped. The five novel strains w...    |
| urease                                          |      6 |        5 | chemical_utilization_object | ...closely related species by the (delayed) positive [[urease]] reaction in the API20NE test and by weak growth o...     |
| catalase activity                               |      2 |        1 | chemical_utilization_object | ... bacterial isolates showed positive reactions for [[catalase activity]], Tween 80 hydrolysis and tellurite reduction. |
| 1-aminocyclopropane-1-carboxylic acid deaminase |      2 |        1 | chemical_utilization_object | ... of producing indole acetic acid, siderophore and [[1-aminocyclopropane-1-carboxylic acid deaminase]], and also showe |
| β-glucuronidase                                 |      2 |        2 | chemical_utilization_object | ... and trehalose, as well as negative reactions for [[β-glucuronidase]], mannose, inositol and glycerol. Genotypic and  |
| β-glucosidase                                   |      2 |        1 | chemical_utilization_object | ... with respect to their ability to produce urease, [[β-glucosidase]], assimilation of inulin and methyl-α-d-glucopyran |
| nitrogenase                                     |      1 |        1 | chemical_utilization_object | ...of methanogene. The nif cluster, encompassing the [[nitrogenase]] genes, was found in every N2-fixing strain within.. |
| α-glucosidase                                   |      1 |        1 | chemical_utilization_object | ...re differentiated by their positive reactions for [[α-glucosidase]], l-arabinose and trehalose, as well as negative r |
| urease substrate                                |      1 |        1 | chemical_utilization_object |                                                                                                                          |
| protease                                        |      1 |        1 | chemical_utilization_object | A novel [[protease]]-producing and cellulose-degrading actinobacterium...                                                |
| trypticase                                      |      1 |        1 | chemical_utilization_object | ...ng on complex substrates, such as casamino acids, [[trypticase]], tryptone, yeast and beef extracts. No growth at ... |
| 1-aminocyclopropane-1-carboxylate deaminase     |      1 |        1 | chemical_utilization_object | ...cytokinin and auxin plant hormones and to produce [[1-aminocyclopropane-1-carboxylate deaminase]]. The DNA G+C conten |


### growth medium / component — 40 unique labels (top 30)

| label                                                                   |   rows |   n_docs | fields                      | example_context                                                                                                          |
|:------------------------------------------------------------------------|-------:|---------:|:----------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| R2A agar                                                                |      6 |        4 | chemical_utilization_object | ... performed on these strains. Both strains grow on [[R2A agar]] forming mucous, bright yellow colonies, developin...   |
| tryptic soy agar                                                        |      6 |        3 | chemical_utilization_object | ...rization. Strain [[MMS21-DH1MA12T]] grew optimally in [[tryptic soy agar]], forming yellow-coloured, convex and smoot |
| nutrient agar                                                           |      6 |        3 | chemical_utilization_object | ... required for growth. Best growth was observed on [[nutrient agar]] or marine agar media. The strains contained dipho |
| marine agar                                                             |      5 |        3 | chemical_utilization_object | ...te, round, smooth and convex after cultivating on [[marine agar]] at 30 °C for 48 h. Cells were catalase and oxidas.. |
| Reasoner's 2A agar                                                      |      4 |        3 | chemical_utilization_object | ...spectively. Furthermore, this strain grew well on [[Reasoner's 2A agar]] but not on nutrient broth agar or Luria-Bert |
| fastidious bacteria broth                                               |      4 |        1 | chemical_utilization_object | ... soy agar with 5% sheep blood solid medium and in [[fastidious bacteria broth]]. Colonies on tryptic soy agar with 5% |
| Reasoner's 2A medium                                                    |      4 |        4 | chemical_utilization_object | ...f Korea. Growth of strain [[EMRT-3T]] was observed in [[Reasoner's 2A medium]] at 10-35 °C (optimum, 25-30 °C) and pH |
| brain heart infusion agar supplemented with 5% defibrinated sheep blood |      4 |        1 | chemical_utilization_object | ...700, Y2011T and Y2014 exhibited optimal growth on [[brain heart infusion agar supplemented with 5% defibrinated sheep |
| marine agar 2216                                                        |      4 |        2 | chemical_utilization_object | ...4T, SYSU T00242T and SYSU T00266T occurred on the [[marine agar 2216]] with pH 8.0 at 37 °C. In addition, the major f |
| 5% sheep blood                                                          |      4 |        1 | chemical_utilization_object | ...e strains grew optimally on tryptic soy agar with [[5% sheep blood]] solid medium and in fastidious bacteria broth. C |
| R2A medium                                                              |      4 |        4 | chemical_utilization_object | ...rea. The novel bacterial strain grew optimally in [[R2A medium]] under the following conditions: 0 % (w/v) NaCl, p... |
| peptone                                                                 |      4 |        4 | chemical_utilization_object | ...i.e. a mixture of 20 proteinogenic amino acids or [[peptone]]) and thioglycolate as reduced sulphur source. Str...    |
| serum                                                                   |      3 |        1 | chemical_utilization_object | ...pneumonia-like organisms medium supplemented with [[serum]] and urea under aerobic and anaerobic atmospheric ...      |
| blood agar                                                              |      2 |        2 | chemical_utilization_object | ...onvex and alpha-haemolytic. The bacterium grew on [[blood agar]] but not on Brain Heart Infusion (BHI) and Mueller... |
| de Man-Rogosa-Sharpe agar                                               |      2 |        1 | chemical_utilization_object | ...ere obtained after culturing a strawberry leaf on [[de Man-Rogosa-Sharpe agar]]. Based on 16S rRNA gene and rpoA gene |
| Tryptone soya agar (TSA)                                                |      2 |        1 | chemical_utilization_object | ... two strains grew best at 28 °C on the plate with [[Tryptone soya agar (TSA)]]. Cells formed circular, convex, transl |
| sheep blood                                                             |      2 |        1 | chemical_utilization_object | ...cter species by their ability to lyse gelatin and [[sheep blood]] and to assimilate d,l-lactate, along with their i.. |
| MacConkey agar                                                          |      1 |        1 | chemical_utilization_object | ...ed rod. It grew on blood agar, chocolate agar and [[MacConkey agar]] incubated at 37 °C in an aerobic environment aft |
| V8 juice agar                                                           |      1 |        1 | chemical_utilization_object | ...eliospores on potato dextrose agar (PDA) and 10 % [[V8 juice agar]], but teliospore germination with basidia was not  |
| marine medium                                                           |      1 |        1 | chemical_utilization_object | ...he genus Ruegeria. Growth occurred at 15-37 °C on [[marine medium]] in the presence of 0.5-10 % (w/v) NaCl and at pH  |
| lysogeny broth agar                                                     |      1 |        1 | chemical_utilization_object | ...ain grew on tryptic soy agar, Reasoner's 2A agar, [[lysogeny broth agar]] and nutrient agar. The average nucleotide i |
| peptone-yeast-glucose broth                                             |      1 |        1 | chemical_utilization_object | ...-product from growth in peptone-yeast extract and [[peptone-yeast-glucose broth]]. The G+C content of DNA from strain |
| peptone-yeast extract                                                   |      1 |        1 | chemical_utilization_object | ...te, was a fermentative end-product from growth in [[peptone-yeast extract]] and peptone-yeast-glucose broth. The G+C  |
| nutrient broth medium                                                   |      1 |        1 | chemical_utilization_object | ...s. The novel bacterial strain grew optimally in a [[nutrient broth medium]] under the following conditions: 1-2% (w/v |
| nitrogen-free growth medium                                             |      1 |        1 | chemical_utilization_object | ...vesicles. N2-fixing vesicles are also produced in [[nitrogen-free growth medium]], in addition to hyphae and sporangi |
| chocolate agar                                                          |      1 |        1 | chemical_utilization_object | ...ative, motile, curved rod. It grew on blood agar, [[chocolate agar]] and MacConkey agar incubated at 37 °C in an aero |
| brain-heart infusion medium                                             |      1 |        1 | chemical_utilization_object | ...hite coloured colonies with a convex elevation on [[brain-heart infusion medium]] supplemented with 0.1 % sodium taur |
| brain heart infusion medium                                             |      1 |        1 | chemical_utilization_object |                                                                                                                          |
| glucose-yeast extract agar                                              |      1 |        1 | chemical_utilization_object | ...by its ability to grow at 30 °C and on 50 % (w/v) [[glucose-yeast extract agar]].                                     |
| defibrinated sheep blood                                                |      1 |        1 | chemical_utilization_object | ...w optimally on [[brain heart infusion agar]] with 5 % [[defibrinated sheep blood]] plate at 30 °C, pH 7.0 and with 0. |


### strain designation — 5,848 unique labels (top 10)

| label          |   rows |   n_docs | fields             | example_context                                                                                                          |
|:---------------|-------:|---------:|:-------------------|:-------------------------------------------------------------------------------------------------------------------------|
| B1T            |      4 |        4 | strains            | A novel Gram-positive strain, [[B1T]], was isolated from uranium-contaminated soil. The...; ... on the 16S rRNA gene seq |
| G39T           |      3 |        3 | strains            | ...cifica NZ-96T (99.3%), Qipengyuania profundimaris [[G39T]] (99.1%) and Qipengyuania citrea RE35F/1T (98.8%)....       |
| LNNU 24178T    |      3 |        3 | strains            | ...nd showed a high similarity to Luteimonas suaedae [[LNNU 24178T]] (99.01%), Luteimonas endophytica RD2P54T (98.80%).. |
| NJ-26T         |      3 |        3 | strains            | ...grouped strain LB-N7T with Flavobacterium cheniae [[NJ-26T]], Flavobacterium odoriferum HXWNR29T, Flavobacteri...     |
| WM1T           |      3 |        3 | strains            | ...SM 12857T) (98.72%), Lacrimispora saccharolyticum [[WM1T]] (98.29%) and Lacrimispora xylanolytica sy1 (98.22...       |
| NEAU-KD1T      |      3 |        3 | strains            | ...3T was most closely related to Mumia xiangluensis [[NEAU-KD1T]] (99.2%) and Mumia quercus NEAU-365T (98.9%). The ...  |
| SM1973T        |      2 |        2 | strains            | ... sequence similarity) and Spartinivicinus marinus [[SM1973T]] (98.0 % sequence similarity). The predominant cel...; . |
| CGMCC 1.18060T |      2 |        1 | strains,study_taxa | ... Flintibacter porci sp. nov. (type strain P01025T=[[CGMCC 1.18060T]]=KCTC 25794T) are proposed.                       |
| 7R016T         |      2 |        2 | strains            | ...bidurans KC 17012T and Streptomyces spinosisporus [[7R016T]]. Nearly 100% average nucleotide identity (ANI) an...     |
| 85T            |      2 |        2 | strains            | ...e similarity (97.7%) with Fulvimarina endophytica [[85T]], while strain MAC8T shared 97.9% sequence similar...        |


### unspecified/placeholder — 15 unique labels (top 15)

| label                            |   rows |   n_docs | fields                                 | example_context                                                                                                          |
|:---------------------------------|-------:|---------:|:---------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|
| <unspecified>                    |      3 |        3 | study_taxa                             |                                                                                                                          |
| (unspecified)                    |      3 |        3 | chemical_utilization_object,study_taxa |                                                                                                                          |
| [not specified]                  |      2 |        2 | study_taxa                             |                                                                                                                          |
| [Not specified]                  |      2 |        2 | study_taxa                             |                                                                                                                          |
| (not specified)                  |      2 |        2 | study_taxa                             |                                                                                                                          |
| [unspecified]                    |      1 |        1 | study_taxa                             |                                                                                                                          |
| [unspecified microbial taxon]    |      1 |        1 | study_taxa                             |                                                                                                                          |
| Zongyanglinia marina             |      1 |        1 | study_taxa                             | ...by the similarities of 98.6 %, 98.0 and 98.0 % to [[Zongyanglinia marina]] DSW4-44T, Parasedimentitalea marina W43T a |
| Starmerella fangiana             |      1 |        1 | study_taxa                             | ...cies in the genus Starmerella, for which the name [[Starmerella fangiana]] sp. nov. is proposed. The holotype strain  |
| <unspecified chemical entity>    |      1 |        1 | chemical_utilization_object            |                                                                                                                          |
| 6 isolates of P. honggalleglyana |      1 |        1 | strains                                |                                                                                                                          |
| 31 isolates of P. acerina        |      1 |        1 | strains                                |                                                                                                                          |
| 20 isolates of P. alpina         |      1 |        1 | strains                                |                                                                                                                          |
| Joostella marina                 |      1 |        1 | study_taxa                             | ...M28999T = KCTC 92588T). Moreover, the transfer of [[Joostella marina]] to the genus Galbibacter as Galbibacter orient |
| Jiella marina                    |      1 |        1 | study_taxa                             | ...as a novel species within the Jiella genus, named [[Jiella marina]] sp. nov., with the type strain designated as LLJ8 |


### taxon (not in NCBITaxon) — 431 unique labels (top 30)

| label                            |   rows |   n_docs | fields     | example_context                                                                                                          |
|:---------------------------------|-------:|---------:|:-----------|:-------------------------------------------------------------------------------------------------------------------------|
| Rhizobium leguminosarum complex  |      2 |        2 | study_taxa | ...rrs sequences placed all three strains within the [[Rhizobium leguminosarum complex]]. Further phylogeny, based on 1  |
| Mesorhizobium terrae             |      2 |        2 | study_taxa | ...nalysis, positioned strain IRAMC:0171T closest to [[Mesorhizobium terrae]] KCTC 72278T and 'Mesorhizobium hungaricum' |
| Bifidobacterium asteroides group |      2 |        2 | study_taxa | ...that strains F806-1T and F814-1.1 belonged to the [[Bifidobacterium asteroides group]] and were most closely related  |
| Yamadazyma koratensis            |      2 |        2 | study_taxa | ...re: PYCC 9797). The MycoBank number is MB 849637. [[Yamadazyma koratensis]] f.a., sp. nov. is proposed for the second |
| 'Candidatus Methanomethylicia'   |      1 |        1 | study_taxa | ...hat strain LWZ-6T belonged to the candidate class [['Candidatus Methanomethylicia']], which lacks cultivated represen |
| Methanosarcina sediminis         |      1 |        1 | study_taxa | ...hanosarcina, Methanosarcina mangrovi sp. nov. and [[Methanosarcina sediminis]] sp. nov., are proposed. The type strai |
| Methylomonadaceae                |      1 |        1 | study_taxa | ...ol%. Strain G7T represents a member of the family [[Methylomonadaceae]] of the class Gammaproteobacteria. It displaye |
| Micromonospora mangrovicola      |      1 |        1 | study_taxa | .... nov. (type strain=TBRC 19727ᵀ=NBRC 117248ᵀ) and [[Micromonospora mangrovicola]] sp. nov. (type strain=TBRC 19729ᵀ=N |
| Micromonospora lacuserhaii       |      1 |        1 | study_taxa | ...TC 59310T), representing the desert isolates, and [[Micromonospora lacuserhaii]] sp. nov. (type strain CPCC 205547T=E |
| Micromonospora aurantinigra      |      1 |        1 | study_taxa | ...udy revealed that PPF5-17T was closely related to [[Micromonospora aurantinigra]] DSM 44815T in the phylogenomic tree |
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
| Micromonospora orduensis S2509T  |      1 |        1 | study_taxa | ...d that isolate STR1-7T is most closely related to [[Micromonospora orduensis S2509T]], and isolate STR1S-6 T forms a  |
| Micromonospora psammae           |      1 |        1 | study_taxa | ... these findings, two novel species were proposed: [[Micromonospora psammae]] sp. nov. (type strain CPCC 205556T=MS104 |
| Microvirga medicaginis           |      1 |        1 | study_taxa | ...proposed a novel species in the genus Microvirga, [[Microvirga medicaginis]] sp. nov., the type strain of which was G |
| Muricauda parva                  |      1 |        1 | study_taxa | ...algicola AsT0115T, Muricauda flava DSM 22638T and [[Muricauda parva]] SW169T with 96.5, 96.4, 96.3, 95.8 and 95.6 % 1 |
| Muricauda flava                  |      1 |        1 | study_taxa | ...giicola 2012CJ35-5T, Muricauda algicola AsT0115T, [[Muricauda flava]] DSM 22638T and Muricauda parva SW169T with 96.5 |
| Mumia spirodelae                 |      1 |        1 | study_taxa | ...el species of the genus Mumia, for which the name [[Mumia spirodelae]] sp. nov. is proposed. The type strain is DW29H |
| Mucilaginibacter sediminis       |      1 |        1 | study_taxa | ...reus sp. nov. (AW1-3T=KACC 23848T=JCM 37500T) and [[Mucilaginibacter sediminis]] sp. nov. (AW1-7T=KACC 23849T=JCM 375 |
| Mucilaginibacter metallidurans   |      1 |        1 | study_taxa | ...of the genus Mucilaginibacter, for which the name [[Mucilaginibacter metallidurans]] sp. nov. is proposed. The type s |
| Mucilaginibacter aureus          |      1 |        1 | study_taxa | ...otaxonomic and genomic characteristics, the names [[Mucilaginibacter aureus]] sp. nov. (AW1-3T=KACC 23848T=JCM 37500T |
| Minisyncoccus archaeophilus      |      1 |        1 | study_taxa | ...taxa for the characterized species, including Ca. [[Minisyncoccus archaeophilus]] and the corresponding family Ca. Mi |


Full catalog written to `reports/chemical_utilization_ijsem_first1000_cborg_gpt41mini_merged_kg_grounded_20260824.ungrounded_catalog.tsv`



## 5. Flags

- ⚠️ field `strains` is only 0.5% grounded (5,950 ungrounded rows)
- ⚠️ 2,147 grounded rows have kg_edge_count=0 (grounded to a node with no edges)
- ⚠️ 97 rows with placeholder labels (unspecified/unknown/NA)
