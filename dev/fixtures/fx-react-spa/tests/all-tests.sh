#!/usr/bin/env bash
# Corre los tests vitest del fixture fx-react-spa.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
cd "$ROOT"

FAIL=0

if ! npx vitest run --reporter=verbose 2>&1; then
  FAIL=1
fi

if [ "$FAIL" -ne 0 ]; then
  echo ""
  echo "FAIL: some vitest tests failed"
  exit 1
fi
echo ""
echo "OK: all vitest tests passed"