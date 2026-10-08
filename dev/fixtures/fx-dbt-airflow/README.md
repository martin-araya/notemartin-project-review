# fx-dbt-airflow

Fixture F06ak. Pipeline analitico con **dbt** (SQL + Jinja), **Apache Airflow** (Python DAGs) y **DuckDB** como base embebida. Cubre linaje declarativo via `ref()`/`source()`, macros Jinja, materialización por carpeta, `is_incremental()`, DAG generado desde YAML y XCom entre tareas.

## Stack

- dbt-core 1.8 + dbt-duckdb 1.8
- Apache Airflow 2.9 (DAGs parseados offline; NO se levanta el scheduler)
- DuckDB (base analitica embebida en `/fixture/dev.duckdb`)
- Python 3.11-slim
- pytest 8.2 + dbt built-in tests

## Estructura

```
fx-dbt-airflow/
├── Dockerfile.test                python:3.11-slim + dbt + apache-airflow
├── entrypoint.sh                  dbt seed + build + airflow dags parse + pytest
├── Makefile                       TEST_CMD, IMAGE_TAG, targets
├── manifest.yml                   requiere linux/macos, container enabled
├── build-history.sh                8 commits reproducibles
├── unique_tokens.txt              34 tokens prefijo NPRGT-FXDBAIR-
├── requirements.txt               dbt-core, dbt-duckdb, apache-airflow, pytest
├── profiles.yml                   target dev (DuckDB) + test (:memory:)
├── .airflowignore                 excluye generated_etl_dag.py
├── dbt/
│   ├── dbt_project.yml            materialization por carpeta (E4)
│   ├── packages.yml               dbt-labs/dbt_utils
│   ├── models/
│   │   ├── staging/
│   │   │   ├── _sources.yml       source('raw', 'ventas_raw') (E1)
│   │   │   ├── stg_ventas.sql     {{ source() }} (E1)
│   │   │   └── stg_clientes.sql   {{ source() }} (E1)
│   │   ├── intermediate/
│   │   │   └── int_ventas_clientes.sql  {{ ref() }} (E1)
│   │   └── marts/
│   │       ├── marts_ventas/
│   │       │   ├── ventas_diarias.sql        table
│   │       │   └── ventas_mensuales.sql      view (override)
│   │       ├── marts_clientes/
│   │       │   └── clientes_top.sql          table
│   │       ├── marts_metricas/
│   │       │   └── metricas_diarias.sql      table + macro Jinja (E2)
│   │       └── marts_incremental/
│   │           ├── ventas_diarias_incremental.sql        is_incremental correcto (E3)
│   │           └── ventas_diarias_incremental_buggy.sql  P2 trap (where 1=1)
│   ├── macros/
│   │   ├── centros_normalizados.sql          macro Jinja parametrizado (E2)
│   │   ├── centros_concat.sql                macro con concat string (P1 SQLi)
│   │   └── legacy_helper.sql                 S1 dead
│   ├── seeds/
│   │   ├── seed_clientes.csv                 5 clientes (CC-11 safe: nombres neutros)
│   │   ├── seed_catalogo.csv                 10 productos
│   │   ├── seed_cliente_venta.csv            13 enlaces cliente-venta
│   │   └── ventas_raw.csv                    12 ventas raw (origen del source)
│   ├── tests/
│   │   ├── singular/
│   │   │   ├── assert_ventas_positivas.sql
│   │   │   └── assert_clientes_activos.sql
│   │   └── generic/
│   │       └── freshness_24h.sql             custom generic test
│   └── snapshots/
│       └── snap_ventas.sql                    snapshot timestamp
├── airflow/
│   ├── dags/
│   │   ├── etl_dag.py                         DAG estatico extract/transform/load
│   │   ├── dag_factory.py                     build_dag_from_yaml() (E5)
│   │   ├── etl_config.yaml                    spec del DAG generado (E5)
│   │   ├── generated_etl_dag.py               wrapper que invoca dag_factory (E5)
│   │   ├── transform_xcom_implicit.py         P6 trap (return dict no serializable)
│   │   └── legacy_purge_dag.py                S2 (start_date 2019 + catchup=False)
│   ├── legacy_purge_dag.py                    S2
│   └── tests/
│       ├── conftest.py                        DagBag fixture
│       ├── test_etl_dag.py                     6 tests
│       ├── test_dag_factory.py                5 tests
│       ├── test_xcom_explicit.py              3 tests (E6)
│       ├── test_xcom_implicit.py              5 tests (P6)
│       ├── test_traps_ecosystem.py            6 tests (E1..E6)
│       ├── test_traps_package.py              6 tests (P1..P6)
│       └── test_deprecated.py                 1 test (S3)
└── tools/
    ├── run_dbt.sh                             dbt deps + seed + build
    ├── run_airflow_tests.sh                   airflow dags parse + pytest airflow/tests/
    ├── wait_for_duckdb.sh                     smoke test del archivo .duckdb
    └── reset_workspace.sh                     rm dev.duckdb dbt_packages target logs
```

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. Linaje via `ref()`/`source()` sin FK en la base (E1)
2. Macros Jinja que generan SQL parametrizado (E2)
3. Ramas `is_incremental()` en modelos incrementales (E3)
4. Materialización por carpeta en `dbt_project.yml` (E4)
5. DAG de Airflow generado desde YAML (E5)
6. XCom explicito entre tareas (E6)

### Paquete (P1‑P6)

1. Macro con concat string `~` (P1, SQLi potencial via `--vars`)
2. `is_incremental()` con `where 1=1` (P2, re-procesa todo)
3. `legacy_helper` macro nunca invocado (P3 adyacente)
4. Materialización incremental con unique_key declarado pero carpeta inconsistente
5. DAG `legacy_purge` con `catchup=False` + `start_date=2019` (P5)
6. `transform_xcom_implicit` con `return dict` no serializable (P6)

### Superficiales (S1‑S3)

1. `legacy_helper.sql` declarado pero no invocado (S1)
2. `legacy_purge_dag.py` con `start_date=2019` + `catchup=False` (S2)
3. `test_deprecated.py` con `pytest.skip` (S3)

## Features (sinonimos neutros CC-11)

- **ventas** (ingesta-de-ventas): DAG `etl_dag` extrae CSV, transforma con `dbt run`, carga con `dbt build`.
- **clientes** (modelo-de-clientes): `int_ventas_clientes` joinea ventas con `stg_clientes`.
- **metricas** (métricas-diarias): `metricas_diarias` usa macro `filter_centros_normalizado`.

## Cómo correr

```bash
docker build -f Dockerfile.test -t npr-fx-dbt-airflow .
docker run --rm -v $(pwd)/.duckdb:/fixture/.duckdb npr-fx-dbt-airflow
```

Salida esperada: `dbt seed + build OK` + `airflow dags parse OK` + `pytest airflow/tests/ 8 archivos passed` + `pytest dev/tests/test_fx_dbt_airflow_ground_truth.py 70 tests passed`.