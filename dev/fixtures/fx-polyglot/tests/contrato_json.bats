#!/usr/bin/env bats
# Tests del contrato JSON implicito (trampa #1 del ecosistema).

setup() {
  WORK="$(mktemp -d)"
  INPUT="$WORK/input.txt"
  printf 'a1|t1|hola\n' > "$INPUT"
  [ -x "$(which ingesta || true)" ] || skip "ingesta no instalado"
  [ -x "$(which transformacion-linux || true)" ] || skip "transformacion-linux no instalado"
}

teardown() {
  [ -n "${WORK:-}" ] && rm -rf "$WORK" 2>/dev/null || true
}

@test "contrato: ingesta current emite {id, ts, raw, tag}" {
  run bash -c "echo 'a|t|r' | ingesta --tag=current"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e 'has("raw") and has("tag") and has("ts") and has("id")' >/dev/null
}

@test "contrato: transformacion v1 acepta el campo raw" {
  echo '{"id":"x","raw":"valor","tag":"current","ts":"now"}' | run transformacion-linux
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.transformed == "valor::v1"' >/dev/null
}

@test "contrato: si ingesta emite sin raw (v2 payload), v1 lo trata como vacio" {
  echo '{"id":"x","payload":"valor","ts":"now"}' | run transformacion-linux
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.transformed == "::v1"' >/dev/null
}

@test "contrato: legacy_compat rellena raw cuando falta" {
  echo '{"id":"x"}' | run transformacion-linux
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.transformed == "::v1"' >/dev/null
}