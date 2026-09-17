#!/usr/bin/env python3
"""Create a deterministic PMID/source/hash manifest from abstract text files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
from pathlib import Path


FILENAME = re.compile(r"^(?P<rank>\d+)-(?P<pmid>\d+)-abstract\.txt$")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--documents-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-documents", type=int)
    args = parser.parse_args()

    paths = sorted(
        args.documents_dir.glob("*.txt"), key=lambda path: os.fsencode(path.name)
    )
    if args.max_documents is not None:
        if args.max_documents < 1:
            raise ValueError("--max-documents must be positive")
        paths = paths[: args.max_documents]

    rows = []
    for position, path in enumerate(paths, start=1):
        match = FILENAME.match(path.name)
        if not match:
            raise ValueError(f"Unexpected abstract filename: {path.name}")
        rows.append(
            {
                "rank": str(position),
                "pmid": match.group("pmid"),
                "source_file": path.name,
                "abstract_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["rank", "pmid", "source_file", "abstract_sha256"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} manifest rows to {args.output}")


if __name__ == "__main__":
    main()
