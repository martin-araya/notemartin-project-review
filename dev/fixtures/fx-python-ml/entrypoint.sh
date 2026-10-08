#!/usr/bin/env bash
# Entrypoint: notebooks via nbval + pytest + dvc repro + ground truth tests.
set -euo pipefail
cd "$(dirname "$0")"

export PYTHONPATH=/fixture
export MLFLOW_TRACKING_URI="file:///fixture/mlruns"

echo "[entrypoint] executing notebooks with pytest --nbval-lax..."
pytest --nbval-lax notebooks/ -q || true

echo "[entrypoint] executing unit + integration tests..."
pytest tests/ -q

echo "[entrypoint] dvc repro (smoke)..."
dvc repro -q 2>&1 | tail -5 || true

echo "[entrypoint] ground truth tests..."
pytest dev/tests/test_fx_python_ml_ground_truth.py -q

echo "[entrypoint] done."