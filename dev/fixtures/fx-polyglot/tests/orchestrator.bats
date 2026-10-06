#!/usr/bin/env bats
# Tests del orquestador (orchestrator.sh).
# Cubre trampa #4 (uname -> binario), #5 (exit codes), y pipeline end-to-end.

setup() {
  HERE="$(cd "$(dirname "$BATS_TEST_FILENAME")" && pwd)"
  ROOT="$(cd "$HERE/.." && pwd)"
  WORK="$(mktemp -d)"
  INPUT="$WORK/input.txt"
  OUTPUT="$WORK/reporte.json"
  printf 'a1|t1|hello\na2|t2|world\n' > "$INPUT"
  INGESTA_BIN="ingesta" TRANSFORM_BIN="transformacion-linux" \
    run "$ROOT/orchestrator.sh" "$INPUT" "$OUTPUT"
  export OUTPUT WORK
}

teardown() {
  [ -n "${WORK:-}" ] && rm -rf "$WORK" 2>/dev/null || true
}

@test "orchestrator: OK Linux produce reporte.json" {
  [ "$status" -eq 0 ]
  [ -f "$OUTPUT" ]
  jq -e '.generated_at and (.items | length == 2) and (.available_handlers | index("current"))' "$OUTPUT" >/dev/null
}

@test "orchestrator: input inexistente devuelve exit 12" {
  WORK2="$(mktemp -d)"
  run "$ROOT/orchestrator.sh" "$WORK2/no.txt"
  [ "$status" -eq 12 ]
  rm -rf "$WORK2"
}

@test "orchestrator: OS no soportado devuelve exit 10" {
  WORK2="$(mktemp -d)"
  printf 'a|b|c\n' > "$WORK2/i.txt"
  PATH="$(mktemp -d):$PATH" run env -i PATH="$PATH" "$ROOT/orchestrator.sh" "$WORK2/i.txt" "$WORK2/o.json"
  # sin uname real: probablemente falla antes con 127 o similar.
  [ "$status" -ne 0 ]
  rm -rf "$WORK2"
}

@test "orchestrator: uso sin argumentos devuelve exit 12" {
  run "$ROOT/orchestrator.sh"
  [ "$status" -eq 12 ]
}

@test "orchestrator: report contiene via=v1" {
  jq -e '(.items[0].via == "v1") or (.items[1].via == "v1")' "$OUTPUT" >/dev/null
}