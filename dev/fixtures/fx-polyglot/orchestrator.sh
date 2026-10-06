#!/usr/bin/env bash
# Orquestador poliglota (F06f): ingesta (Go) -> transformacion (Rust) -> reporte (jq/bash).
#
# Trampas plantadas:
#  1. set -euo pipefail, trap cleanup EXIT, eleccion de binario segun uname
#     (trampa #4 del ecosistema).
#  2. Exit codes usados como protocolo (trampa #5 del ecosistema):
#       0 = ok, 2 = empty line, 3 = malformed, 4 = unknown tag,
#       64 = strict rejected, 8 = JSON malformado, 9 = sin feature,
#       10 = OS no soportado, 11 = jq fallo, 12 = uso incorrecto.
#  3. Contrato JSON implicito: ingesta emite {id, ts, raw, tag} (current) o
#     {id, ts_raw, body} (legacy). El jq aqui reescribe silenciosamente con
#     fallback `.raw // .body // ""` (trampa del paquete #2).

set -euo pipefail
IFS=$'\n\t'

INGESTA_BIN="${INGESTA_BIN:-ingesta}"
INGESTA_TAG="${INGESTA_TAG:-current}"
TMPDIR_LOCAL="${TMPDIR:-/tmp}"

cleanup() {
  local rc=$?
  if [ -n "${WORKDIR:-}" ] && [ -d "$WORKDIR" ]; then
    rm -rf "$WORKDIR" 2>/dev/null || true
  fi
  exit "$rc"
}
trap cleanup EXIT

usage() {
  echo "uso: orchestrator.sh <input.txt> [output.json]" >&2
  exit 12
}

# Trampa #4: eleccion segun uname. La rama Linux es la que se ejercita en CI.
case "$(uname -s)" in
  Linux)
    TRANSFORM_BIN="${TRANSFORM_BIN:-transformacion-linux}"
    ;;
  Darwin)
    TRANSFORM_BIN="${TRANSFORM_BIN:-transformacion-linux-v2}"
    ;;
  *)
    echo "OS no soportado: $(uname -s) (exit 10)" >&2
    exit 10
    ;;
esac

[ "$#" -ge 1 ] || usage
INPUT="$1"
OUTPUT="${2:-reporte.json}"

if [ ! -f "$INPUT" ]; then
  echo "input inexistente: $INPUT" >&2
  exit 12
fi

WORKDIR="$(mktemp -d "$TMPDIR_LOCAL/fxpoly.XXXXXX")"
trap 'cleanup' EXIT

TAGS_FILE="$WORKDIR/tags.txt"
ITEMS_FILE="$WORKDIR/items.json"

# Capturamos los tags disponibles para incluirlos en el reporte (trampa #6).
if ! "$INGESTA_BIN" --list-tags > "$TAGS_FILE" 2>/dev/null; then
  : > "$TAGS_FILE"
fi

# Pipeline ingesta -> transformacion -> JSON normalizado por linea.
{
  "$INGESTA_BIN" --tag="$INGESTA_TAG" < "$INPUT" \
    | jq -c '{id: .id, raw: (.raw // .body // "")}' \
    | "$TRANSFORM_BIN"
} > "$ITEMS_FILE"

# Reporte final (NO usamos format_report de lib.sh: trampa #3 superficial).
if ! jq -n \
    --slurpfile items "$ITEMS_FILE" \
    --rawfile tags "$TAGS_FILE" \
    --arg now "$(iso_now)" \
    '{generated_at: $now, items: $items, available_handlers: ($tags | split("\n") | map(select(. != "")))}' \
    > "$OUTPUT"; then
  echo "jq fallo generando reporte (exit 11)" >&2
  exit 11
fi

echo "OK: $OUTPUT"