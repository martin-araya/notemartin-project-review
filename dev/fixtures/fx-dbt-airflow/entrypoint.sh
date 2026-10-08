#!/usr/bin/env bash
# Entrypoint: dbt seed + build + test + airflow dags parse + pytest.
set -euo pipefail
cd "$(dirname "$0")"

export AIRFLOW_HOME=/fixture/.airflow
export DBT_PROFILES_DIR=/fixture

echo "[entrypoint] dbt seed + build + test..."
bash tools/run_dbt.sh

echo "[entrypoint] airflow dags parse + airflow tests..."
bash tools/run_airflow_tests.sh

echo "[entrypoint] ground truth tests..."
pytest dev/tests/test_fx_dbt_airflow_ground_truth.py -q

echo "[entrypoint] done."