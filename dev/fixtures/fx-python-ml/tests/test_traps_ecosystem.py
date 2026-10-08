from __future__ import annotations

from pathlib import Path


def test_e1_notebooks_exist_in_order():
    """E1: los notebooks core existen con prefijo numerico para orden."""
    notebooks_dir = Path('/fixture/notebooks')
    core = ['01_exploratorio.ipynb', '02_features.ipynb', '03_entrenamiento.ipynb',
            '04_evaluacion.ipynb', '05_inferencia.ipynb']
    for nb in core:
        assert (notebooks_dir / nb).is_file(), f'missing {nb}'


def test_e2_hydra_config_with_package_global():
    """E2: conf/config.yaml usa @package _global_ (Compose API)."""
    content = Path('/fixture/conf/config.yaml').read_text()
    assert '@package' in content or '_global_' in content
    assert 'defaults:' in content
    assert 'Entrenamiento' in content or 'entrenamiento' in content


def test_e2_hydra_subconfigs_exist():
    """E2: hay sub-configs para los overrides."""
    for sub in ['entrenamiento/default.yaml', 'entrenamiento/random_forest.yaml',
                'evaluacion/default.yaml', 'evaluacion/f1.yaml',
                'inferencia/default.yaml']:
        assert Path(f'/fixture/conf/{sub}').is_file()


def test_e3_dvc_yaml_with_stages():
    """E3: dvc.yaml define stages train/evaluate/evaluate."""
    content = Path('/fixture/dvc.yaml').read_text()
    assert 'stages:' in content
    assert 'train:' in content
    assert 'evaluate:' in content
    assert 'register:' in content
    assert 'deps:' in content
    assert 'outs:' in content


def test_e4_mlflow_registers_model_by_name():
    """E4: el modelo se registra por 'iris_clf' via mlflow.sklearn.log_model."""
    import json
    nb03 = json.loads(Path('/fixture/notebooks/03_entrenamiento.ipynb').read_text())
    sources = '\n'.join(
        ''.join(c.get('source', [])) for c in nb03['cells'] if c.get('cell_type') == 'code'
    )
    assert "registered_model_name='iris_clf'" in sources


def test_e5_feature_engineering_duplicated():
    """E5: src/features.py usa StandardScaler, notebook 02_features.ipynb usa MinMaxScaler."""
    src_content = Path('/fixture/src/features.py').read_text()
    assert 'StandardScaler' in src_content
    nb_content = Path('/fixture/notebooks/02_features.ipynb').read_text()
    assert 'MinMaxScaler' in nb_content


def test_e6_random_state_in_train():
    """E6: src/train.py usa random_state para reproducibilidad."""
    content = Path('/fixture/src/train.py').read_text()
    assert 'random_state' in content