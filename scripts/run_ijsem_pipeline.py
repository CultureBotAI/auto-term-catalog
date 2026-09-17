#!/usr/bin/env python3
"""Run IJSEM acquisition, OntoGPT extraction, grounding, and TSV export."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run(command: list[str]) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=Path("config/ijsem_first1000_pipeline.json"),
        type=Path,
    )
    parser.add_argument("--nodes", required=True, type=Path)
    parser.add_argument("--edges", required=True, type=Path)
    parser.add_argument("--metpo", required=True, type=Path)
    parser.add_argument(
        "--extraction",
        type=Path,
        help="Reuse an existing OntoGPT YAML stream instead of calling the model.",
    )
    parser.add_argument(
        "--documents-dir",
        type=Path,
        help="Reuse an existing verified abstract directory instead of Europe PMC.",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dry-run-extraction", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    config_path = args.config if args.config.is_absolute() else repo_root / args.config
    config = json.loads(config_path.read_text(encoding="utf-8"))
    documents_dir = args.documents_dir or repo_root / config["corpus"]["documents_dir"]
    extraction = args.extraction or repo_root / config["ontogpt"]["extraction_output"]
    output = args.output or repo_root / config["output"]["grounded_tsv"]
    entities_output = repo_root / config["output"]["entities_tsv"]

    if args.documents_dir is None:
        run(
            [
                "python3",
                str(repo_root / "scripts/fetch_ijsem_abstracts.py"),
                "--manifest",
                str(repo_root / config["corpus"]["manifest"]),
                "--output-dir",
                str(documents_dir),
            ]
        )
    if args.extraction is None:
        extraction_command = [
            "python3",
            str(repo_root / "scripts/run_ontogpt_extraction.py"),
            "--config",
            str(config_path),
            "--documents-dir",
            str(documents_dir),
            "--output",
            str(extraction),
        ]
        if args.dry_run_extraction:
            extraction_command.append("--dry-run")
        run(extraction_command)
        if args.dry_run_extraction:
            return

    grounding = config["grounding"]
    command = [
        str(repo_root / "scripts/generate_merged_kg_grounded_tsv.sh"),
        "--extraction",
        str(extraction),
        "--documents-dir",
        str(documents_dir),
        "--nodes",
        str(args.nodes),
        "--edges",
        str(args.edges),
        "--metpo",
        str(args.metpo),
        "--max-documents",
        str(config["corpus"]["document_limit"]),
        "--max-edge-evidence",
        str(grounding["max_edge_evidence"]),
        "--entities-output",
        str(entities_output),
        "--output",
        str(output),
    ]
    if grounding.get("expand_growth_conditions"):
        command.append("--expand-growth-conditions")
    run(command)


if __name__ == "__main__":
    main()
