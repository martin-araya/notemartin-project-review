from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

import pytest

FIXTURE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIXTURE_ROOT))
sys.path.insert(0, str(FIXTURE_ROOT / "src"))

MLRUNS = FIXTURE_ROOT / "mlruns"


@pytest.fixture(scope="session", autouse=True)
def setup_mlflow():
    """Inicializa MLflow file store; limpia antes de la sesion de tests."""
    if MLRUNS.exists():
        shutil.rmtree(MLRUNS, ignore_errors=True)
    MLRUNS.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MLFLOW_TRACKING_URI", f"file://{MLRUNS.resolve()}")
    yield
    # no cleanup; permitimos que mlruns persista para inspeccion


@pytest.fixture
def fastapi_client():
    """FastAPI TestClient (lazy)."""
    from fastapi.testclient import TestClient
    from src.app.main import app

    return TestClient(app)


@pytest.fixture
def iris_data():
    """Carga el dataset iris (150 rows)."""
    import pandas as pd

    return pd.read_csv(FIXTURE_ROOT / "data" / "iris.csv")