#!/usr/bin/env python3
"""Run the configured OntoGPT extraction in validated, resumable batches."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

import yaml


def normalized(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def load_documents(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as stream:
        documents = [item for item in yaml.safe_load_all(stream) if isinstance(item, dict)]
    return documents


def validate_batch(output: Path, inputs: list[Path]) -> None:
    documents = load_documents(output)
    expected = sorted(normalized(path.read_text(encoding="utf-8")) for path in inputs)
    observed = sorted(normalized(str(doc.get("input_text", ""))) for doc in documents)
    if expected != observed:
        raise ValueError(
            f"{output} does not contain exactly the {len(inputs)} requested input texts"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--documents-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--batch-dir", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    extraction = config["ontogpt"]
    repo_root = Path(__file__).resolve().parents[1]
    template = repo_root / extraction["template"]
    batch_root = args.batch_dir or repo_root / extraction["batch_dir"]
    limit = int(config["corpus"]["document_limit"])
    batch_size = int(extraction["batch_size"])
    inputs = sorted(args.documents_dir.glob("*.txt"), key=lambda path: os.fsencode(path.name))[:limit]
    if len(inputs) != limit:
        raise ValueError(f"Expected {limit} abstract files, found {len(inputs)}")

    environment = os.environ.copy()
    if not environment.get("OPENAI_API_KEY") and environment.get("CBORG_API_KEY"):
        environment["OPENAI_API_KEY"] = environment["CBORG_API_KEY"]
    if not args.dry_run and not environment.get("OPENAI_API_KEY"):
        raise ValueError("Set CBORG_API_KEY or OPENAI_API_KEY before running OntoGPT")

    batch_root.mkdir(parents=True, exist_ok=True)
    batch_outputs = []
    commands = []
    for batch_number, start in enumerate(range(0, len(inputs), batch_size), start=1):
        batch_inputs = inputs[start : start + batch_size]
        input_dir = batch_root / f"batch_{batch_number:04d}_inputs"
        output = batch_root / f"batch_{batch_number:04d}.yaml"
        log = batch_root / f"batch_{batch_number:04d}.log"
        input_dir.mkdir(parents=True, exist_ok=True)
        for source in batch_inputs:
            destination = input_dir / source.name
            if not destination.exists() or destination.read_bytes() != source.read_bytes():
                shutil.copyfile(source, destination)
        command = [
            "ontogpt",
            "extract",
            "--template",
            str(template),
            "--inputfile",
            str(input_dir),
            "--model",
            extraction["model"],
            "--model-provider",
            extraction["model_provider"],
            "--api-base",
            extraction["api_base"],
            "--temperature",
            str(extraction["temperature"]),
            "--output-format",
            "yaml",
            "--output",
            str(output),
        ]
        commands.append(command)
        if args.dry_run:
            continue
        if output.exists() and not args.force:
            try:
                validate_batch(output, batch_inputs)
                batch_outputs.append(output)
                continue
            except (ValueError, yaml.YAMLError):
                pass
        with log.open("w", encoding="utf-8") as log_stream:
            subprocess.run(
                command,
                check=True,
                env=environment,
                stdout=log_stream,
                stderr=subprocess.STDOUT,
            )
        validate_batch(output, batch_inputs)
        batch_outputs.append(output)

    metadata = {
        "config": config,
        "template_sha256": hashlib.sha256(template.read_bytes()).hexdigest(),
        "document_count": len(inputs),
        "commands": commands,
    }
    metadata_path = args.output.with_suffix(args.output.suffix + ".run.json")
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if args.dry_run:
        print(f"Validated configuration for {len(inputs)} abstracts in {len(commands)} batches")
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as destination:
        for batch_output in batch_outputs:
            content = batch_output.read_bytes().rstrip() + b"\n"
            destination.write(content)
    validate_batch(args.output, inputs)
    print(f"Wrote {len(inputs)} extracted documents to {args.output}")


if __name__ == "__main__":
    main()
