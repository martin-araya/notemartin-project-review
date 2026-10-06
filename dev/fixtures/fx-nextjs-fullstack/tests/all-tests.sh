#!/usr/bin/env bash
# Corre los tests del fixture fx-nextjs-fullstack.
# - vitest: corre tests/unit/ (validacion contra el codigo fuente).
# - playwright: se omite si Playwright no esta disponible (npm install
#   puede haber fallado en el contenedor).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
cd "$ROOT"

FAIL=0

echo "=== vitest (unit) ==="
if ! npx vitest run --reporter=verbose 2>&1; then
  FAIL=1
fi

if [ "$FAIL" -ne 0 ]; then
  echo ""
  echo "FAIL: vitest fallo"
  exit 1
fi
echo ""
echo "OK: all vitest passed"