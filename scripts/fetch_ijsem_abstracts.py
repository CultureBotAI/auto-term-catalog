#!/usr/bin/env python3
"""Fetch the frozen IJSEM PMID corpus from Europe PMC and verify its hashes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


EUROPE_PMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def clean_text(value: str | None) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def fetch_abstract(pmid: str, *, timeout: float) -> str:
    query = urllib.parse.urlencode(
        {
            "query": f"EXT_ID:{pmid} AND SRC:MED",
            "format": "json",
            "resultType": "core",
            "pageSize": "1",
        }
    )
    request = urllib.request.Request(
        f"{EUROPE_PMC}?{query}",
        headers={"User-Agent": "CultureBotAI-auto-term-catalog/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    results = payload.get("resultList", {}).get("result", [])
    if not results:
        raise ValueError(f"Europe PMC returned no MED record for PMID {pmid}")
    abstract = clean_text(results[0].get("abstractText"))
    if not abstract:
        raise ValueError(f"Europe PMC returned no abstract for PMID {pmid}")
    return abstract


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--timeout", default=60.0, type=float)
    parser.add_argument("--delay", default=0.1, type=float)
    parser.add_argument(
        "--allow-content-drift",
        action="store_true",
        help="Write changed abstracts instead of failing their committed SHA-256 check.",
    )
    args = parser.parse_args()

    with args.manifest.open(newline="", encoding="utf-8") as stream:
        manifest = list(csv.DictReader(stream, delimiter="\t"))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for index, row in enumerate(manifest, start=1):
        abstract = fetch_abstract(row["pmid"], timeout=args.timeout)
        content = abstract.encode("utf-8")
        digest = hashlib.sha256(content).hexdigest()
        if digest != row["abstract_sha256"] and not args.allow_content_drift:
            raise ValueError(
                f"Content drift for PMID {row['pmid']}: expected "
                f"{row['abstract_sha256']}, observed {digest}"
            )
        destination = args.output_dir / row["source_file"]
        destination.write_bytes(content)
        if index != len(manifest):
            time.sleep(args.delay)
    print(f"Fetched and verified {len(manifest)} IJSEM abstracts")


if __name__ == "__main__":
    main()
