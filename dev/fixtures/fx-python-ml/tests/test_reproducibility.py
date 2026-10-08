from __future__ import annotations

import pandas as pd
import pytest
from sklearn.datasets import load_iris

from src.train import train_model


def _get_iris_xy():
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
    y = pd.Series(iris.target)
    return X, y


def test_reproducibility_same_seed():
    X, y = _get_iris_xy()
    model_a = train_model('random_forest', X, y, random_state=42)
    model_b = train_model('random_forest', X, y, random_state=42)
    preds_a = model_a.predict(X)
    preds_b = model_b.predict(X)
    assert (preds_a == preds_b).all()


def test_random_state_default_is_42():
    """E6: el default random_state debe ser 42."""
    import inspect
    from src.train import train_model
    sig = inspect.signature(train_model)
    assert sig.parameters['random_state'].default == 42


def test_legacy_train_has_no_random_state():
    """P6 adyacente: legacy_train no acepta random_state."""
    import inspect
    from src.legacy_train import legacy_train
    sig = inspect.signature(legacy_train)
    assert 'random_state' not in sig.parameters


def test_legacy_train_is_dead():
    """S1: legacy_train no se invoca desde ningun modulo activo."""
    from pathlib import Path
    src_files = list(Path('/fixture/src').rglob('*.py'))
    invoked = []
    for path in src_files:
        if path.name == 'legacy_train.py':
            continue
        content = path.read_text(encoding='utf-8', errors='replace')
        if 'legacy_train' in content and 'import' in content:
            invoked.append(path.name)
    assert invoked == [], f"legacy_train is invoked from: {invoked}"