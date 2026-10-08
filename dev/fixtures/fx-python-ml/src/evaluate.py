from __future__ import annotations

from typing import Any, Callable

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

METRICAS: dict[str, Callable] = {
    "f1": f1_score,
    "accuracy": accuracy_score,
}


def evaluate_model(
    model,
    X: pd.DataFrame,
    y: pd.Series,
    metrica: str = "f1",
    **kwargs: Any,
) -> dict[str, float]:
    if metrica not in METRICAS:
        raise ValueError(f"metrica desconocida: {metrica}")
    y_pred = model.predict(X)
    fn = METRICAS[metrica]
    score = fn(y, y_pred, **kwargs)
    return {metrica: float(score), "n_samples": int(len(y))}