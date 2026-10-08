from __future__ import annotations

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from src.features import engineer_features_v1


def test_src_features_uses_standard_scaler():
    """E5/P5: src/features.py usa StandardScaler."""
    df = pd.DataFrame({
        'sepal_length': [5.1, 4.9, 4.7],
        'sepal_width': [3.5, 3.0, 3.2],
        'species': ['a', 'b', 'c'],
    })
    out = engineer_features_v1(df.copy())
    assert 'species' in out.columns
    numeric = [c for c in out.columns if c != 'species']
    # StandardScaler: media ~ 0, std ~ 1
    for col in numeric:
        assert abs(out[col].mean()) < 1e-6


def test_notebook_features_uses_minmax_scaler():
    """E5: 02_features.ipynb usa MinMaxScaler (divergente)."""
    import json
    with open('/fixture/notebooks/02_features.ipynb') as f:
        nb = json.load(f)
    sources = '\n'.join(
        ''.join(c.get('source', [])) for c in nb['cells'] if c.get('cell_type') == 'code'
    )
    assert 'MinMaxScaler' in sources
    assert 'StandardScaler' not in sources


def test_features_divergence_produces_different_outputs():
    """P5: StandardScaler vs MinMaxScaler sobre los mismos datos produce resultados distintos."""
    df = pd.DataFrame({
        'a': [10.0, 20.0, 30.0, 40.0],
    })
    standard = StandardScaler().fit_transform(df[['a']]).flatten()
    minmax = MinMaxScaler().fit_transform(df[['a']]).flatten()
    # Mismo rango pero diferente distribucion
    assert standard[2] != minmax[2]  # valores del medio son diferentes
    assert abs(standard.max()) < 1e-6  # StandardScaler normaliza a std 1