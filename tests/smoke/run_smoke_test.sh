#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C
export PYTHONHASHSEED=0
export TZ=UTC

TEST_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${TEST_DIR}/../.." && pwd)"
OUTPUT_DIR="${1:-${REPO_ROOT}/work/smoke}"
TABLE_A="${OUTPUT_DIR}/smoke_merged_kg_grounded.tsv"
TABLE_B="${OUTPUT_DIR}/smoke_merged_kg_grounded.second.tsv"
ENTITIES_A="${OUTPUT_DIR}/smoke_entities.tsv"
ENTITIES_B="${OUTPUT_DIR}/smoke_entities.second.tsv"
REVIEW="${OUTPUT_DIR}/smoke.review.md"
CATALOG="${OUTPUT_DIR}/smoke.ungrounded_catalog.tsv"

if ! python3 -c 'import pandas, tabulate, yaml' >/dev/null 2>&1; then
  echo "Missing smoke-test dependencies." >&2
  echo "Install requirements-extraction.txt and .claude/skills/review-extraction-table/requirements.txt." >&2
  exit 2
fi

mkdir -p -- "${OUTPUT_DIR}"

generate() {
  local entities="$1"
  local table="$2"
  "${REPO_ROOT}/scripts/generate_merged_kg_grounded_tsv.sh" \
    --extraction "${TEST_DIR}/ontogpt_extraction.yaml" \
    --documents-dir "${TEST_DIR}/abstracts" \
    --nodes "${TEST_DIR}/merged-kg_nodes.tsv" \
    --edges "${TEST_DIR}/merged-kg_edges.tsv" \
    --metpo "${TEST_DIR}/metpo.owl" \
    --max-documents 1 \
    --max-edge-evidence 5 \
    --entities-output "${entities}" \
    --output "${table}"
}

generate "${ENTITIES_A}" "${TABLE_A}"
generate "${ENTITIES_B}" "${TABLE_B}"
cmp -- "${TABLE_A}" "${TABLE_B}"
cmp -- "${ENTITIES_A}" "${ENTITIES_B}"

python3 "${REPO_ROOT}/.claude/skills/review-extraction-table/scripts/profile_table.py" \
  "${TABLE_A}" \
  --out "${REVIEW}" \
  --catalog-out "${CATALOG}" \
  --top 5

python3 "${TEST_DIR}/assert_smoke_output.py" \
  --table "${TABLE_A}" \
  --abstract "${TEST_DIR}/abstracts/00001-99999999-abstract.txt" \
  --review "${REVIEW}"

echo "Smoke table: ${TABLE_A}"
echo "Review report: ${REVIEW}"
