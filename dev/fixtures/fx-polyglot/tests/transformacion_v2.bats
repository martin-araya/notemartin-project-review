#!/usr/bin/env bats
# Tests del binario transformacion_v2 (features v2 + strict).
setup() {
  BIN="${TRANSFORM_BIN_V2:-transformacion-linux-v2}"
  [ -x "$(which "$BIN" || true)" ] || skip "transformacion-linux-v2 no instalado"
}

@test "transformacion v2: lee .payload y emite transformed con sufijo ::v2" {
  echo '{"id":"a1","payload":"hola"}' | run "$BIN"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.id == "a1" and .transformed == "hola::v2" and .via == "v2"' >/dev/null
}

@test "transformacion v2 strict: campo extra se rechaza con exit 64" {
  echo '{"id":"a1","payload":"x","extra":"y"}' | run "$BIN"
  [ "$status" -eq 64 ]
}

@test "transformacion v2: campo raw se ignora silenciosamente" {
  echo '{"id":"a1","raw":"x"}' | run "$BIN"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.transformed == "::v2"' >/dev/null
}