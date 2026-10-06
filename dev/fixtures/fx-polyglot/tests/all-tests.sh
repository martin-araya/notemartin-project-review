#!/usr/bin/env bash
# Corre todos los bats del fixture fx-polyglot.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
cd "$ROOT"

FAIL=0

if [ ! -x "$(which bats 2>/dev/null || true)" ]; then
  echo "SKIP: bats no instalado"
  exit 1
fi

if ! bats tests/; then
  FAIL=1
fi

if [ "$FAIL" -ne 0 ]; then
  echo ""
  echo "FAIL: some bats failed"
  exit 1
fi
echo ""
echo "OK: all bats passed"