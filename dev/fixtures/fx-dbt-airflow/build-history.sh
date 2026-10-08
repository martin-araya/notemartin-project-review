#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06ak.
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
        entrypoint.sh requirements.txt profiles.yml .airflowignore \
        unique_tokens.txt
git commit -q -m "chore: initial scaffold (dbt + airflow + profiles)"

# Commit 2: dbt sources + staging (E1)
git add dbt/dbt_project.yml dbt/packages.yml \
        dbt/models/staging/_sources.yml \
        dbt/models/staging/stg_ventas.sql \
        dbt/models/staging/stg_clientes.sql \
        dbt/seeds/seed_clientes.csv dbt/seeds/seed_catalogo.csv
git commit -q -m "feat(dbt): sources + staging models con ref/source (E1)"

# Commit 3: intermediate + marts + incremental (E3)
git add dbt/models/intermediate/int_ventas_clientes.sql \
        dbt/models/marts/marts_ventas/ \
        dbt/models/marts/marts_clientes/ \
        dbt/models/marts/marts_incremental/
git commit -q -m "feat(dbt): intermediate + marts + incremental models (E3)"

# Commit 4: macros + tests + snapshots
git add dbt/macros/centros_normalizados.sql \
        dbt/macros/centros_concat.sql \
        dbt/macros/legacy_helper.sql \
        dbt/tests/ dbt/snapshots/
git commit -q -m "feat(dbt): macros (E2 + P1) + tests + snapshots + legacy helper (S1)"

# Commit 5: airflow DAG estatico (extract/transform/load)
git add airflow/dags/etl_dag.py
git commit -q -m "feat(airflow): DAG estatico etl_dag con xcom_push correcto"

# Commit 6: DAG factory desde YAML (E5) + xcom implicit (P6)
git add airflow/dags/dag_factory.py \
        airflow/dags/generated_etl_dag.py \
        airflow/dags/etl_config.yaml \
        airflow/dags/transform_xcom_implicit.py
git commit -q -m "feat(airflow): DAG factory desde YAML (E5) + xcom implicit (P6)"

# Commit 7: legacy purge DAG (S2) + airflow tests
git add airflow/legacy_purge_dag.py airflow/tests/
git commit -q -m "feat(airflow): legacy_purge_dag (S2) + airflow tests (8 archivos)"

# Commit 8: tools + metricas marts
git add tools/ dbt/models/marts/marts_metricas/
git commit -q -m "chore: shell wrappers + metricas marts + readme"

echo "Historia creada con 8 commits:"
git log --oneline