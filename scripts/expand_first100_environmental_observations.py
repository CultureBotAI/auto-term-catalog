#!/usr/bin/env python3
"""Add source-grounded temperature and pH observations to an IJSEM TSV."""

from __future__ import annotations

import argparse
import csv
import re
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple
from urllib.parse import quote


class Observation(NamedTuple):
    display: str
    evidence: str


Annotations = dict[tuple[str, str, str], dict[str, list[Observation]]]

METPO = {
    ("temperature", "optimum"): ("METPO:2000053", "METPO:1001001"),
    ("temperature", "growth"): ("METPO:2000054", "METPO:1001002"),
    ("temperature", "range"): ("METPO:2000055", "METPO:1001003"),
    ("pH", "optimum"): ("METPO:2000501", "METPO:1001013"),
    ("pH", "growth"): ("METPO:2000502", "METPO:1001012"),
    ("pH", "range"): ("METPO:2000503", "METPO:1001015"),
}


def annotations() -> Annotations:
    data: Annotations = {}

    def add(
        doc: int,
        subjects: Iterable[str],
        parameter: str,
        ranges: Iterable[tuple[str, str]] = (),
        optima: Iterable[tuple[str, str]] = (),
        growth: Iterable[tuple[str, str]] = (),
    ) -> None:
        for subject in subjects:
            key = (str(doc), subject, parameter)
            if key in data:
                raise ValueError(f"Duplicate environmental annotation: {key}")
            data[key] = {
                "range": [Observation(*item) for item in ranges],
                "optimum": [Observation(*item) for item in optima],
                "growth": [Observation(*item) for item in growth],
            }

    add(3, ["Ax23T"], "temperature", [("temperature range 33-75 °C", "33 to 75 °C")], [("temperature optimum 73 °C", "optimum 73 °C")])
    add(3, ["Ax23T"], "pH", [("pH range 4.0-9.0", "pH 4.0-9.0")], [("pH optimum 6.0-8.0", "optimum 6.0-8.0")])
    add(6, ["JP12T"], "temperature", [("temperature range 4-40 °C", "4-40 °C")], [("temperature optimum 24-30 °C", "best between 24 and 30 °C")])
    add(6, ["JP12T"], "pH", [("pH range 3.7-6.0", "pH values of 3.7-6.0")], [("pH optimum 4.1-5.6", "best between 4.1 and 5.6")])
    add(7, ["P3C3T"], "temperature", optima=[("temperature optimum 35 °C", "35 °C")])
    add(7, ["P3C3T"], "pH", optima=[("pH optimum 6.0", "pH 6.0")])
    add(7, ["MAC6T"], "temperature", optima=[("temperature optimum 30 °C", "30 °C")])
    add(7, ["MAC6T"], "pH", optima=[("pH optimum 6.0", "pH 6.0")])
    add(10, ["BV2-CT"], "temperature", [("temperature range 35-50 °C", "range 35-50 °C")], [("temperature optimum 45 °C", "45 °C")])
    add(10, ["BV2-CT"], "pH", [("pH range 5.5-9.0", "range pH 5.5-9.0")], [("pH optimum 7.2", "pH 7.2")])
    add(13, ["MT/JULY 2010T"], "temperature", [("temperature range 20-45 °C", "20-45 °C")])
    add(13, ["MT/JULY 2010T"], "pH", [("pH range 5.0-7.0", "pH 5.0-7.0")])
    add(19, ["S174ᵀ", "W118ᵀ"], "temperature", optima=[("temperature optimum 25 °C", "25 °C")])
    add(19, ["S174ᵀ", "W118ᵀ"], "pH", optima=[("pH optimum 8.0", "pH 8.0")])
    add(21, ["BD586T", "BD613T", "BD626T"], "temperature", growth=[("growth temperature 35 °C", "35 °C")])
    add(21, ["BD586T", "BD613T", "BD626T"], "pH", ranges=[("pH range 7-9", "pH 7-9")])
    add(22, ["meth-B3ᵀ"], "temperature", optima=[("temperature optimum 35 °C", "35 °C")])
    add(22, ["meth-B3ᵀ"], "pH", optima=[("pH optimum 7.0", "pH 7.0")])
    add(23, ["SB112T"], "temperature", ranges=[("temperature range 10-45 °C", "10-45 °C")])
    add(23, ["SB112T"], "pH", ranges=[("pH range 6.0-12.0", "pH 6.0-12.0")])
    add(24, ["G7T"], "temperature", ranges=[("temperature range 4-21 °C", "4 to 21 °C")])
    add(24, ["G7T"], "pH", growth=[("growth pH 6.8", "pH 6.8")])
    add(29, ["A7.4T"], "temperature", ranges=[("temperature range 10-35 °C", "10-35 °C")])
    add(29, ["A7.4T"], "pH", ranges=[("pH range 6.0-9.0", "pH 6.0-9.0")])
    add(32, ["483ᵀ", "357ᵀ"], "temperature", [("temperature range 10-40 °C", "10-40 °C")], [("temperature optimum 30 °C", "optimum, 30 °C")])
    add(32, ["483ᵀ", "357ᵀ"], "pH", [("pH range 5.5-9.0", "pH 5.5-9.0")], [("pH optimum 6.0", "optimum, pH 6.0")])
    add(33, ["HK31-PT"], "temperature", [("temperature range 20-35 °C", "20-35 °C")], [("temperature optimum 30-35 °C", "optimum, 30-35 °C")])
    add(33, ["HK31-PT"], "pH", [("pH range 7-9", "pH 7-9")], [("pH optimum 8", "optimum, 8")])
    add(41, ["YIM 135249T", "YIM 135347"], "temperature", [("temperature range 10-35 °C", "10-35 °C")], [("temperature optimum 28 °C", "optimum 28 °C")])
    add(41, ["YIM 135249T", "YIM 135347"], "pH", [("pH range 4.0-9.0", "pH 4.0-9.0")], [("pH optimum 7.0", "optimum pH 7.0")])
    add(43, ["sgz302541T", "sgz302542", "sgz302552T", "sgz302555"], "temperature", optima=[("temperature optimum 30 °C", "30 °C")])
    add(43, ["sgz302541T", "sgz302542", "sgz302552T", "sgz302555"], "pH", optima=[("pH optimum 7.0", "pH 7.0")])
    add(44, ["E16BAT", "E15BD"], "temperature", optima=[("temperature optimum 37 °C", "37 °C")])
    add(44, ["E16BAT", "E15BD"], "pH", optima=[("pH optimum 9", "pH 9")])
    add(45, ["WXL103", "WXL210T"], "temperature", [("temperature range 10-42 °C", "10-42 °C")], [("temperature optimum 28 °C", "optimum 28 °C")])
    add(45, ["WXL103", "WXL210T"], "pH", [("pH range 7.0-9.0", "pH 7.0-9.0")], [("pH optimum 7.0-8.0", "optimum 7.0-8.0")])
    add(46, ["LJ205T", "TR449", "ZJ450T", "ZJ454", "ZJ70T", "ZJ77"], "temperature", optima=[("temperature optimum 28.0 °C", "28.0 °C")])
    add(46, ["LJ205T", "TR449"], "pH", optima=[("pH optimum 9.0", "pH 9.0")])
    add(46, ["ZJ450T", "ZJ454", "ZJ70T", "ZJ77"], "pH", optima=[("pH optimum 7.0", "pH 7.0")])
    add(47, ["G4-2T"], "temperature", [("temperature range 20-50 °C", "20-50 °C")], [("temperature optimum 37 °C", "optimum, 37 °C")])
    add(47, ["G4-2T"], "pH", [("pH range 6.0-9.0", "pH 6.0-9.0")], [("pH optimum 8.0", "optimum, 8.0")])
    add(49, ["IAD-21T"], "temperature", ranges=[("temperature range 15-37 °C", "15 to 37 °C")])
    add(49, ["IAD-21T"], "pH", ranges=[("pH range 6.0-7.4", "6.0 to 7.4")])
    add(50, ["LBK-2T"], "temperature", [("temperature range 20-50 °C", "20-50℃")], [("temperature optimum 37 °C", "optimum: 37 ℃")])
    add(50, ["LBK-2T"], "pH", [("pH range 3.5-8.0", "pH 3.5-8.0")], [("pH optimum 7.0", "optimum: pH 7.0")])
    add(52, ["TRA05-7T"], "temperature", [("temperature range 4-40 °C", "4-40 °C")], [("temperature optimum 28 °C", "optimum 28 °C")])
    add(52, ["TRA05-7T"], "pH", [("pH range 7-11", "pH 7-11")], [("pH optimum 7", "optimum pH 7")])
    add(57, ["MINF-07-Sa-05T"], "temperature", ranges=[("temperature range 4-40 °C", "4-40 °C")])
    add(57, ["MINF-07-Sa-05T"], "pH", ranges=[("pH range 6.0-10.0", "pH 6.0-10.0")])
    add(58, ["FAM 1755T"], "temperature", ranges=[("temperature range 20-40 °C", "20-40 °C")])
    add(62, ["CHS3-5T"], "temperature", [("temperature range 10-40 °C", "10-40 °C")], [("temperature optimum 30 °C", "30 °C")])
    add(62, ["CHS3-5T"], "pH", [("pH range 4.0-10.0", "pH 4.0-10.0")], [("pH optimum 7.0", "pH 7.0")])
    add(62, ["M-2T"], "temperature", [("temperature range 15-40 °C", "15-40 °C")], [("temperature optimum 30 °C", "30 °C")])
    add(62, ["M-2T"], "pH", [("pH range 6.0-9.0", "pH 6.0-9.0")], [("pH optimum 7.0", "pH 7.0")])
    add(63, ["SyP6RT"], "temperature", optima=[("temperature optimum 30 °C", "30 °C")])
    add(63, ["SyP6RT"], "pH", optima=[("pH optimum 7.0", "pH 7.0")])
    add(64, ["CF4.4T", "KK5.5T"], "temperature", ranges=[("temperature range 4-25 °C", "4 and 25 °C")])
    add(64, ["CF4.4T"], "pH", [("pH range 6-11", "pH 6-11")], [("pH optimum 9-10", "pH 9-10")])
    add(64, ["KK5.5T"], "pH", [("pH range 6-10", "pH 6-10")], [("pH optimum 8-9", "pH 8-9")])
    add(65, ["Mg75T"], "temperature", [("temperature range 15-40 °C", "15-40 °C")], [("temperature optimum 28-30 °C", "28-30 °C")])
    add(65, ["Mg75T"], "pH", [("pH range 5.0-10.0", "between 5.0 and 10.0")], [("pH optimum 7.0", "pH 7.0")])
    add(67, ["M3-11T", "M6-14T"], "temperature", optima=[("temperature optimum 28 °C", "28 °C")])
    add(67, ["M3-11T", "M6-14T"], "pH", optima=[("pH optimum 7.0", "pH 7.0")])
    add(69, ["REN36T"], "temperature", [("temperature range 20-45 °C", "range from 20 to 45 °C")], [("temperature optimum 37 °C", "temperature of 37 °C")])
    add(69, ["REN36T"], "pH", [("pH range 4.0-8.0", "range from pH 4.0 to 8.0")], [("pH optimum 6.0", "pH of 6.0")])
    add(71, ["MAC3T", "MAC8T"], "temperature", ranges=[("temperature range 4-40 °C", "4-40 °C")])
    add(71, ["MAC3T", "MAC8T"], "pH", ranges=[("pH range 4.0-10.0", "pH 4.0-10.0")])
    add(75, ["HSL-7T"], "temperature", [("temperature range 15-37 °C", "15-37 °C")], [("temperature optimum 20 °C", "optimum at 20 °C")])
    add(75, ["HSL-7T"], "pH", [("pH range 6.0-10.0", "pH 6.0-10.0")], [("pH optimum 7.0", "optimum at 7.0")])
    add(78, ["28AT"], "temperature", [("temperature range 50-85 °C", "50 and 85 °C")], [("temperature optimum 75-80 °C", "optimum: 75-80 °C")])
    add(78, ["28AT"], "pH", [("pH range 5.3-7.0", "between 5.3 and 7.0")], [("pH optimum 6.5", "optimum: pH 6.5")])
    add(79, ["SD5T"], "temperature", [("temperature range 4-42 °C", "4 and 42 °C")], [("temperature optimum 37 °C", "optimum 37 °C")])
    add(79, ["SD5T"], "pH", [("pH range 6.5-9.0", "between 6.5 and 9.0")], [("pH optimum 7.0", "optimum 7.0")])
    add(80, ["HB62T"], "temperature", [("temperature range 16-40 °C", "16-40 °C")], [("temperature optimum 37 °C", "37 °C")])
    add(80, ["HB62T"], "pH", [("pH range 6.0-9.5", "pH 6.0-9.5")], [("pH optimum 6.5-7.0", "pH 6.5-7.0")])
    add(83, ["Y1685T", "Y1700", "Y2011T", "Y2014"], "temperature", optima=[("temperature optimum 30 °C", "30 °C")])
    add(84, ["DFM-14T"], "temperature", optima=[("temperature optimum 25 °C", "25 °C")])
    add(84, ["DFM-14T"], "pH", optima=[("pH optimum 7.0", "pH 7.0")])
    add(88, ["AD34T"], "temperature", [("temperature range 20-60 °C", "20-60 °C")], [("temperature optimum 37 °C", "37 °C")])
    add(88, ["PAK95"], "temperature", [("temperature range 20-60 °C", "20-60 °C")], [("temperature optimum 40 °C", "40 °C")])
    add(88, ["AD34T", "PAK95"], "pH", [("pH range 5.0-9.0", "pH 5.0-9.0")], [("pH optimum 7.5", "pH 7.5")])
    add(90, ["N2T"], "temperature", [("temperature range 30-40 °C", "30 and 40 °C")], [("temperature optimum 35 °C", "35 °C")])
    add(90, ["N2T"], "pH", [("pH range 6.0-11.0", "6.0-11.0")], [("pH optimum 9.0", "pH 9.0")])
    add(93, ["2305UL40-4T"], "temperature", [("temperature range 22-36 °C", "22-36 °C")], [("temperature optimum 25-30 °C", "optimum 25-30 °C")])
    add(93, ["2305UL40-4T"], "pH", [("pH range 6-8", "pH 6-8")], [("pH optimum 7", "optimum pH 7")])
    add(94, ["LWZ-6T"], "temperature", [("temperature range 35-65 °C", "35-65 °C")], [("temperature optimum 55 °C", "optimum 55 °C")])
    add(94, ["LWZ-6T"], "pH", [("pH range 5.0-8.0", "pH 5.0-8.0")], [("pH optimum 6.0-6.5", "optimum 6.0-6.5")])
    add(97, ["NN19T"], "temperature", [("temperature range 15-37 °C", "15 °C and 37 °C")], [("temperature optimum 30 °C", "optimal 30 °C")])
    add(97, ["NN19T"], "pH", [("pH range 6.5-8.0", "pH 6.5-8.0")], [("pH optimum 7.0", "optimal pH 7.0")])
    add(100, ["P0083T"], "temperature", [("temperature range 4-25 °C", "4 and 25 °C")], [("temperature optimum 20 °C", "optimal growth at 20 °C")])
    add(100, ["P0083T"], "pH", ranges=[("pH range 5-8", "pH 5-8")])
    return data


NUMBER = r"-?\d+(?:\.\d+)?"
RANGE_VALUE = rf"{NUMBER}(?:\s*(?:-|–|to|and)\s*{NUMBER})?"
TEMPERATURE_PATTERN = re.compile(
    rf"(?P<value>\d+\(\d+\)\s*(?:-|–)\s*\d+|"
    rf"{NUMBER}\s*(?:°\s*C|℃)?\s*(?:-|–|to|and)\s*{NUMBER}|{NUMBER})"
    rf"\s*(?:°\s*C|℃)",
    re.IGNORECASE,
)
PH_PATTERN = re.compile(
    rf"\bpH\b(?P<prefix>\s*(?:(?:values?|range)?\s*"
    rf"(?:of|from|between|at|is)?\s*))(?P<value>{RANGE_VALUE})",
    re.IGNORECASE,
)
OPTIMUM_TAIL = re.compile(
    rf"^\s*\(?\s*(?:optimum|optimal|optima)"
    rf"(?:\s*(?:of|at|is|,|:))*\s*(?P<value>{RANGE_VALUE})\s*(?:°\s*C|℃)",
    re.IGNORECASE,
)
OPTIMUM_PH_TAIL = re.compile(
    rf"^\s*\(?\s*(?:optimum|optimal|optima)"
    rf"(?:\s*(?:of|at|is|,|:))*\s*(?:pH\s*)?(?P<value>{RANGE_VALUE})",
    re.IGNORECASE,
)
RANGE_TAIL = re.compile(
    rf"^\s*\(?\s*(?:range|ranging)(?:\s*(?:of|from|is|,|:))*\s*"
    rf"(?P<value>{RANGE_VALUE})\s*(?:°\s*C|℃)",
    re.IGNORECASE,
)
RANGE_PH_TAIL = re.compile(
    rf"^\s*\(?\s*(?:range|ranging)(?:\s*(?:of|from|is|,|:))*\s*"
    rf"(?:pH\s*)?(?P<value>{RANGE_VALUE})",
    re.IGNORECASE,
)


def is_range_value(value: str, prefix: str = "") -> bool:
    return bool(
        re.search(r"(?:-|–|\bto\b|\band\b)", value, re.IGNORECASE)
        or re.search(r"\b(?:between|from|range|ranging)\b", prefix, re.IGNORECASE)
    )


def sentence_observations(sentence: str, parameter: str) -> list[tuple[str, Observation]]:
    """Extract explicit numeric growth conditions from one source sentence."""
    found: list[tuple[str, Observation]] = []
    pattern = TEMPERATURE_PATTERN if parameter == "temperature" else PH_PATTERN
    tail_pattern = OPTIMUM_TAIL if parameter == "temperature" else OPTIMUM_PH_TAIL
    range_tail_pattern = RANGE_TAIL if parameter == "temperature" else RANGE_PH_TAIL
    matches = list(pattern.finditer(sentence))
    for match in matches:
        value = re.sub(r"(?:°\s*C|℃)", "", match.group("value"), flags=re.IGNORECASE)
        value = re.sub(r"\s+", " ", value.strip())
        direct_prefix = sentence[max(0, match.start() - 22) : match.start()]
        local_prefix = sentence[max(0, match.start() - 40) : match.start()]
        if parameter == "pH":
            local_prefix += match.group("prefix")
        local_prefix = re.split(r"[,;)]", local_prefix)[-1]
        optimum_near = bool(
            re.search(
                r"(?:\(\s*(?:optimum|optimal|optima)[^()]*$|"
                r"\b(?:optimum|optimal|optima)(?:\s+(?:is|of|at))?[\s,:]*$|"
                r"\b(?:grew|grows)?\s*optimally\s+at\s*$)",
                direct_prefix,
                re.IGNORECASE,
            )
        )
        observation_type = (
            "optimum"
            if optimum_near
            else "range"
            if is_range_value(value, local_prefix)
            else "optimum"
            if re.search(r"\b(?:optimal growth|grew optimally|grows optimally)\b", sentence, re.IGNORECASE)
            else "growth"
        )
        unit = " °C" if parameter == "temperature" else ""
        evidence_text = match.group(0)
        found.append(
            (
                observation_type,
                Observation(f"{parameter} {observation_type} {value}{unit}", evidence_text),
            )
        )

        # Parenthetical optima commonly omit the parameter name, for example
        # "pH 5.0-9.0 (optimum 7.0)" and "10-35 °C (optimum 28 °C)".
        tail = sentence[match.end() : match.end() + 70]
        optimum = tail_pattern.search(tail)
        if optimum:
            optimum_value = re.sub(r"\s+", " ", optimum.group("value").strip())
            optimum_start = match.end() + optimum.start()
            optimum_end = match.end() + optimum.end()
            found.append(
                (
                    "optimum",
                    Observation(
                        f"{parameter} optimum {optimum_value}{unit}",
                        sentence[optimum_start:optimum_end],
                    ),
                )
            )

        range_tail = range_tail_pattern.search(tail)
        if range_tail:
            range_value = re.sub(r"\s+", " ", range_tail.group("value").strip())
            range_start = match.end() + range_tail.start()
            range_end = match.end() + range_tail.end()
            found.append(
                (
                    "range",
                    Observation(
                        f"{parameter} range {range_value}{unit}",
                        sentence[range_start:range_end],
                    ),
                )
            )

    unique = []
    seen = set()
    for observation_type, observation in found:
        key = (observation_type, observation.display.casefold())
        if key not in seen:
            seen.add(key)
            unique.append((observation_type, observation))
    return unique


def automatic_annotations(
    rows: list[dict[str, str]], texts: dict[str, str], *, after_doc: int
) -> Annotations:
    """Extract growth conditions after the manually audited document prefix."""
    by_doc: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_doc.setdefault(row["doc"], []).append(row)

    result: Annotations = {}
    for doc, doc_rows in by_doc.items():
        if int(doc) <= after_doc:
            continue
        source = doc_rows[0]["source_file"]
        text = texts[source]
        strain_labels = list(
            dict.fromkeys(row["label"] for row in doc_rows if row["field"] == "strains")
        )
        if not strain_labels:
            continue
        first_sentence = next(sentence_spans(text), (0, text))[1]
        primary = [
            label
            for label in strain_labels
            if re.search(re.escape(label), first_sentence, re.IGNORECASE)
        ]
        if not primary:
            positions = [
                (match.start(), label)
                for label in strain_labels
                if (match := re.search(re.escape(label), text, re.IGNORECASE))
            ]
            primary = [min(positions)[1]] if positions else [strain_labels[0]]

        for _, sentence in sentence_spans(text):
            if not re.search(r"\b(?:growth|grew|grow|grows|optimum|optimal|optima|optimally|thrived)\b", sentence, re.IGNORECASE):
                continue
            explicit = [
                label
                for label in strain_labels
                if re.search(re.escape(label), sentence, re.IGNORECASE)
            ]
            subjects = explicit or primary
            for parameter in ("temperature", "pH"):
                observations = sentence_observations(sentence, parameter)
                if not observations:
                    continue
                for subject in subjects:
                    key = (doc, subject, parameter)
                    types = result.setdefault(
                        key, {"range": [], "growth": [], "optimum": []}
                    )
                    for observation_type, observation in observations:
                        if observation not in types[observation_type]:
                            types[observation_type].append(observation)
    return result


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


def evidence(text: str, subject: str, observation: Observation):
    candidates = []
    for sentence_start, sentence in sentence_spans(text):
        for match in re.finditer(re.escape(observation.evidence), sentence, re.IGNORECASE):
            subject_match = re.search(re.escape(subject), sentence, re.IGNORECASE)
            candidates.append(
                (
                    0 if subject_match else 1,
                    sentence_start,
                    match.start(),
                    sentence,
                    match,
                    subject_match,
                )
            )
    if not candidates:
        raise ValueError(f"Cannot locate evidence for {subject!r}: {observation.evidence!r}")
    _, sentence_start, _, sentence, match, subject_match = min(
        candidates, key=lambda item: item[:3]
    )
    spans = {(match.start(), match.end())}
    if subject_match:
        spans.add((subject_match.start(), subject_match.end()))
    highlighted = sentence
    for start, end in sorted(spans, reverse=True):
        highlighted = highlighted[:start] + "[[" + highlighted[start:end] + "]]" + highlighted[end:]
    return (
        "; ".join(
            f"{sentence_start + start}:{sentence_start + end}"
            for start, end in sorted(spans)
        ),
        highlighted,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--documents-dir", required=True, type=Path)
    parser.add_argument("--nodes", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--automatic-after",
        type=int,
        default=100,
        help="Use deterministic source-text extraction after this audited prefix.",
    )
    args = parser.parse_args()

    with args.input.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    rows = [
        row
        for row in rows
        if row.get("field") not in {"temperature_observation", "pH_observation"}
    ]

    wanted_ids = {identifier for pair in METPO.values() for identifier in pair}
    nodes = {}
    with args.nodes.open(newline="", encoding="utf-8") as stream:
        for node in csv.DictReader(stream, delimiter="\t"):
            if node.get("id") in wanted_ids:
                nodes[node["id"]] = node
    missing = wanted_ids - set(nodes)
    if missing:
        raise ValueError(f"Missing KG-Microbe METPO nodes: {sorted(missing)}")

    texts = {
        path.name: path.read_text(encoding="utf-8")
        for path in args.documents_dir.glob("*.txt")
    }
    all_annotations = annotations()
    generated = automatic_annotations(rows, texts, after_doc=args.automatic_after)
    overlap = set(all_annotations) & set(generated)
    if overlap:
        raise ValueError(f"Manual/automatic environmental overlap: {sorted(overlap)[:5]}")
    all_annotations.update(generated)
    by_doc = {}
    subject_ids = {}
    for row in rows:
        by_doc.setdefault(row["doc"], row)
        subject_ids.setdefault((row["doc"], row["label"]), row["entity_id"])
        if row.get("relationship_subject_label"):
            subject_ids.setdefault(
                (row["doc"], row["relationship_subject_label"]),
                row["relationship_subject_id"],
            )

    added = []
    for (doc, subject, parameter), types in all_annotations.items():
        if doc not in by_doc:
            raise ValueError(f"No TSV provenance row for document {doc}")
        subject_id = subject_ids.get((doc, subject))
        if not subject_id:
            raise ValueError(f"No entity ID for document {doc} subject {subject!r}")
        source = by_doc[doc]["source_file"]
        for observation_type in ("range", "growth", "optimum"):
            for observation in types[observation_type]:
                predicate_id, class_id = METPO[(parameter, observation_type)]
                predicate = nodes[predicate_id]
                observation_class = nodes[class_id]
                row = {field: "" for field in fieldnames}
                for field in ("doc", "source_file", "pmid"):
                    row[field] = by_doc[doc][field]
                row.update(
                    {
                        "field": f"{parameter}_observation",
                        "kind": "phenotype_observation",
                        "entity_id": f"AUTO:{quote(observation.display)}",
                        "label": observation.display,
                        "relationship_subject_id": subject_id,
                        "relationship_subject_label": subject,
                        "chemical_relationship": predicate["name"],
                        "chemical_level_type": observation_type,
                        "chemical_base_label": parameter,
                        "chemicals_utilized": "0",
                        "study_taxa": "0",
                        "strains": "0",
                        "chemical_relationship_id": predicate_id,
                        "chemical_relationship_label": predicate["name"],
                        "chemical_relationship_match_type": "kg_microbe_metpo",
                        "grounded_id": class_id,
                        "grounded_ids": class_id,
                        "kg_name": observation_class["name"],
                        "kg_category": observation_class["category"],
                        "match_type": "kg_microbe_metpo",
                        "kg_edge_count": "0",
                    }
                )
                row["original_spans"], row["context"] = evidence(
                    texts[source], subject, observation
                )
                added.append(row)

    rows.extend(added)
    rows.sort(
        key=lambda row: (
            int(row["doc"]),
            1 if row["field"] in {"temperature_observation", "pH_observation"} else 0,
            row["relationship_subject_label"].casefold(),
            row["field"],
            row.get("chemical_level_type", ""),
            row["label"].casefold(),
        )
    )
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Added environmental observation rows: {len(added)}")
    print(f"Total rows: {len(rows)}")


if __name__ == "__main__":
    main()
