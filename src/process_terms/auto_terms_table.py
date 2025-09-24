import yaml
import pandas as pd
import json
from typing import Any, Dict, List

# ---------- helpers (same as before) ----------
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
        return spans.get("text") or spans.get("span") or spans.get("value") or json.dumps(spans)
    return str(spans)

def extract_microbe_names(val: Any) -> List[str]:
    names: List[str] = []
    if val is None: return names
    if isinstance(val, (list, tuple, set)):
        for x in val:
            if isinstance(x, dict):
                for k in ("name","label","taxon","scientific_name","value","id"):
                    if x.get(k): names.append(str(x[k])); break
            else: names.append(str(x))
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
        try: return "auto:" in str(x).lower()
        except: return False
    return walk(ent)

# ---------- main ----------
def build_auto_tables(yaml_path: str) -> pd.DataFrame:
    # collect entities
    all_entities = []
    for doc in iter_yaml_docs(yaml_path):
        all_entities.extend(find_entities_like(doc))

    # filter to AUTO
    auto_entities = [e for e in all_entities if entity_contains_auto(e)]

    # build rows
    rows = []
    for e in auto_entities:
        microbes = extract_microbe_names(e.get("study_taxa")) or ["UNKNOWN_MICROBE"]
        for microbe in microbes:
            rows.append({
                "microbe": microbe,
                "id": e.get("id"),
                "label": e.get("label"),
                "original_spans": normalize_spans(e.get("original_spans") or e.get("spans") or e.get("mentions")),
                "study_taxa": 1 if e.get("study_taxa") else 0,
                "strains": 1 if e.get("strains") else 0,
                "chemicals_mentioned": 1 if (e.get("chemicals_mentioned") or e.get("chemicals")) else 0,
            })

    df = pd.DataFrame(rows)

    # drop rows where id, label, and original_spans are all empty
    df = df.dropna(how="all", subset=["id", "label", "original_spans"])

    # remove exact duplicates
    df = df.drop_duplicates(subset=["microbe","id","label","original_spans",
                                    "study_taxa","strains","chemicals_mentioned"])

    return df

# Example usage
if __name__ == "__main__":
    path = "/Users/lukewang/Downloads/chemical_utilization_cborg_gpt5_20250819_113045.yaml"
    df = build_auto_tables(path)
    print(df.head())
    df.to_csv("auto_terms_by_microbe_clean.csv", index=False)
    print("Saved auto_terms_by_microbe_clean.csv")
