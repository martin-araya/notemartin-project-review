# Ground Truth: fx-dbt-airflow

Tabla maestra de referencia cruzada para F06ak. Cada elemento tiene su id, archivo:línea y descripción.

## Entry points (resumen)

- 23 entry points en dbt (project.yml, packages.yml, sources, 11 modelos, 3 macros, 4 seeds, 3 tests, 1 snapshot)
- 8 entry points en airflow (etl_dag, dag_factory, etl_config.yaml, generated_etl_dag, transform_xcom_implicit, legacy_purge_dag, 2 wrappers)
- 4 entry points en config (profiles.yml, requirements.txt, .airflowignore, entrypoint.sh)
- 8 entry points en tests (8 archivos pytest)
- 4 entry points en tools

## Features

- **FEAT-001 ventas** (ingesta-de-ventas): 7 R-NN, 2 decision_points, 7 traces
- **FEAT-002 clientes** (modelo-de-clientes): 7 R-NN, 1 decision_point, 7 traces
- **FEAT-003 metricas** (métricas-diarias): 7 R-NN, 2 decision_points, 7 traces

## Trampas ejercitadas

### Ecosistema (E1‑E6)

| id | where | descripcion |
|---|---|---|
| TRAP-E01 | dbt/models/staging/stg_ventas.sql:2 | {{ source('raw','ventas_raw') }} sin FK en la base |
| TRAP-E02 | dbt/macros/centros_normalizados.sql:1 | macro Jinja parametrizado |
| TRAP-E03 | dbt/models/marts/marts_incremental/ventas_diarias_incremental.sql:8 | is_incremental() branch |
| TRAP-E04 | dbt/dbt_project.yml:24 | materialization por carpeta |
| TRAP-E05 | airflow/dags/dag_factory.py:9 | DAG factory desde YAML |
| TRAP-E06 | airflow/dags/etl_dag.py:30 | xcom_push/pull explicito |

### Paquete (P1‑P6)

| id | where | descripcion |
|---|---|---|
| TRAP-P01 | dbt/macros/centros_concat.sql:3 | concat string `~` (SQLi) |
| TRAP-P02 | dbt/models/marts/marts_incremental/ventas_diarias_incremental_buggy.sql:8 | is_incremental() con where 1=1 |
| TRAP-P03 | dbt/macros/legacy_helper.sql:1 | dead macro helper |
| TRAP-P04 | dbt/dbt_project.yml:26 | materialization inconsistency incremental vs table |
| TRAP-P05 | airflow/legacy_purge_dag.py:13 | DAG con catchup=False + start_date=2019 |
| TRAP-P06 | airflow/dags/transform_xcom_implicit.py:11 | return dict no serializable |

### Superficiales (S1‑S3)

| id | where | descripcion |
|---|---|---|
| TRAP-S01 | dbt/macros/legacy_helper.sql:1 | macro nunca invocado |
| TRAP-S02 | airflow/legacy_purge_dag.py:13 | DAG nunca corre |
| TRAP-S03 | airflow/tests/test_deprecated.py:1 | test con pytest.skip |

## Call graph

| from | to | kind |
|---|---|---|
| EP-airflow-etl-dag | EP-dbt-build-jobs | BashOperator |
| EP-airflow-etl-dag | EP-dbt-stg-ventas | XCOM_PUSH |
| EP-airflow-etl-dag | EP-dbt-stg-ventas | XCOM_PULL |
| EP-airflow-dag-factory | EP-airflow-etl-config-yaml | YAML_PARSE |
| EP-airflow-dag-factory | EP-airflow-generated-etl-dag | DAG_BUILD |
| EP-dbt-stg-ventas | EP-dbt-sources | REF_SOURCE |
| EP-dbt-stg-clientes | EP-dbt-sources | REF_SOURCE |
| EP-dbt-int-ventas-clientes | EP-dbt-stg-ventas | REF |
| EP-dbt-int-ventas-clientes | EP-dbt-stg-clientes | REF |
| EP-dbt-ventas-diarias | EP-dbt-int-ventas-clientes | REF |
| EP-dbt-clientes-top | EP-dbt-int-ventas-clientes | REF |
| EP-dbt-metricas-diarias | EP-dbt-ventas-diarias | REF |
| EP-dbt-metricas-diarias | EP-dbt-macro-centros-normalizados | MACRO_INVOKE |
| EP-dbt-ventas-diarias-incremental | EP-dbt-int-ventas-clientes | REF |
| EP-dbt-snapshot-ventas | EP-dbt-sources | REF_SOURCE |
| EP-dbt-seed-clientes | EP-dbt-stg-clientes | SEED_LOAD |

## Tests

| file | feature | tests |
|---|---|---|
| airflow/tests/test_etl_dag.py | FEAT-001 ventas | 6 |
| airflow/tests/test_dag_factory.py | FEAT-001 ventas (E5) | 5 |
| airflow/tests/test_xcom_explicit.py | FEAT-001 ventas (E6) | 3 |
| airflow/tests/test_xcom_implicit.py | FEAT-001 ventas (P6) | 5 |
| airflow/tests/test_traps_ecosystem.py | all (ecosystem) | 6 |
| airflow/tests/test_traps_package.py | all (package) | 6 |
| airflow/tests/test_deprecated.py | all (deprecated) | 1 |

Total: **32 tests pytest** en airflow/tests/.