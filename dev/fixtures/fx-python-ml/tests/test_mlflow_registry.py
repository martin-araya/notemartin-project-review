from __future__ import annotations

import os
from pathlib import Path


def test_mlflow_tracking_uri_is_file_scheme():
    """D-423: MLflow usa file store (no servidor)."""
    uri = os.environ.get("MLFLOW_TRACKING_URI", "")
    assert uri.startswith("file://"), f"expected file:// URI, got {uri!r}"


def test_mlflow_mlruns_dir_exists_or_creatable():
    from src.register import track_with_mlflow
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        uri = f"file://{tmp}"
        os.environ["MLFLOW_TRACKING_URI"] = uri
        # solo importamos para verificar que track_with_mlflow no falle de import
        assert callable(track_with_mlflow)


def test_mlflow_artifact_path_uses_models_iris():
    """E4: los modelos usan el nombre 'iris_clf' (no el legacy 'iris_classifier_legacy')."""
    import subprocess
    result = subprocess.run(
        ["grep", "-r", "iris_clf", "/fixture/notebooks", "/fixture/conf", "/fixture/src"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "iris_clf" in result.stdout


def test_register_module_importable():
    from src.register import track_with_mlflow
    assert callable(track_with_mlflow)


def test_legacy_evaluation_uses_wrong_model_name():
    """P4 trap: notebook 04_evaluacion_legacy.ipynb registra con 'iris_classifier_legacy'."""
    content = Path("/fixture/notebooks/04_evaluacion_legacy.ipynb").read_text()
    assert "iris_classifier_legacy" in content