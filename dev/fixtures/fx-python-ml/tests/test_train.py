from __future__ import annotations

import pandas as pd
import pytest
from sklearn.datasets import load_iris

from src.train import ALGORITMOS, train_model


def _get_iris_xy():
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
    y = pd.Series(iris.target)
    return X, y


def test_train_random_forest():
    X, y = _get_iris_xy()
    model = train_model('random_forest', X, y, random_state=42)
    preds = model.predict(X)
    assert len(preds) == len(y)
    assert (preds == y).mean() > 0.9


def test_train_logistic_regression():
    X, y = _get_iris_xy()
    model = train_model('logistic_regression', X, y, random_state=42)
    preds = model.predict(X)
    assert len(preds) == len(y)


def test_train_unknown_algorithm():
    X, y = _get_iris_xy()
    with pytest.raises(ValueError):
        train_model('unknown_algo', X, y)


def test_train_with_kwargs():
    X, y = _get_iris_xy()
    model = train_model('random_forest', X, y, n_estimators=10)
    assert model.n_estimators == 10


def test_train_uses_random_state():
    """E6: random_state se aplica al modelo."""
    X, y = _get_iris_xy()
    model_a = train_model('random_forest', X, y, random_state=42)
    model_b = train_model('random_forest', X, y, random_state=42)
    preds_a = model_a.predict(X)
    preds_b = model_b.predict(X)
    assert (preds_a == preds_b).all()


def test_algoritmos_registry():
    assert 'random_forest' in ALGORITMOS
    assert 'logistic_regression' in ALGORITMOS