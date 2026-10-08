from __future__ import annotations

import pandas as pd
from sklearn.preprocessing import StandardScaler


def engineer_features_v1(df: pd.DataFrame) -> pd.DataFrame:
    """Feature engineering usado por el codigo de produccion (StandardScaler).

    E5 trampa: notebook 02_features.ipynb usa MinMaxScaler; los P6/P5 detectan
    la divergencia que produce metricas inconsistentes entre notebook y src.
    """
    numeric_cols = [c for c in df.columns if c != "species"]
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df


def split_features_target(df: pd.DataFrame, target: str = "species"):
    """Separa X / y. Asume que df tiene columna target."""
    y = df[target]
    X = df.drop(columns=[target])
    return X, y


def load_csv(path: str) -> pd.DataFrame:
    """Carga CSV desde path."""
    return pd.read_csv(path)