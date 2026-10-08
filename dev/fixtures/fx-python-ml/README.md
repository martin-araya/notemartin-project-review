# fx-python-ml

Fixture F06al. Proyecto de ML con notebooks Jupyter, configuracion Hydra, pipeline DVC, tracking MLflow y servicio de inferencia FastAPI. Tres features (`entrenamiento`, `evaluacion`, `inferencia`) con sinonimos neutros CC-11.

## Stack

- Python 3.11-slim
- scikit-learn 1.5 (CPU; sin GPU)
- Hydra 1.3 (Compose API con defaults + overrides)
- DVC 3.5 (file backend; 3 stages: train, evaluate, register)
- MLflow 2.18 (FileStore en `mlruns/`; sin servidor)
- FastAPI 0.115 + uvicorn (servicio de inferencia)
- Jupyter + nbval (notebooks reproducibles)
- pytest 8.2 + pytest-asyncio

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. **E1**: Estado oculto en notebooks (orden de ejecucion via nbval).
2. **E2**: Composición Hydra con `@package _global_` + `defaults:` en `conf/config.yaml`.
3. **E3**: Stages DVC en `dvc.yaml` con `deps`/`outs`/`metrics`.
4. **E4**: Modelos registrados por nombre (`registered_model_name='iris_clf'`) en MLflow.
5. **E5**: Feature engineering duplicado (`src/features.py` con StandardScaler vs `notebooks/02_features.ipynb` con MinMaxScaler).
6. **E6**: `random_state=42` en `src/train.py` para reproducibilidad.

### Paquete (P1‑P6)

1. **P1**: `notebooks/06_setup_with_delete.ipynb` con `del df` que rompe state.
2. **P2**: Hydra override que apunta a un config inexistente.
3. **P3**: DVC stage `register` con `outs` que puede no generarse.
4. **P4**: `notebooks/04_evaluacion_legacy.ipynb` registra con nombre incorrecto `iris_classifier_legacy`.
5. **P5**: Divergencia StandardScaler vs MinMaxScaler produce metricas inconsistentes.
6. **P6**: `src/legacy_train.py` sin `random_state` produce modelos no reproducibles.

### Superficiales (S1‑S3)

1. **S1**: `src/legacy_train.py` declarado pero nunca invocado.
2. **S2**: `notebooks/00_setup.ipynb` solo contiene imports (sin state oculto).
3. **S3**: `tests/test_deprecated.py` con `pytest.skip("placeholder")`.

## Features (sinonimos neutros CC-11)

- **entrenamiento**: `src/train.py` + `notebooks/03_entrenamiento.ipynb` (model + MLflow tracking).
- **evaluacion**: `src/evaluate.py` + `notebooks/04_evaluacion.ipynb` (metrics + log).
- **inferencia**: `src/app/main.py` (FastAPI POST `/inferencia` desde MLflow registry).

## Cómo correr

```bash
docker build -f Dockerfile.test -t npr-fx-python-ml .
docker run --rm -v $(pwd)/.mlruns:/fixture/mlruns npr-fx-python-ml
```

Salida esperada: notebooks ejecutados via `pytest --nbval-lax` + tests pytest OK + `dvc repro` OK + ground truth tests passed.

## Estructura

```
fx-python-ml/
├── Dockerfile.test                python:3.11-slim + deps + dvc init
├── entrypoint.sh                  notebooks + tests + dvc repro + ground truth
├── Makefile                       TEST_CMD, IMAGE_TAG, targets
├── manifest.yml                   requiere linux/macos, container enabled
├── build-history.sh                8 commits reproducibles
├── unique_tokens.txt              33 tokens prefijo NPRGT-FXPML-
├── requirements.txt               scikit-learn, hydra, dvc, mlflow, fastapi, jupyter, nbval, pytest
├── pyproject.toml                 pytest config + pythonpath = [".", "src"]
├── pytest.ini                     nbval config
├── data/
│   └── iris.csv                    150 rows sklearn iris
├── conf/
│   ├── config.yaml                 E2: @package _global_ + defaults
│   ├── entrenamiento/
│   │   ├── default.yaml
│   │   ├── random_forest.yaml
│   │   └── logistic_regression.yaml
│   ├── evaluacion/
│   │   ├── default.yaml
│   │   └── f1.yaml
│   └── inferencia/
│       └── default.yaml            model_name: iris_clf
├── notebooks/
│   ├── 00_setup.ipynb              S2: solo imports
│   ├── 01_exploratorio.ipynb       E1: estado orden
│   ├── 02_features.ipynb           E5: MinMaxScaler
│   ├── 03_entrenamiento.ipynb      E4: MLflow tracking
│   ├── 04_evaluacion.ipynb         E1: log metrics
│   ├── 04_evaluacion_legacy.ipynb  P4: nombre incorrecto
│   ├── 05_inferencia.ipynb         E1: cargar + predict
│   └── 06_setup_with_delete.ipynb   P1: state out-of-order
├── src/
│   ├── __init__.py
│   ├── config.py                   get_param via Hydra Compose
│   ├── features.py                 E5/P5: StandardScaler
│   ├── train.py                    E6: random_state=42
│   ├── evaluate.py                 metricas f1 + accuracy
│   ├── register.py                 mlflow.sklearn.log_model
│   ├── legacy_train.py             S1+P6: sin random_state
│   └── app/
│       └── main.py                 FastAPI POST /inferencia
├── dvc.yaml                        E3: stages train/evaluate/register
├── params.yaml                     parametros versionados
└── tests/
    ├── conftest.py                 fixtures: client, iris_data
    ├── test_train.py
    ├── test_evaluate.py
    ├── test_inference.py            FastAPI TestClient
    ├── test_hydra_config.py
    ├── test_dvc_pipeline.py
    ├── test_mlflow_registry.py
    ├── test_reproducibility.py      P6: random_state
    ├── test_features_divergence.py  P5: StandardScaler vs MinMaxScaler
    ├── test_traps_ecosystem.py      E1..E6
    ├── test_traps_package.py        P1..P6
    ├── test_traps_superficial.py    S1..S3
    └── test_deprecated.py           S3 pytest.skip
```