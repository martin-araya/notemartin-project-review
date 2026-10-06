#!/usr/bin/env bash
# Tests del binario Go stripped (trampa #2 del ecosistema aplicada a binarios).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
BIN="$ROOT/artifacts/app"

if [ ! -f "$BIN" ]; then
  echo "SKIP: $BIN missing (run build/build-all.sh)"
  exit 0
fi

FAIL=0

MAGIC=$(head -c 4 "$BIN" | od -An -tx1 | tr -d ' ')
if [ "$MAGIC" != "7f454c46" ]; then
  echo "FAIL: bad magic: $MAGIC (expected 7f454c46 = ELF)"
  FAIL=1
else
  echo "OK: magic is ELF"
fi

FILE_TYPE=$(file -b "$BIN")
if echo "$FILE_TYPE" | grep -q "ELF.*executable"; then
  echo "OK: file -b says ELF executable"
else
  echo "FAIL: file -b does not say ELF: $FILE_TYPE"
  FAIL=1
fi

if nm "$BIN" 2>&1 | grep -qE "CalcularTarifa|ValidarLicencia|Sincronizar"; then
  echo "FAIL: nm found feature names in symbol table (should be stripped)"
  FAIL=1
else
  echo "OK: nm does not reveal feature names (stripped)"
fi

LITERALS_FOUND=0
STRINGS_TMP=$(mktemp)
strings -a -n 4 "$BIN" > "$STRINGS_TMP"
for lit in "calcular_tarifa" "validar_licencia" "sincronizar" \
          "FXMIN_TARIFA_PREFIX" "FXMIN_TARIFA_SUFFIX" \
          "FXMIN_LIC_INVALID" "FXMIN_SYNC_OK" "FXMIN_SYNC_ERROR"; do
  if grep -qF "$lit" "$STRINGS_TMP"; then
    LITERALS_FOUND=$((LITERALS_FOUND + 1))
  else
    echo "FAIL: literal $lit not found via strings"
    FAIL=1
  fi
done
rm -f "$STRINGS_TMP"
echo "OK: $LITERALS_FOUND/8 literals found via strings"

if [ $FAIL -ne 0 ]; then
  echo ""
  echo "GO BINARY TESTS: FAILED"
  exit 1
fi
echo ""
echo "GO BINARY TESTS: OK"