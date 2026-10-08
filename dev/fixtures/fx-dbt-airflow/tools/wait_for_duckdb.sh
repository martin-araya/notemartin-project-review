#!/usr/bin/env bash
# Smoke test: verifica que dev.duckdb existe y es accesible.
set -euo pipefail
cd "$(dirname "$0")/.."

DUCKDB_PATH="${DUCKDB_PATH:-/fixture/dev.duckdb}"

if [ ! -f "$DUCKDB_PATH" ]; then
    echo "ERROR: $DUCKDB_PATH does not exist" >&2
    exit 1
fi

echo "DuckDB OK: $DUCKDB_PATH"
python3 -c "import duckdb; con = duckdb.connect('$DUCKDB_PATH'); print(con.execute('SHOW TABLES').fetchall())"