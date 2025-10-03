import yaml
import pandas as pd
import re
import json
from typing import Any, Dict, List

# ---------- helpers (unchanged structure) ----------
def iter_yaml_docs(path: str):
    with open(path, "r", encoding="utf-8") as f:
        for doc in yaml.safe_load_all(f):
            if isinstance(doc, dict):
                yield doc

def find_entities_like(obj: Any) -> List[Dict[str, Any]]:
    entities: List[Dict[str, Any]] = []
    keys = ["named_entities", "named-entities", "entities", "ner", "annotations", "extractions"]
    if isinstance(obj, dict):
        for k in keys:
            if k in obj:
                block = obj[k]
                if isinstance(block, list):
                    entities.extend([x for x in block if isinstance(x, dict)])
                elif isinstance(block, dict):
                    entities.extend([v for v in block.values() if isinstance(v, dict)])
        for v in obj.values():
            entities.extend(find_entities_like(v))
    elif isinstance(obj, list):
        if obj and all(isinstance(x, dict) for x in obj):
            entities.extend(obj)
    return entities

def normalize_spans(spans: Any) -> str:
    if spans is None: return ""
    if isinstance(spans, str): return spans
    if isinstance(spans, list):
        parts = []
        for s in spans:
            if isinstance(s, dict):
                for k in ("text","span","value","original","surface","string"):
                    if s.get(k): parts.append(str(s[k])); break
            else:
                parts.append(str(s))
        return "; ".join(parts)
    if isinstance(spans, dict):
        return spans.get("text") or spans.get("span") or spans.get("value") or json.dumps(spans, ensure_ascii=False)
    return str(spans)

def extract_microbe_names(val: Any) -> List[str]:
    names: List[str] = []
    if val is None: return names
    if isinstance(val, (list, tuple, set)):
        for x in val:
            if isinstance(x, dict):
                for k in ("name","label","taxon","scientific_name","value","id"):
                    if x.get(k): names.append(str(x[k])); break
            else:
                names.append(str(x))
    elif isinstance(val, dict):
        for k in ("name","label","taxon","scientific_name","value","id"):
            if val.get(k): names.append(str(val[k])); break
    elif isinstance(val, str):
        names.append(val)
    return [n.strip() for n in names if n]

def entity_contains_auto(ent: Dict[str, Any]) -> bool:
    def walk(x: Any) -> bool:
        if isinstance(x, dict):
            return any(walk(v) for v in x.values())
        if isinstance(x, (list, tuple, set)):
            return any(walk(v) for v in x)
        try:
            return "auto:" in str(x).lower()
        except Exception:
            return False
    return walk(ent)

# ---------- category inference ----------
BINOMIAL_RE = re.compile(r"\b([A-Z][a-z]+)\s([a-z\-]{2,})\b")
STRAIN_KEYS = re.compile(r"\b(DSM|ATCC|JCM|NRRL|NCIMB|KCTC|CGMCC|NBRC|BCRC|LMG|NCTC|KACC)\b")
STRAIN_WORDS = re.compile(r"\b(strain|isolate|type strain|culture)\b", re.I)
STRAIN_CODE  = re.compile(r"\b([A-Z]{1,3}\d{2,}[A-Za-z0-9\-]*)\b")
CHEM_KEYWORDS = re.compile(
    r"\b(glucose|fructose|sucrose|lactose|xylose|arabinose|cellulose|xylan|lignin|glycerol|acetate|propionate|butyrate|"
    r"lactate|pyruvate|succinate|citrate|ethanol|methanol|phenol|benzene|toluene|xylene|sulfate|sulphate|sulfite|sulphite|"
    r"nitrate|nitrite|ammonia|ammonium|chloroform|formate|formic acid|acetic acid|citric acid|NaCl|KCl|MgCl2|H2|H2S|CO2|CH4|"
    r"urea|heme|amino acid|amino acids)\b", re.I
)

def _concat_text(ent: Dict[str, Any]) -> str:
    parts = []
    for k in ("label", "original_spans", "spans", "mentions"):
        v = ent.get(k)
        if v is None: continue
        parts.append(normalize_spans(v) if k != "label" else (v if isinstance(v, str) else str(v)))
    return " | ".join(p for p in parts if p)

def infer_categories(ent: Dict[str, Any]) -> Dict[str, int]:
    """
    Always returns integers 0 or 1 for each category.
    Defaults to 0, flips to 1 if explicit fields or heuristics match.
    """
    text = _concat_text(ent)

    # start at 0 for every category
    flag_taxa  = 0
    flag_strain = 0
    flag_chem  = 0

    # explicit fields can flip to 1
    if ent.get("study_taxa"): flag_taxa = 1
    if ent.get("strains"): flag_strain = 1
    if ent.get("chemicals_mentioned") or ent.get("chemicals"): flag_chem = 1

    # heuristics only flip if still 0
    if not flag_taxa:
        if BINOMIAL_RE.search(text) or re.search(r"\b(genus|species|family|order|phylum|class|microbe|bacterium|archaea|fungus|yeast)\b", text, re.I):
            flag_taxa = 1
    if not flag_strain:
        if STRAIN_KEYS.search(text) or STRAIN_WORDS.search(text) or STRAIN_CODE.search(text):
            flag_strain = 1
    if not flag_chem:
        if CHEM_KEYWORDS.search(text):
            flag_chem = 1

    return {"study_taxa": flag_taxa, "strains": flag_strain, "chemicals_mentioned": flag_chem}

# ---------- main ----------
def build_auto_tables(yaml_path: str) -> pd.DataFrame:
    # collect entities
    all_entities = []
    for doc in iter_yaml_docs(yaml_path):
        all_entities.extend(find_entities_like(doc))

    # keep only AUTO entries
    auto_entities = [e for e in all_entities if entity_contains_auto(e)]

    # build rows
    rows = []
    for e in auto_entities:
        microbes = extract_microbe_names(e.get("study_taxa")) or ["UNKNOWN_MICROBE"]
        flags = infer_categories(e)  # <-- guarantees 0/1
        for microbe in microbes:
            rows.append({
                "microbe": microbe,
                "id": e.get("id") or e.get("_id") or e.get("uuid"),
                "label": e.get("label"),
                "original_spans": normalize_spans(e.get("original_spans") or e.get("spans") or e.get("mentions")),
                "study_taxa": flags["study_taxa"],
                "strains": flags["strains"],
                "chemicals_mentioned": flags["chemicals_mentioned"],
            })

    df = pd.DataFrame(rows)

    if not df.empty:
        # Drop rows with no identifying fields at all
        df = df.dropna(how="all", subset=["id","label","original_spans"])

        # Deduplicate fully
        df = df.drop_duplicates(subset=[
            "microbe","id","label","original_spans","study_taxa","strains","chemicals_mentioned"
        ])

        # FINAL GUARANTEE: every flag is an explicit int 0/1
        for col in ["study_taxa","strains","chemicals_mentioned"]:
            df[col] = df[col].fillna(0).astype(int)

    return df

# ---------- run ----------
if __name__ == "__main__":
    # set your YAML file path here (or wire up argparse)
    path = "/Users/lukewang/Downloads/chemical_utilization_cborg_gpt5_20250819_113045.yaml"
    df = build_auto_tables(path)
    print(df.head(15))
    df.to_csv("auto_terms_by_microbe_clean_inferred.csv", index=False)
    print("Saved auto_terms_by_microbe_clean_inferred.csv")
