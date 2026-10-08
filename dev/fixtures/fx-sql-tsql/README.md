# fx-sql-tsql

Fixture F06aj. Base de datos SQL Server 2022 con T-SQL: stored procedures con `sp_executesql`, `MERGE` con `OUTPUT $action`, triggers `AFTER` e `INSTEAD OF`, CTE recursivas, tablas temporales globales (`##global`) y scripts de SQL Agent (3 jobs). Migraciones con un orquestador `db/install.sql` + `sqlcmd`. Tests en T-SQL puro ejecutados por `tools/run_tests.sh` (sin tSQLt).

## Stack

- SQL Server 2022 (imagen oficial `mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04`)
- T-SQL (DDL + DML + stored procedures + triggers + functions + views)
- `mssql-tools18` (`sqlcmd` con `-C TrustServerCertificate`)
- Contenedor Docker con `entrypoint.sh` que arranca `sqlservr`, espera, aplica migraciones y corre tests

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. `sp_executesql` parametrizado vs string-concatenado (E1)
2. `MERGE ... OUTPUT $action` + `INTO` (E2)
3. Triggers `AFTER` + `INSTEAD OF` (E3)
4. CTE recursiva con `UNION ALL` y `OPTION (MAXRECURSION)` (E4)
5. Tablas temporales globales `##global` compartidas (E5)
6. SQL Agent jobs (`sp_add_job` + `sp_add_schedule` + `sp_attach_schedule`) (E6)

### Paquete (P1‑P6)

1. `usp_stock_search_raw` con `EXEC` de string concatenado (P1, SQLi potencial)
2. `usp_reconcile_partial` sin `WHEN NOT MATCHED BY SOURCE` (P2, huerfanos)
3. Trigger `INSTEAD OF UPDATE` que omite columna `quantity_on_hand` (P3)
4. CTE recursiva con ciclo en `bom_links` sin `MAXRECURSION` (P4)
5. `usp_temp_consume` no limpia `##global_stock_temp` (P5, leak)
6. `JOB_LEGACY_PURGE` con `enabled = 0` (P6, nunca corre)

### Superficiales (S1‑S3)

1. `usp_legacy_export` declarado pero no invocado (S1)
2. `usp_legacy_purge` referencia `dbo.legacy_archive` que no existe; trigger `trg_old_audit` sobre tabla inexistente (S2, instalación silenciosamente falla)
3. `08_deprecated_test.sql` con `IF 1=0 SELECT 'noop'` (S3)

## Features y R-NN

3 features × ≥ 7 R-NN cada una (21 R-NN total):

- **stock (inventario)**: CRUD sobre `stock_items` + `stock_movements`, triggers `AFTER`/`INSTEAD OF`, búsqueda dinámica.
- **reconcile (conciliación)**: `MERGE` con `OUTPUT $action` en `reconcile_lines` + `reconcile_audit`.
- **dashboard (reportes)**: vistas materializadas + cache en `report_cache` + JSON serializado.

## Cómo correr

```bash
docker build -f Dockerfile.test -t npr-fx-sql-tsql .
docker run --rm -v $(pwd)/.sqlserver_data:/var/opt/mssql/data npr-fx-sql-tsql
```

Salida esperada: `[SUITE_PASS]` x8 (stock, reconcile, dashboard, triggers, sql_agent, trap_ecosystem, trap_package, deprecated).

## Estructura

```
fx-sql-tsql/
├── Dockerfile.test             FROM mcr.microsoft.com/mssql/server:2022-CU14-ubuntu-22.04
├── entrypoint.sh               sqlservr + wait + install + tests
├── Makefile                    TEST_CMD, IMAGE_TAG, targets
├── manifest.yml                requiere linux/macos, container enabled
├── build-history.sh            8 commits reproducibles
├── unique_tokens.txt           33 tokens prefijo NPRGT-FXSQLTS-
├── config/msodbcsql.ini        ODBC con TrustServerCertificate=yes
├── db/
│   ├── install.sql             maestro: tablas aux + V00X + R__ + sql + seed
│   ├── uninstall.sql           DROP sin preparar
│   ├── migration/
│   │   ├── V001__init_schema.sql              5 tablas + 2 indices
│   │   ├── V002__init_triggers.sql           trg_stock_movements_after_insert + trg_stock_instead_of_update
│   │   ├── V003__recursive_cte_bom.sql       usp_explode_bom con UNION ALL
│   │   ├── V004__dynamic_sql_search.sql      usp_stock_search_dynamic + usp_stock_search_raw
│   │   ├── V005__merge_conciliacion.sql      usp_reconcile_run + usp_reconcile_partial
│   │   ├── V006__global_temp_inventory.sql   usp_temp_load + usp_temp_consume
│   │   ├── V007__sql_agent_jobs.sql          3 jobs SQL Agent
│   │   ├── V008__legacy_sprocs.sql           usp_legacy_export + usp_legacy_purge
│   │   ├── R__recalc_stock_totals.sql        (P4 trap)
│   │   └── R__rebuild_report_cache.sql       (P5 trap)
│   ├── sql/
│   │   ├── views.sql                         vw_stock_current + vw_reconcile_dashboard + vw_report_top_items
│   │   ├── synonyms.sql                      5 sinonimos (E2 + P2 trap)
│   │   ├── functions.sql                     fn_stock_available + fn_reconcile_status + fn_report_total_sales
│   │   └── legacy_artifact.sql               trg_old_audit sobre tabla inexistente (S2)
│   ├── seed/
│   │   ├── seed_stock.sql                    5 items stock
│   │   ├── seed_movements.sql                12 movimientos (1 soft-deleted)
│   │   └── seed_bom.sql                      jerarquia con ciclo A->B->C->A (P4 trap)
│   └── test/
│       ├── test_runner.sql                   fx_assert_equal + fx_test_begin/end + fx_test_results
│       ├── 01_stock_test.sql                 7 tests
│       ├── 02_reconcile_test.sql             7 tests
│       ├── 03_reports_test.sql               7 tests
│       ├── 04_triggers_test.sql              7 tests
│       ├── 05_sql_agent_test.sql             7 tests
│       ├── 06_trap_ecosystem_test.sql        6 tests (E1..E6)
│       ├── 07_trap_package_test.sql          6 tests (P1..P6)
│       └── 08_deprecated_test.sql            1 test (S3)
└── tools/
    ├── wait_for_sql.sh                       poll hasta que sqlcmd acepte conexiones
    ├── apply_migrations.sh                   CREATE DATABASE + db/install.sql
    ├── run_tests.sh                          itera 8 archivos de test con sqlcmd
    └── reset_db.sh                           DROP DATABASE fxsqlts
```