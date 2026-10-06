#!/usr/bin/env bash
# Helpers bash del orquestador del fixture fx-polyglot.
#
# Trampa del paquete #2: format_report() esta definida aqui pero nunca se llama;
# el orquestador usa `jq -n` directamente.

set -euo pipefail

# Emite timestamp ISO-8601 UTC. Wrapper para que la policy output sea estable.
iso_now() {
  date -u +%Y-%m-%dT%H:%M:%SZ
}

# NO SE USA (trampa #3 superficial: helper exportado pero no llamado).
# Documentada en ground_truth.json como superficie muerta.
format_report() {
  local items_file="$1"
  local tags_file="$2"
  jq -n \
    --slurpfile items "$items_file" \
    --rawfile tags "$tags_file" \
    '{generated_at: (now | todate), items: $items, handlers: ($tags | split("\n"))}'
}

# Mensaje legacy (tambien no usado) para verificar la busqueda de codigo muerto.
unused_helper() {
  echo "este helper no se invoca" >&2
  return 1
}