from __future__ import annotations

import pandas as pd
import pytest
from sklearn.datasets import load_iris

from src.evaluate import METRICAS, evaluate_model
from src.train import train_model


@pytest.fixture
def trained_model():
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
    y = pd.Series(iris.target)
    return train_model('random_forest', X, y, random_state=42), X, y


def test_evaluate_f1(trained_model):
    model, X, y = trained_model
    metrics = evaluate_model(model, X, y, metrica='f1', average='weighted')
    assert 'f1' in metrics
    assert 0.0 <= metrics['f1'] <= 1.0


def test_evaluate_accuracy(trained_model):
    model, X, y = trained_model
    metrics = evaluate_model(model, X, y, metrica='accuracy')
    assert 'accuracy' in metrics
    assert 0.0 <= metrics['accuracy'] <= 1.0


def test_evaluate_unknown_metrica(trained_model):
    model, X, y = trained_model
    with pytest.raises(ValueError):
        evaluate_model(model, X, y, metrica='unknown_metric')


def test_evaluate_includes_n_samples(trained_model):
    model, X, y = trained_model
    metrics = evaluate_model(model, X, y, metrica='accuracy')
    assert metrics['n_samples'] == len(y)


def test_metricas_registry():
    assert 'f1' in METRICAS
    assert 'accuracy' in METRICAS