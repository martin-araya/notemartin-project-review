#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06al.
set -euo pipefail
cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

# Commit 1: scaffold
git add .gitignore README.md manifest.yml Makefile Dockerfile.test \
        entrypoint.sh requirements.txt unique_tokens.txt \
        pyproject.toml pytest.ini
git commit -q -m "chore: initial scaffold (deps + dockerfile + entrypoint)"

# Commit 2: data + Hydra configs (E2)
git add data/iris.csv conf/
git commit -q -m "feat(config): iris dataset + Hydra Compose config (E2)"

# Commit 3: src/ + notebooks (E1, E4, E5)
git add src/__init__.py src/config.py src/train.py src/evaluate.py \
        src/features.py src/register.py \
        src/app/__init__.py src/app/main.py \
        notebooks/00_setup.ipynb notebooks/01_exploratorio.ipynb \
        notebooks/02_features.ipynb notebooks/03_entrenamiento.ipynb \
        notebooks/04_evaluacion.ipynb notebooks/05_inferencia.ipynb
git commit -q -m "feat(ml): src modules + notebooks core (E1, E4, E5)"

# Commit 4: DVC pipeline (E3)
git add dvc.yaml params.yaml metrics/ notebooks/04_evaluacion_legacy.ipynb
git commit -q -m "feat(dvc): pipeline stages + legacy eval notebook (E3 + P4)"

# Commit 5: P1 trap notebook + S1 dead legacy_train
git add notebooks/06_setup_with_delete.ipynb src/legacy_train.py
git commit -q -m "feat(traps): P1 delete-state notebook + S1 dead legacy_train"

# Commit 6: FastAPI app (ya en commit 3; resta ajustar flag)
git commit -q --allow-empty -m "feat(serve): FastAPI POST /inferencia from MLflow registry (E4)"

# Commit 7: tests
git add tests/__init__.py tests/conftest.py tests/test_train.py tests/test_evaluate.py \
        tests/test_inference.py tests/test_hydra_config.py tests/test_dvc_pipeline.py \
        tests/test_mlflow_registry.py tests/test_reproducibility.py \
        tests/test_features_divergence.py tests/test_traps_ecosystem.py \
        tests/test_traps_package.py tests/test_traps_superficial.py tests/test_deprecated.py
git commit -q -m "test: 13 test files (train/evaluate/inference/hydra/dvc/mlflow/reproducibility/features/ecosystem/package/superficial/deprecated)"

# Commit 8: tools (opcional)
git commit -q --allow-empty -m "chore: entrypoint wraps notebooks + tests + dvc repro"

echo "Historia creada con 8 commits:"
git log --oneline