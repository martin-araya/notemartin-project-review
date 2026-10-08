from __future__ import annotations

import mlflow
import mlflow.sklearn


def track_with_mlflow(model, X, model_name: str, tracking_uri: str, experiment: str, metrics: dict | None = None) -> str:
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment)
    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "model", registered_model_name=model_name)
        if metrics:
            for k, v in metrics.items():
                mlflow.log_metric(k, v)
    return model_name