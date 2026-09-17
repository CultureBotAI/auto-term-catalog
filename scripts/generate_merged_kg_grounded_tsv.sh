#!/usr/bin/env bash
#
# Deterministically convert a multi-document OntoGPT extraction YAML file into
# a merged-KG-grounded TSV. The same ordered inputs produce byte-identical TSVs.

set -euo pipefail

export LC_ALL=C
export PYTHONHASHSEED=0
export TZ=UTC

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

usage() {
  cat <<'EOF'
Usage:
  scripts/generate_merged_kg_grounded_tsv.sh \
    --extraction PATH \
    --documents-dir PATH \
    --nodes PATH \
    --edges PATH \
    --metpo PATH \
    --output PATH \
    [--entities-output PATH] \
    [--max-documents NUMBER] \
    [--expand-growth-conditions] \
    [--max-edge-evidence NUMBER]

Required inputs:
  --extraction     Multi-document OntoGPT extraction YAML.
  --documents-dir Directory of PMID-labelled source .txt files. Files are
                  associated with YAML documents in bytewise filename order.
  --nodes          merged-kg_nodes.tsv.
  --edges          merged-kg_edges.tsv.
  --metpo          METPO ontology in RDF/XML OWL format.
  --output         Destination grounded TSV.

Optional:
  --entities-output     Destination for the intermediate flattened entity TSV.
                        Defaults to OUTPUT with ".entities.tsv" appended.
  --max-documents       Process only the first NUMBER extracted documents and
                        source files in deterministic order.
  --expand-growth-conditions
                        Add source-grounded salinity, temperature, and pH
                        ranges/growth values/optima after KG grounding.
  --max-edge-evidence  Maximum incident KG edges retained per grounded ID.
                        Defaults to 5.
EOF
}

EXTRACTION=""
DOCUMENTS_DIR=""
NODES=""
EDGES=""
METPO=""
OUTPUT=""
ENTITIES_OUTPUT=""
MAX_DOCUMENTS=""
EXPAND_GROWTH_CONDITIONS=0
MAX_EDGE_EVIDENCE=5

while (($#)); do
  case "$1" in
    --extraction)
      EXTRACTION="${2:?missing value for --extraction}"
      shift 2
      ;;
    --documents-dir)
      DOCUMENTS_DIR="${2:?missing value for --documents-dir}"
      shift 2
      ;;
    --nodes)
      NODES="${2:?missing value for --nodes}"
      shift 2
      ;;
    --edges)
      EDGES="${2:?missing value for --edges}"
      shift 2
      ;;
    --metpo)
      METPO="${2:?missing value for --metpo}"
      shift 2
      ;;
    --output)
      OUTPUT="${2:?missing value for --output}"
      shift 2
      ;;
    --entities-output)
      ENTITIES_OUTPUT="${2:?missing value for --entities-output}"
      shift 2
      ;;
    --max-documents)
      MAX_DOCUMENTS="${2:?missing value for --max-documents}"
      shift 2
      ;;
    --expand-growth-conditions)
      EXPAND_GROWTH_CONDITIONS=1
      shift
      ;;
    --max-edge-evidence)
      MAX_EDGE_EVIDENCE="${2:?missing value for --max-edge-evidence}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

for required in EXTRACTION DOCUMENTS_DIR NODES EDGES METPO OUTPUT; do
  if [[ -z "${!required}" ]]; then
    echo "Missing required argument: ${required}" >&2
    usage >&2
    exit 2
  fi
done

[[ -f "${EXTRACTION}" ]] || { echo "Extraction file not found: ${EXTRACTION}" >&2; exit 1; }
[[ -d "${DOCUMENTS_DIR}" ]] || { echo "Documents directory not found: ${DOCUMENTS_DIR}" >&2; exit 1; }
[[ -f "${NODES}" ]] || { echo "Node file not found: ${NODES}" >&2; exit 1; }
[[ -f "${EDGES}" ]] || { echo "Edge file not found: ${EDGES}" >&2; exit 1; }
[[ -f "${METPO}" ]] || { echo "METPO file not found: ${METPO}" >&2; exit 1; }
[[ "${MAX_EDGE_EVIDENCE}" =~ ^[0-9]+$ ]] || {
  echo "--max-edge-evidence must be a non-negative integer" >&2
  exit 2
}
if [[ -n "${MAX_DOCUMENTS}" && ! "${MAX_DOCUMENTS}" =~ ^[1-9][0-9]*$ ]]; then
  echo "--max-documents must be a positive integer" >&2
  exit 2
fi

if [[ -z "${ENTITIES_OUTPUT}" ]]; then
  ENTITIES_OUTPUT="${OUTPUT%.tsv}.entities.tsv"
fi

mkdir -p -- "$(dirname -- "${OUTPUT}")" "$(dirname -- "${ENTITIES_OUTPUT}")"
TMP_ENTITIES="$(mktemp "${ENTITIES_OUTPUT}.tmp.XXXXXX")"
TMP_OUTPUT="$(mktemp "${OUTPUT}.tmp.XXXXXX")"
TMP_EXPANDED="$(mktemp "${OUTPUT}.expanded.tmp.XXXXXX")"
cleanup() {
  rm -f -- "${TMP_ENTITIES}" "${TMP_OUTPUT}" "${TMP_EXPANDED}"
}
trap cleanup EXIT

EXTRACT_ARGS=(
  --input "${EXTRACTION}"
  --documents-dir "${DOCUMENTS_DIR}"
  --output "${TMP_ENTITIES}"
)
if [[ -n "${MAX_DOCUMENTS}" ]]; then
  EXTRACT_ARGS+=(--max-documents "${MAX_DOCUMENTS}")
fi
python3 "${REPO_ROOT}/src/process_terms/extract_grounding_entities.py" "${EXTRACT_ARGS[@]}"

python3 "${REPO_ROOT}/src/process_terms/ground_entities_merged_kg.py" \
  --input "${TMP_ENTITIES}" \
  --nodes "${NODES}" \
  --edges "${EDGES}" \
  --metpo "${METPO}" \
  --max-edge-evidence "${MAX_EDGE_EVIDENCE}" \
  --strict-relationships \
  --output "${TMP_OUTPUT}"

if ((EXPAND_GROWTH_CONDITIONS)); then
  python3 "${REPO_ROOT}/scripts/expand_first100_chemical_levels.py" \
    --input "${TMP_OUTPUT}" \
    --documents-dir "${DOCUMENTS_DIR}" \
    --nodes "${NODES}" \
    --output "${TMP_EXPANDED}"
  python3 "${REPO_ROOT}/scripts/expand_first100_environmental_observations.py" \
    --input "${TMP_EXPANDED}" \
    --documents-dir "${DOCUMENTS_DIR}" \
    --nodes "${NODES}" \
    --output "${TMP_OUTPUT}"
fi

chmod 0644 "${TMP_ENTITIES}" "${TMP_OUTPUT}"
mv -f -- "${TMP_ENTITIES}" "${ENTITIES_OUTPUT}"
mv -f -- "${TMP_OUTPUT}" "${OUTPUT}"
rm -f -- "${TMP_EXPANDED}"

trap - EXIT
echo "Wrote entities: ${ENTITIES_OUTPUT}"
echo "Wrote grounded TSV: ${OUTPUT}"
