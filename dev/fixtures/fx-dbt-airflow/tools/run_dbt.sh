#!/usr/bin/env bash
# Ejecuta dbt deps + dbt seed + dbt build (run + test).
set -euo pipefail
cd "$(dirname "$0")/.."

export DBT_PROFILES_DIR=/fixture

echo "[run_dbt] dbt deps..."
dbt deps --project-dir /fixture/dbt || true

echo "[run_dbt] dbt seed..."
dbt seed --project-dir /fixture/dbt --profiles-dir .

echo "[run_dbt] dbt build (run + test)..."
dbt build --project-dir /fixture/dbt --profiles-dir .

echo "[run_dbt] done."