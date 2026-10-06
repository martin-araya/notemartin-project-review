#!/usr/bin/env bats
# Tests de la CLI ingesta (Go).
# Usa el binario `ingesta` instalado por el Dockerfile o el local.

setup() {
  BIN="${INGESTA_BIN:-ingesta}"
  [ -x "$(which "$BIN" || true)" ] || skip "ingesta no instalado"
}

@test "ingesta: emite JSON con tag current para entrada valida" {
  echo "a1|b1|hello" | run "$BIN" --tag=current
  [ "$status" -eq 0 ]
  echo "$output" | jq -e '.id == "a1" and .ts == "b1" and .raw == "hello" and .tag == "current"' >/dev/null
}

@test "ingesta: maneja multiples lineas" {
  printf 'a1|b1|uno\na2|b2|dos\n' | run "$BIN" --tag=current
  [ "$status" -eq 0 ]
  lines=$(echo "$output" | wc -l | tr -d ' ')
  [ "$lines" -eq 2 ]
}

@test "ingesta: linea vacia devuelve exit 2" {
  printf '\n' | run "$BIN" --tag=current
  [ "$status" -eq 2 ]
}

@test "ingesta: linea malformada devuelve exit 3" {
  echo "solo_un_campo" | run "$BIN" --tag=current
  [ "$status" -eq 3 ]
}

@test "ingesta: tag desconocida devuelve exit 4" {
  echo "a|b|c" | run "$BIN" --tag=no-existe
  [ "$status" -eq 4 ]
}

@test "ingesta: --list-tags imprime current" {
  run "$BIN" --list-tags
  [ "$status" -eq 0 ]
  [[ "$output" == *"current"* ]]
}

@test "ingesta: stdin vacio devuelve exit 0 sin output" {
  printf '' | run "$BIN" --tag=current
  [ "$status" -eq 0 ]
  [ -z "$output" ]
}