from __future__ import annotations

from pathlib import Path


DVC_YAML = Path("/fixture/dvc.yaml")
PARAMS_YAML = Path("/fixture/params.yaml")


def test_dvc_yaml_exists():
    assert DVC_YAML.is_file()


def test_dvc_yaml_has_stages():
    content = DVC_YAML.read_text()
    assert "stages:" in content


def test_dvc_yaml_train_stage():
    content = DVC_YAML.read_text()
    assert "train:" in content
    assert "deps:" in content
    assert "outs:" in content


def test_dvc_yaml_evaluate_stage():
    content = DVC_YAML.read_text()
    assert "evaluate:" in content
    assert "metrics:" in content


def test_dvc_yaml_register_stage():
    content = DVC_YAML.read_text()
    assert "register:" in content


def test_dvc_yaml_has_data_iris():
    content = DVC_YAML.read_text()
    assert "iris.csv" in content


def test_dvc_yaml_has_src_train_dep():
    content = DVC_YAML.read_text()
    assert "src/train.py" in content


def test_params_yaml_exists():
    assert PARAMS_YAML.is_file()


def test_params_yaml_has_seed():
    content = PARAMS_YAML.read_text()
    assert "semilla" in content
    assert "42" in content


def test_params_yaml_has_entrenamiento():
    content = PARAMS_YAML.read_text()
    assert "entrenamiento:" in content
    assert "algoritmo" in content