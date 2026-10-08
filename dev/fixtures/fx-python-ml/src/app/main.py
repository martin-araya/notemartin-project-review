from __future__ import annotations

import os

import mlflow
import mlflow.pyfunc
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="fxpm-inference")


class PredictRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class PredictResponse(BaseModel):
    species: str
    model_name: str
    model_version: int | str


def _get_model(name: str, stage: str = "Production"):
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "file:///fixture/mlruns")
    mlflow.set_tracking_uri(tracking_uri)
    model_uri = f"models:/{name}@{stage.lower()}"
    try:
        return mlflow.pyfunc.load_model(model_uri)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"model {model_uri} not found: {e}")


@app.get("/")
def root():
    return {"status": "ok", "service": "fxpm-inference"}


@app.post("/inferencia", response_model=PredictResponse)
def predict(req: PredictRequest, model_name: str = "iris_clf"):
    model = _get_model(model_name, "production")
    df = pd.DataFrame([req.model_dump()])
    pred = model.predict(df)[0]
    return PredictResponse(species=str(pred), model_name=model_name, model_version=1)