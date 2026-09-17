#!/usr/bin/env python3
"""Flatten OntoGPT chemical-utilization YAML into grounding candidates."""

from __future__ import annotations

import argparse
import csv
import itertools
import os
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote, unquote

import yaml


FIELD_KINDS = {
    "study_taxa": "taxon_candidate",
    "strains": "strain",
}
STRAIN_OBJECT_PREDICATES = {"deposited_as", "identical_to"}
SPAN_PATTERN = re.compile(r"^\s*(\d+)\s*:\s*(\d+)\s*$")


def normalized_document_text(text: str) -> str:
    """Normalize inconsequential file/YAML line-ending differences."""
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def documents_with_sources(
    documents: list[Any], source_files: list[Path]
) -> list[tuple[int, dict[str, Any], Path | None]]:
    """Match extracted documents to source files by text, never directory order."""
    if not source_files:
        return [
            (position, document, None)
            for position, document in enumerate(documents, start=1)
            if isinstance(document, dict)
        ]

    sources_by_text: dict[str, deque[Path]] = defaultdict(deque)
    for source_file in source_files:
        text = normalized_document_text(source_file.read_text(encoding="utf-8"))
        sources_by_text[text].append(source_file)

    matched: list[tuple[Path, dict[str, Any]]] = []
    for yaml_position, document in enumerate(documents, start=1):
        if not isinstance(document, dict):
            continue
        input_text = document.get("input_text")
        if not isinstance(input_text, str):
            raise ValueError(f"YAML document {yaml_position} has no input_text")
        candidates = sources_by_text.get(normalized_document_text(input_text))
        if not candidates:
            raise ValueError(
                f"YAML document {yaml_position} does not match any unused source file"
            )
        matched.append((candidates.popleft(), document))

    unused = [path.name for candidates in sources_by_text.values() for path in candidates]
    if unused:
        raise ValueError(
            f"{len(unused)} source file(s) were not matched to a YAML document: "
            + ", ".join(sorted(unused)[:5])
        )

    matched.sort(key=lambda item: os.fsencode(item[0].name))
    return [
        (position, document, source_file)
        for position, (source_file, document) in enumerate(matched, start=1)
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--documents-dir",
        type=Path,
        help="Optional input directory whose sorted filenames supply source file and PMID provenance.",
    )
    parser.add_argument(
        "--max-documents",
        type=int,
        help="Process only the first N documents and source files in deterministic order.",
    )
    return parser.parse_args()


def values(value: Any) -> Iterable[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return (item for item in value if isinstance(item, str))
    if isinstance(value, str):
        return [value]
    return []


def raw_values(raw_output: str, field: str) -> list[str]:
    match = re.search(
        rf"(?m)^[ \t]*{re.escape(field)}:[ \t]*([^\r\n]*)$",
        raw_output,
    )
    if not match or not match.group(1):
        return []
    return [value.strip() for value in match.group(1).split(";") if value.strip()]


def normalized_spans(entity: dict[str, Any]) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for span in entity.get("original_spans") or []:
        if isinstance(span, str):
            match = SPAN_PATTERN.match(span)
            if match:
                spans.append((int(match.group(1)), int(match.group(2))))
        elif isinstance(span, dict):
            start = span.get("start")
            end = span.get("end")
            if isinstance(start, int) and isinstance(end, int):
                spans.append((start, end))
    return spans


def context_from_spans(
    text: str,
    spans: list[tuple[int, int]],
    *,
    related_label: str = "",
    window: int = 50,
) -> str:
    snippets: list[str] = []
    for start, end in spans:
        if not 0 <= start < end <= len(text):
            continue
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        prefix = text[context_start:start]
        mention = text[start:end]
        suffix = text[end:context_end]
        snippet = (
            ("..." if context_start else "")
            + prefix
            + f"[[{mention}]]"
            + suffix
            + ("..." if context_end < len(text) else "")
        )
        if related_label:
            snippet = re.sub(
                re.escape(related_label),
                lambda match: f"[[{match.group(0)}]]",
                snippet,
                flags=re.IGNORECASE,
            )
        if snippet not in snippets:
            snippets.append(snippet)
    return "; ".join(snippets)


def find_label_spans(text: str, label: str) -> list[tuple[int, int]]:
    if not text or not label:
        return []
    exact = [
        (match.start(), match.end())
        for match in re.finditer(re.escape(label), text, flags=re.IGNORECASE)
    ]
    if exact:
        return exact

    flexible_pattern = re.escape(label).replace(r"\ ", r"\s+")
    flexible_pattern = flexible_pattern.replace(r"\+", r"\s*\+")
    flexible_pattern = flexible_pattern.replace(r"\-", r"\s*\-")
    flexible = [
        (match.start(), match.end())
        for match in re.finditer(flexible_pattern, text, flags=re.IGNORECASE)
    ]
    if flexible:
        return flexible

    suffix = label.rsplit(maxsplit=1)[-1]
    if len(suffix) >= 3 and any(character.isdigit() for character in suffix):
        return [
            (match.start(), match.end())
            for match in re.finditer(
                rf"(?<![A-Za-z0-9]){re.escape(suffix)}(?![A-Za-z0-9])",
                text,
                flags=re.IGNORECASE,
            )
        ]
    return []


def main() -> None:
    args = parse_args()
    if args.max_documents is not None and args.max_documents < 1:
        raise ValueError("--max-documents must be a positive integer")
    source_files = (
        sorted(args.documents_dir.glob("*.txt"), key=lambda path: os.fsencode(path.name))
        if args.documents_dir
        else []
    )
    if args.max_documents is not None:
        source_files = source_files[: args.max_documents]
    rows: list[dict[str, str]] = []

    with args.input.open(encoding="utf-8") as stream:
        loaded = yaml.safe_load_all(stream)
        documents = list(
            itertools.islice(loaded, args.max_documents)
            if args.max_documents is not None
            else loaded
        )

    for doc_number, document, matched_source in documents_with_sources(
        documents, source_files
    ):
        extracted = document.get("extracted_object") or {}
        entity_records = {
            entity.get("id"): entity
            for entity in document.get("named_entities") or []
            if isinstance(entity, dict) and entity.get("id")
        }
        entities = {}
        for entity_id, entity in entity_records.items():
            label = entity.get("label", "")
            # PyYAML 1.1 coerces unquoted labels such as "on" to booleans.
            # The AUTO identifier retains the original lexical value.
            entities[entity_id] = (
                label
                if isinstance(label, str)
                else unquote(entity_id.removeprefix("AUTO:"))
            )
        ids_by_label = {label.casefold(): entity_id for entity_id, label in entities.items() if label}
        input_text = document.get("input_text") or ""
        source_file = matched_source.name if matched_source else ""
        pmid_match = re.search(r"-(\d+)-abstract\.txt$", source_file)
        pmid = pmid_match.group(1) if pmid_match else ""
        seen: set[tuple[str, str, str, str]] = set()

        def add(
            field: str,
            kind: str,
            entity_id: str,
            *,
            relationship_subject_id: str = "",
            chemical_relationship: str = "",
        ) -> None:
            key = (field, entity_id, relationship_subject_id, chemical_relationship)
            if key in seen:
                return
            seen.add(key)
            entity = entity_records.get(entity_id, {})
            label = entities.get(entity_id, unquote(entity_id.removeprefix("AUTO:")))
            spans = find_label_spans(input_text, label) or normalized_spans(entity)
            relationship_subject_label = (
                entities.get(
                    relationship_subject_id,
                    unquote(relationship_subject_id.removeprefix("AUTO:")),
                )
                if relationship_subject_id
                else ""
            )
            context = context_from_spans(
                input_text,
                spans,
                related_label=relationship_subject_label,
            )
            if not context:
                spans = find_label_spans(input_text, label)
                context = context_from_spans(
                    input_text,
                    spans,
                    related_label=relationship_subject_label,
                )
            rows.append(
                {
                    "doc": str(doc_number),
                    "source_file": source_file,
                    "pmid": pmid,
                    "field": field,
                    "kind": kind,
                    "entity_id": entity_id,
                    "label": label,
                    "original_spans": "; ".join(f"{start}:{end}" for start, end in spans),
                    "context": context,
                    "relationship_subject_id": relationship_subject_id,
                    "relationship_subject_label": relationship_subject_label,
                    "chemical_relationship": chemical_relationship,
                }
            )

        for field, kind in FIELD_KINDS.items():
            for entity_id in values(extracted.get(field)):
                add(field, kind, entity_id)
            for label in raw_values(document.get("raw_completion_output") or "", field):
                entity_id = ids_by_label.get(label.casefold(), f"AUTO:{quote(label)}")
                add(field, kind, entity_id)

        for relation in extracted.get("chemical_utilizations") or []:
            if not isinstance(relation, dict):
                continue
            subject = relation.get("subject")
            predicate = relation.get("predicate")
            obj = relation.get("object")
            if not all(
                isinstance(value, str) and value.strip()
                for value in (subject, predicate, obj)
            ):
                continue
            add(
                "chemical_utilization_object",
                "chemical",
                obj,
                relationship_subject_id=subject,
                chemical_relationship=predicate,
            )

        for relation in extracted.get("strain_relationships") or []:
            if not isinstance(relation, dict):
                continue
            subject = relation.get("subject")
            obj = relation.get("object")
            predicate = relation.get("predicate", "")
            if isinstance(subject, str):
                add("strains", "strain", subject)
            if isinstance(obj, str):
                if predicate in STRAIN_OBJECT_PREDICATES:
                    add("strains", "strain", obj)
                else:
                    add("study_taxa", "taxon_candidate", obj)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "doc",
        "source_file",
        "pmid",
        "field",
        "kind",
        "entity_id",
        "label",
        "original_spans",
        "context",
        "relationship_subject_id",
        "relationship_subject_label",
        "chemical_relationship",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
