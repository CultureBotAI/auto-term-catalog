#!/usr/bin/env python3
"""Expand first-100 chemical rows into name, concentration, and optimum rows."""

from __future__ import annotations

import argparse
import csv
import re
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote


class Level(NamedTuple):
    display: str
    evidence: str


LevelMap = dict[tuple[str, str, str], dict[str, list[Level]]]
METPO_NACL_OPTIMUM = "METPO:2000507"
METPO_NACL_GROWTH = "METPO:2000508"
METPO_NACL_RANGE = "METPO:2000509"


def level_annotations() -> LevelMap:
    """Return source-audited levels keyed by document, subject, and chemical."""
    levels: LevelMap = {}

    def add(
        doc: int,
        subjects: Iterable[str],
        chemical: str,
        concentrations: Iterable[tuple[str, str]] = (),
        optima: Iterable[tuple[str, str]] = (),
    ) -> None:
        for subject in subjects:
            key = (str(doc), subject, chemical)
            if key in levels:
                raise ValueError(f"Duplicate level annotation: {key}")
            levels[key] = {
                "concentration": [Level(*item) for item in concentrations],
                "optimum": [Level(*item) for item in optima],
            }

    add(3, ["Ax23T"], "NaCl", [("3-6% NaCl", "3-6%")], [("optimum 3-4.5% NaCl", "3-4.5%")])
    add(6, ["JP12T"], "NaCl", [("0-0.5% NaCl", "0-0.5%")], [("best 0.25% (w/v) NaCl", "0.25%")])
    add(7, ["P3C3T"], "NaCl", [("0.5% (v/w) NaCl", "0.5%")], [("optimum 0.5% (v/w) NaCl", "0.5%")])
    add(7, ["MAC6T"], "NaCl", [("4.0% (v/w) NaCl", "4.0%")], [("optimum 4.0% (v/w) NaCl", "4.0%")])
    add(15, ["AW1-3T"], "NaCl", [("0.0-0.5% (w/v) NaCl", "0.0-0.5%")])
    add(15, ["AW1-7T"], "NaCl", [("0-0.5% NaCl", "0-0.5%")])
    add(19, ["S174ᵀ", "W118ᵀ"], "NaCl", [("2.0% (w/v) NaCl", "2.0%")], [("optimum 2.0% (w/v) NaCl", "2.0%")])
    add(21, ["BD586T", "BD613T", "BD626T"], "NaCl", [("up to 10% NaCl", "10%")])
    add(41, ["YIM 135249T", "YIM 135347"], "sodium chloride", [("0-9.0% sodium chloride (NaCl, w/v)", "0-9.0%")], [("optimum 0% sodium chloride (NaCl, w/v)", "0%")])
    add(45, ["WXL103", "WXL210T"], "NaCl", [("2.5-8% (w/v) NaCl", "2.5-8%")], [("optimum 3-4% NaCl", "3-4%")])
    add(46, ["LJ205T", "TR449"], "NaCl", [("0.5-1.0% (w/v) NaCl", "0.5-1.0%")], [("optimum 0.5-1.0% (w/v) NaCl", "0.5-1.0%")])
    add(46, ["ZJ450T", "ZJ454", "ZJ70T", "ZJ77"], "NaCl", [("1.0% (w/v) NaCl", "1.0%")], [("optimum 1.0% (w/v) NaCl", "1.0%")])
    add(47, ["G4-2T"], "NaCl", [("0-1% (w/v) NaCl", "0-1%")], [("optimum 0.5% NaCl", "0.5%")])
    add(57, ["MINF-07-Sa-05T"], "NaCl", [("up to 9% (w/v) NaCl", "9%")])
    add(58, ["FAM 1755T"], "NaCl", [("0-5% (w/v) NaCl", "0-5%")])
    add(62, ["CHS3-5T"], "NaCl", [("2.0-11.0% NaCl", "2.0-11.0%")], [("optimum 3.0% NaCl", "3.0%")])
    add(62, ["M-2T"], "NaCl", [("2.0-4.0% NaCl", "2.0-4.0%")], [("optimum 3.0% NaCl", "3.0%")])
    add(63, ["SyP6RT"], "NaCl", [("0.25% (w/v) NaCl", "0.25%")], [("optimum 0.25% (w/v) NaCl", "0.25%")])
    add(64, ["CF4.4T"], "NaCl", [("0-20% (w/v) NaCl", "0-20%")], [("optimum 5% (w/v) NaCl", "5%")])
    add(64, ["KK5.5T"], "NaCl", [("0-20% (w/v) NaCl", "0-20%")], [("optimum 0-2.5% (w/v) NaCl", "0-2.5%")])
    add(65, ["Mg75T"], "NaCl", [("0-3% (w/v) NaCl", "0% to 3%")], [("optimal 0-1% (w/v) NaCl", "0-1%")])
    add(66, ["TMP9T", "TMP25"], "NaCl", [("up to 4.5% NaCl", "4.5%")])
    add(66, ["G.S.17T"], "NaCl", [("up to 3.0% NaCl", "3.0%")])
    add(69, ["REN36T"], "sodium chloride (NaCl)", [("0-2% sodium chloride (NaCl)", "0% to 2%")], [("optimal 0% sodium chloride (NaCl)", "salt concentration of 0%")])
    add(71, ["MAC3T"], "sodium chloride", [("0-15.0% (w/v) sodium chloride (NaCl)", "0-15.0%")])
    add(71, ["MAC8T"], "sodium chloride", [("0-14.0% (w/v) sodium chloride (NaCl)", "0-14.0%")])
    add(75, ["HSL-7T"], "NaCl", [("0-1% (w/v) NaCl", "0-1%")], [("optimum 0.5% NaCl", "0.5%")])
    add(78, ["28AT"], "sodium chloride", [("5-50 g l⁻¹ sodium chloride (NaCl)", "5 to 50 g l⁻¹")], [("optimum 20 g l⁻¹ sodium chloride (NaCl)", "20 g l⁻¹")])
    add(79, ["SD5T"], "sodium chloride", [("1-10% (w/v) sodium chloride", "1-10%")], [("optimum 5% sodium chloride", "5%")])
    add(84, ["DFM-14T"], "NaCl", [("2% (w/v) NaCl", "2%")], [("optimum 2% (w/v) NaCl", "2%")])
    add(88, ["AD34T", "PAK95"], "NaCl", [("1.4-4.8 M NaCl", "1.4-4.8 M")], [("optimum 3.1 M NaCl", "3.1 M")])
    add(90, ["N2T"], "NaCl", [("13-20% (w/v) NaCl", "13-20 %")], [("optimum 15% NaCl", "15%")])
    return levels


def sentence_spans(text: str):
    start = 0
    for match in re.finditer(r"[.!?](?=\s|$)", text):
        end = match.end()
        yield start, text[start:end]
        start = end
        while start < len(text) and text[start].isspace():
            start += 1
    if start < len(text):
        yield start, text[start:]


def is_range_level(display: str) -> bool:
    """Return true for ranges and upper limits, excluding the hyphen in NaCl."""
    return bool(
        re.search(r"\bup to\b", display, re.IGNORECASE)
        or re.search(
            r"\d+(?:\.\d+)?\s*%?\s*(?:-|–|\bto\b)\s*\d+(?:\.\d+)?",
            display,
            re.IGNORECASE,
        )
    )


SALT_LABELS = {"nacl", "sodium chloride", "sodium chloride (nacl)", "sea salt", "salt"}
AMOUNT_PATTERN = re.compile(
    r"(?P<amount>(?:\d+(?:\.\d+)?\s*%\s*(?:\([^)]*\)\s*)?"
    r"(?:-|–|to)\s*\d+(?:\.\d+)?\s*%\s*(?:\([^)]*\))?|"
    r"(?:up to\s+)?\d+(?:\.\d+)?"
    r"(?:\s*(?:-|–|to)\s*\d+(?:\.\d+)?)?\s*"
    r"(?:%\s*(?:\([^)]*\))?|mM\b|M\b|g\s*(?:l|L)[⁻\-−]?1|g\s*/\s*[lL])))",
    re.IGNORECASE,
)


def automatic_levels(row: dict[str, str], text: str) -> dict[str, list[Level]] | None:
    """Extract explicit NaCl/salt growth levels for documents after the audited prefix."""
    if int(row["doc"]) <= 100 or row["label"].casefold() not in SALT_LABELS:
        return None
    chemical_terms = ["NaCl", "sodium chloride", "sea salt"]
    if row["label"].casefold() == "salt":
        chemical_terms.append("salt")
    levels: dict[str, list[Level]] = {"concentration": [], "optimum": []}
    candidates = []
    for _, sentence in sentence_spans(text):
        relevant = re.search(
            r"\b(?:growth|grew|grow|grows|optimum|optimal|optima|tolerat|thrived)\b",
            sentence,
            re.IGNORECASE,
        ) and any(re.search(re.escape(term), sentence, re.IGNORECASE) for term in chemical_terms)
        if relevant:
            candidates.append(sentence)
    explicit = [
        sentence
        for sentence in candidates
        if re.search(re.escape(row["relationship_subject_label"]), sentence, re.IGNORECASE)
    ]
    for sentence in explicit or candidates:
        chemicals = [
            match
            for term in chemical_terms
            for match in re.finditer(re.escape(term), sentence, re.IGNORECASE)
        ]
        if not chemicals:
            continue
        for amount in AMOUNT_PATTERN.finditer(sentence):
            chemical = min(chemicals, key=lambda match: abs(match.start() - amount.start()))
            if abs(chemical.start() - amount.start()) > 80:
                continue
            between = sentence[
                min(amount.end(), chemical.end()) : max(amount.start(), chemical.start())
            ]
            if re.search(r"\b(?!NaCl\b)[A-Za-z0-9]+Cl\b", between, re.IGNORECASE):
                continue
            prefix = sentence[max(0, amount.start() - 28) : amount.start()]
            optimum = bool(
                re.search(
                    r"(?:\(\s*(?:optimum|optimal|optima)[^()]*$|"
                    r"\b(?:optimum|optimal|optima)(?:\s+(?:is|of|at))?[\s,:]*$)",
                    prefix,
                    re.IGNORECASE,
                )
            )
            level_type = "optimum" if optimum else "concentration"
            amount_text = re.sub(r"\s+", " ", amount.group("amount").strip())
            display = (
                f"optimum {amount_text} {row['label']}"
                if optimum
                else f"{amount_text} {row['label']}"
            )
            level = Level(display, amount.group("amount"))
            if level not in levels[level_type]:
                levels[level_type].append(level)
    return levels if any(levels.values()) else None


def evidence(row: dict[str, str], text: str, level: Level, level_type: str):
    base = row["label"]
    chemical_terms = [base]
    if base.casefold() in SALT_LABELS:
        chemical_terms = [
            "NaCl",
            "sodium chloride (NaCl)",
            "sodium chloride",
            "sea salt",
            "salt",
        ]

    candidates = []
    amount_pattern = re.escape(level.evidence)
    if level.evidence[:1].isdigit():
        amount_pattern = rf"(?<![\d.\-]){amount_pattern}(?!\d)"
    for sentence_start, sentence in sentence_spans(text):
        amounts = list(re.finditer(amount_pattern, sentence, re.IGNORECASE))
        chemicals = [
            match
            for term in chemical_terms
            for match in re.finditer(re.escape(term), sentence, re.IGNORECASE)
        ]
        if not amounts or not chemicals:
            continue
        subject_present = bool(
            re.search(re.escape(row["relationship_subject_label"]), sentence, re.IGNORECASE)
        )
        for amount in amounts:
            prior = sentence[max(0, amount.start() - 45) : amount.start()]
            optimum_near = bool(re.search(r"(?i)(?:optimum|optimal|best)", prior))
            chemical = min(chemicals, key=lambda item: abs(item.start() - amount.start()))
            candidates.append(
                (
                    0 if subject_present else 1,
                    0 if optimum_near == (level_type == "optimum") else 1,
                    abs(chemical.start() - amount.start()),
                    sentence_start,
                    amount.start(),
                    chemical.start(),
                    sentence,
                    amount,
                    chemical,
                )
            )
    if not candidates:
        raise ValueError(
            f"Cannot locate evidence for doc {row['doc']} "
            f"{row['relationship_subject_label']!r} {level.display!r}"
        )

    *_, sentence, amount, chemical = min(candidates, key=lambda item: item[:6])
    sentence_start = min(candidates, key=lambda item: item[:6])[3]
    local_spans = sorted(
        {(amount.start(), amount.end()), (chemical.start(), chemical.end())}
    )
    if len(local_spans) == 2 and local_spans[1][0] <= local_spans[0][1]:
        local_spans = [(local_spans[0][0], max(local_spans[0][1], local_spans[1][1]))]
    absolute_spans = [
        (sentence_start + start, sentence_start + end) for start, end in local_spans
    ]
    highlighted = sentence
    for start, end in reversed(local_spans):
        highlighted = highlighted[:start] + "[[" + highlighted[start:end] + "]]" + highlighted[end:]
    return (
        "; ".join(f"{start}:{end}" for start, end in absolute_spans),
        highlighted,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--documents-dir", required=True, type=Path)
    parser.add_argument("--nodes", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    with args.input.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        existing_fields = reader.fieldnames or []
        existing_rows = list(reader)
    added_fields = {"chemical_level_type", "chemical_base_label", "chebi_label"}
    old_fields = [field for field in existing_fields if field not in added_fields]
    original_rows = [
        {field: row.get(field, "") for field in old_fields}
        for row in existing_rows
        if row.get("chemical_level_type", "") not in {"concentration", "optimum"}
    ]
    insert_at = old_fields.index("chemical_relationship") + 1
    new_fields = old_fields[:insert_at] + [
        "chemical_level_type",
        "chemical_base_label",
        "chebi_label",
    ] + old_fields[insert_at:]

    annotations = level_annotations()
    wanted_metpo = {
        METPO_NACL_OPTIMUM,
        METPO_NACL_GROWTH,
        METPO_NACL_RANGE,
    }
    metpo_labels = {}
    with args.nodes.open(newline="", encoding="utf-8") as stream:
        for node in csv.DictReader(stream, delimiter="\t"):
            if node.get("id") in wanted_metpo:
                metpo_labels[node["id"]] = node.get("name", "")
    missing_metpo = wanted_metpo - set(metpo_labels)
    if missing_metpo or any(not label for label in metpo_labels.values()):
        raise ValueError(
            "Required METPO terms are missing canonical KG-Microbe labels: "
            + ", ".join(sorted(missing_metpo))
        )
    salt_template = next(
        row for row in original_rows if row["grounded_id"] == "CHEBI:26710"
    )
    texts = {
        path.name: path.read_text(encoding="utf-8")
        for path in args.documents_dir.glob("*.txt")
    }

    matched = set()
    generated_level_keys = set()
    output_rows = []
    for row in original_rows:
        relationship = row["field"] == "chemical_utilization_object"
        row["chemical_level_type"] = "chemical_name" if relationship else ""
        row["chemical_base_label"] = row["label"] if relationship else ""
        row["chebi_label"] = row["label"] if row["grounded_id"].startswith("CHEBI:") else ""
        key = (row["doc"], row["relationship_subject_label"], row["label"])
        annotation = annotations.get(key)
        if annotation is None:
            annotation = automatic_levels(row, texts[row["source_file"]])
        if annotation:
            matched.add(key)
            if row["label"].casefold() in {"nacl", "sodium chloride", "sodium chloride (nacl)"}:
                candidates = [item for item in row["grounded_ids"].split("|") if item]
                row["grounded_id"] = "CHEBI:26710"
                row["grounded_ids"] = "|".join(dict.fromkeys(["CHEBI:26710", *candidates]))
                for field in ("kg_category", "kg_edge_count", "kg_edge_evidence"):
                    row[field] = salt_template[field]
                row["match_type"] = row["match_type"] or "synonym"
            row["kg_name"] = row["label"]
            row["chebi_label"] = row["label"]
        output_rows.append(row)

        if not annotation:
            continue
        for level_type in ("concentration", "optimum"):
            for level in annotation[level_type]:
                variant = dict(row)
                variant["entity_id"] = f"AUTO:{quote(level.display)}"
                variant["label"] = level.display
                variant["chemical_level_type"] = level_type
                variant["chemical_base_label"] = row["label"]
                variant["chebi_label"] = level.display
                variant["kg_name"] = level.display
                variant["match_type"] = f"context_{level_type}"
                if level_type == "optimum":
                    metpo_id = METPO_NACL_OPTIMUM
                elif is_range_level(level.display):
                    metpo_id = METPO_NACL_RANGE
                else:
                    metpo_id = METPO_NACL_GROWTH
                variant["chemical_relationship"] = metpo_labels[metpo_id]
                variant["chemical_relationship_id"] = metpo_id
                variant["chemical_relationship_label"] = metpo_labels[metpo_id]
                variant["chemical_relationship_match_type"] = "kg_microbe_metpo"
                variant["original_spans"], variant["context"] = evidence(
                    row, texts[row["source_file"]], level, level_type
                )
                generated_key = (
                    row["doc"],
                    row["relationship_subject_id"],
                    level_type,
                    level.display.casefold(),
                )
                if generated_key in generated_level_keys:
                    continue
                generated_level_keys.add(generated_key)
                output_rows.append(variant)

    missing = set(annotations) - matched
    if missing:
        raise ValueError(f"{len(missing)} annotated rows were not found: {sorted(missing)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=new_fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Original rows: {len(original_rows)}")
    print(f"Expanded rows: {len(output_rows)}")
    print(f"Annotated chemical relationships: {len(matched)}")


if __name__ == "__main__":
    main()
