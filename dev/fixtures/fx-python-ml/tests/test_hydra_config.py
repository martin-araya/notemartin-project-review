from __future__ import annotations

from pathlib import Path

import yaml


CONF_DIR = Path("/fixture/conf")


def test_global_config_exists():
    assert (CONF_DIR / "config.yaml").is_file()


def test_global_config_has_package_marker():
    content = (CONF_DIR / "config.yaml").read_text()
    assert "@package" in content or "_global_" in content


def test_global_config_has_defaults():
    content = (CONF_DIR / "config.yaml").read_text()
    assert "defaults:" in content


def test_entrenamiento_configs_exist():
    for fname in ("default.yaml", "random_forest.yaml", "logistic_regression.yaml"):
        assert (CONF_DIR / "entrenamiento" / fname).is_file()


def test_evaluacion_configs_exist():
    for fname in ("default.yaml", "f1.yaml"):
        assert (CONF_DIR / "evaluacion" / fname).is_file()


def test_inferencia_config_exists():
    assert (CONF_DIR / "inferencia" / "default.yaml").is_file()


def test_random_forest_config_has_n_estimators():
    content = (CONF_DIR / "entrenamiento" / "random_forest.yaml").read_text()
    assert "n_estimators" in content


def test_f1_config_has_average():
    content = (CONF_DIR / "evaluacion" / "f1.yaml").read_text()
    assert "average" in content


def test_inferencia_default_has_model_name():
    content = (CONF_DIR / "inferencia" / "default.yaml").read_text()
    assert "iris_clf" in content


def test_global_config_yaml_is_valid():
    """Verifica que config.yaml parsea como YAML."""
    with (CONF_DIR / "config.yaml").open() as f:
        data = yaml.safe_load(f)
    assert "defaults" in data
    assert "datos" in data
    assert "mlflow" in data