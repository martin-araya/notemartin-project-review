from __future__ import annotations

import json
from pathlib import Path


def test_p1_notebook_with_delete_state():
    """P1 trap: notebook 06_setup_with_delete.ipynb tiene `del df`."""
    nb = json.loads(Path('/fixture/notebooks/06_setup_with_delete.ipynb').read_text())
    sources = '\n'.join(
        ''.join(c.get('source', [])) for c in nb['cells'] if c.get('cell_type') == 'code'
    )
    assert 'del df' in sources


def test_p2_hydra_override_can_break_chain():
    """P2 trap: conf/entrenamiento/default.yaml puede ser overrideado con config inexistente."""
    # Verifica que la estructura permite apuntar a un archivo que no existe
    content = Path('/fixture/conf/entrenamiento/default.yaml').read_text()
    # Solo documentacion: el override es valido si Hydra puede resolverlo.
    # El test verifica que el archivo existe y es parseable.
    assert 'algoritmo' in content


def test_p3_dvc_stage_outs_exist():
    """P3 trap: dvc.yaml stage `register` declara outs pero puede no crearse correctamente."""
    content = Path('/fixture/dvc.yaml').read_text()
    assert 'register:' in content
    assert 'outs:' in content


def test_p4_legacy_notebook_registers_with_wrong_name():
    """P4 trap: notebook 04_evaluacion_legacy.ipynb registra con 'iris_classifier_legacy'."""
    nb = json.loads(Path('/fixture/notebooks/04_evaluacion_legacy.ipynb').read_text())
    sources = '\n'.join(
        ''.join(c.get('source', [])) for c in nb['cells'] if c.get('cell_type') == 'code'
    )
    assert 'iris_classifier_legacy' in sources


def test_p5_feature_divergence_documented():
    """P5 trap: src usa StandardScaler y notebook MinMaxScaler (divergencia)."""
    src = Path('/fixture/src/features.py').read_text()
    nb = Path('/fixture/notebooks/02_features.ipynb').read_text()
    assert 'StandardScaler' in src
    assert 'MinMaxScaler' in nb
    assert 'StandardScaler' not in nb


def test_p6_legacy_train_no_random_state():
    """P6 trap: src/legacy_train.py no acepta random_state."""
    content = Path('/fixture/src/legacy_train.py').read_text()
    # legacy_train firma debe ser (X, y) sin random_state
    assert 'def legacy_train' in content
    # Verificar SOLO la firma de la funcion, no los comentarios/docstring
    import re
    fn_match = re.search(r"def legacy_train\([^)]*\)", content)
    assert fn_match is not None, 'def legacy_train no encontrada'
    assert 'random_state' not in fn_match.group(0), 'firma incluye random_state'