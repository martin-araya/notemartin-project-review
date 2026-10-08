#!/usr/bin/env bash
# Limpia artefactos generados.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[reset_workspace] removing dev.duckdb..."
rm -f /fixture/dev.duckdb
echo "[reset_workspace] removing dbt/dbt_packages..."
rm -rf /fixture/dbt/dbt_packages
echo "[reset_workspace] removing dbt/target..."
rm -rf /fixture/dbt/target
echo "[reset_workspace] removing dbt/logs..."
rm -rf /fixture/dbt/logs
echo "[reset_workspace] removing .airflow..."
rm -rf /fixture/.airflow
echo "[reset_workspace] removing Generated/..."
rm -rf /fixture/Generated
echo "[reset_workspace] done."