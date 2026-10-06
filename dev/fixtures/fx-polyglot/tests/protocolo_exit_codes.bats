#!/usr/bin/env bats
# Tests de los exit codes como protocolo (trampa #5 del ecosistema).
# Cada binario devuelve un codigo distinto segun el tipo de error.

@test "ingesta: exit 2 para linea vacia" {
  [ -x "$(which ingesta || true)" ] || skip "ingesta no instalado"
  printf '' | run ingesta --tag=current
  [ "$status" -eq 0 ]
  printf '\n' | run ingesta --tag=current
  [ "$status" -eq 2 ]
}

@test "ingesta: exit 3 para linea malformada" {
  [ -x "$(which ingesta || true)" ] || skip "ingesta no instalado"
  echo "solo_un_campo" | run ingesta --tag=current
  [ "$status" -eq 3 ]
}

@test "ingesta: exit 4 para tag desconocida" {
  [ -x "$(which ingesta || true)" ] || skip "ingesta no instalado"
  echo "a|b|c" | run ingesta --tag=no-existe
  [ "$status" -eq 4 ]
}

@test "transformacion v1: exit 8 para JSON malformado" {
  [ -x "$(which transformacion-linux || true)" ] || skip "transformacion-linux no instalado"
  echo "no es json" | run transformacion-linux
  [ "$status" -eq 8 ]
}

@test "transformacion v2: exit 64 para campo extra con strict" {
  [ -x "$(which transformacion-linux-v2 || true)" ] || skip "transformacion-linux-v2 no instalado"
  echo '{"id":"a","payload":"x","extra":"y"}' | run transformacion-linux-v2
  [ "$status" -eq 64 ]
}

@test "transformacion v1: exit 2 para linea vacia" {
  [ -x "$(which transformacion-linux || true)" ] || skip "transformacion-linux no instalado"
  printf '\n' | run transformacion-linux
  [ "$status" -eq 2 ]
}