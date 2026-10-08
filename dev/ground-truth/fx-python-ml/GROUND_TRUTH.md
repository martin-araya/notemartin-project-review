# Ground Truth: fx-python-ml

Tabla maestra de referencia cruzada para F06al. Cada elemento tiene su id, archivo:línea y descripción.

## Features

- **FEAT-001 entrenamiento** (ingesta-de-ventas): 7 R-NN, 2 decision_points, 7 traces
- **FEAT-002 evaluacion** (modelo-de-clientes): 7 R-NN, 2 decision_points, 7 traces
- **FEAT-003 inferencia** (métricas-diarias): 7 R-NN, 2 decision_points, 7 traces

## Trampas ejercitadas

### Ecosistema (E1‑E6)

| id | where | descripcion |
|---|---|---|
| TRAP-E01 | notebooks/01_exploratorio.ipynb:1 | notebooks ejecutados en orden |
| TRAP-E02 | conf/config.yaml:1 | Hydra Compose con @package _global_ + overrides |
| TRAP-E03 | dvc.yaml:1 | 3 stages: train + evaluate + register |
| TRAP-E04 | notebooks/03_entrenamiento.ipynb:1 | MLflow registered_model_name='iris_clf' |
| TRAP-E05 | src/features.py:9 | StandardScaler (divergencia con MinMaxScaler en notebook) |
| TRAP-E06 | src/train.py:24 | random_state=42 (reproducibilidad) |

### Paquete (P1‑P6)

| id | where | descripcion |
|---|---|---|
| TRAP-P01 | notebooks/06_setup_with_delete.ipynb:1 | del df rompe state out-of-order |
| TRAP-P02 | conf/config.yaml:2 | Hydra override apuntando a config inexistente |
| TRAP-P03 | dvc.yaml:21 | outs: mlruns/.placeholder que puede no crearse |
| TRAP-P04 | notebooks/04_evaluacion_legacy.ipynb:1 | registered_model_name='iris_classifier_legacy' (P4) |
| TRAP-P05 | src/features.py:9 vs notebooks/02_features.ipynb:1 | StandardScaler vs MinMaxScaler divergen |
| TRAP-P06 | src/legacy_train.py:8 | legacy_train sin random_state (S1 dead + P6) |

### Superficiales (S1‑S3)

| id | where | descripcion |
|---|---|---|
| TRAP-S01 | src/legacy_train.py:8 | dead function nunca invocada |
| TRAP-S02 | notebooks/00_setup.ipynb:1 | notebook solo imports |
| TRAP-S03 | tests/test_deprecated.py:1 | pytest.skip placeholder |

## Tests

| file | feature | tests |
|---|---|---|
| tests/test_train.py | FEAT-001 entrenamiento | 5 |
| tests/test_evaluate.py | FEAT-002 evaluacion | 5 |
| tests/test_inference.py | FEAT-003 inferencia | 5 |
| tests/test_hydra_config.py | FEAT-001 entrenamiento (E2) | 10 |
| tests/test_dvc_pipeline.py | FEAT-001 entrenamiento (E3) | 10 |
| tests/test_mlflow_registry.py | FEAT-001 entrenamiento (E4) | 5 |
| tests/test_reproducibility.py | FEAT-001 entrenamiento (E6+P6) | 4 |
| tests/test_features_divergence.py | FEAT-002 evaluacion (P5) | 3 |
| tests/test_traps_ecosystem.py | all (ecosystem) | 7 |
| tests/test_traps_package.py | all (package) | 6 |
| tests/test_traps_superficial.py | all (superficial) | 3 |
| tests/test_deprecated.py | all (deprecated) | 1 |

Total: **64 tests pytest** en `tests/`.