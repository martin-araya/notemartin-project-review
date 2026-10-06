#!/usr/bin/env bats
# Tests del binario transformacion con feature v1 (default).
setup() {
  BIN="${TRANSFORM_BIN:-transformacion-linux}"
  [ -x "$(which "$BIN" || true)" ] || skip "transformacion-linux no instalado"
}

@test "transformacion v1: lee .raw y emite transformed con sufijo ::v1" {
  echo '{"id":"a1","raw":"hola"}' | run "$BIN"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.id == "a1" and .transformed == "hola::v1" and .via == "v1"' >/dev/null
}

@test "transformacion v1: campo payload se ignora silenciosamente" {
  echo '{"id":"a1","payload":"x"}' | run "$BIN"
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.transformed == "::v1"' >/dev/null
}

@test "transformacion v1: JSON malformado devuelve exit 8" {
  echo 'no es json' | run "$BIN"
  [ "$status" -eq 8 ]
}

@test "transformacion v1: linea vacia devuelve exit 2" {
  printf '\n' | run "$BIN"
  [ "$status" -eq 2 ]
}

@test "transformacion v1: maneja multiples lineas" {
  printf '{"id":"a","raw":"1"}\n{"id":"b","raw":"2"}\n' | run "$BIN"
  [ "$status" -eq 0 ]
  lines=$(echo "$output" | wc -l | tr -d ' ')
  [ "$lines" -eq 2 ]
}