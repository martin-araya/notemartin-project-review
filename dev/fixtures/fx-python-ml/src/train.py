from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

ALGORITMOS: dict[str, type] = {
    "random_forest": RandomForestClassifier,
    "logistic_regression": LogisticRegression,
}


def _default_kwargs(algorithm: str) -> dict[str, Any]:
    if algorithm == "random_forest":
        return {"n_estimators": 100}
    if algorithm == "logistic_regression":
        return {"max_iter": 1000}
    return {}


def train_model(
    algorithm: str,
    X: pd.DataFrame,
    y: pd.Series,
    random_state: int = 42,
    **kwargs: Any,
):
    if algorithm not in ALGORITMOS:
        raise ValueError(f"algoritmo desconocido: {algorithm}")
    cls = ALGORITMOS[algorithm]
    params = {"random_state": random_state}
    params.update(_default_kwargs(algorithm))
    params.update(kwargs)
    model = cls(**params)
    model.fit(X, y)
    return model