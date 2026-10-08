#!/usr/bin/env bash
# Valida DAGs con airflow dags parse + ejecuta tests pytest.
set -euo pipefail
cd "$(dirname "$0")/.."

export AIRFLOW_HOME=/fixture/.airflow
export DBT_PROFILES_DIR=/fixture

echo "[run_airflow_tests] airflow dags parse..."
airflow dags parse /fixture/airflow/dags/

echo "[run_airflow_tests] pytest airflow/tests/..."
pytest airflow/tests/ -q

echo "[run_airflow_tests] done."