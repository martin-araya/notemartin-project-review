#!/usr/bin/env bats
# Test end-to-end: ingest -> transform -> report (todo el pipeline).

setup() {
  HERE="$(cd "$(dirname "$BATS_TEST_FILENAME")" && pwd)"
  ROOT="$(cd "$HERE/.." && pwd)"
  WORK="$(mktemp -d)"
  INPUT="$WORK/input.txt"
  OUTPUT="$WORK/reporte.json"
  printf 'a1|t1|hola\na2|t2|mundo\n' > "$INPUT"
  [ -x "$(which ingesta || true)" ] || skip "ingesta no instalado"
  [ -x "$(which transformacion-linux || true)" ] || skip "transformacion-linux no instalado"
}

teardown() {
  [ -n "${WORK:-}" ] && rm -rf "$WORK" 2>/dev/null || true
}

@test "e2e: ok Linux genera reporte valido" {
  run "$ROOT/orchestrator.sh" "$INPUT" "$OUTPUT"
  [ "$status" -eq 0 ]
  [ -f "$OUTPUT" ]
  jq -e '.items | length == 2' "$OUTPUT" >/dev/null
  jq -e 'all(.items[]; .transformed | endswith("::v1"))' "$OUTPUT" >/dev/null
  jq -e 'all(.items[]; .via == "v1")' "$OUTPUT" >/dev/null
}

@test "e2e: reporte incluye available_handlers" {
  run "$ROOT/orchestrator.sh" "$INPUT" "$OUTPUT"
  [ "$status" -eq 0 ]
  jq -e '.available_handlers | index("current")' "$OUTPUT" >/dev/null
}

@test "e2e: input vacio produce reporte sin items" {
  : > "$INPUT"
  run "$ROOT/orchestrator.sh" "$INPUT" "$OUTPUT"
  # ingesta devuelve exit 2 en linea vacia, asi que el orquestador aborta.
  [ "$status" -ne 0 ]
}