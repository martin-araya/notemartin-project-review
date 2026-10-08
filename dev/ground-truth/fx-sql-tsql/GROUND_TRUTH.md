# Ground Truth: fx-sql-tsql

Tabla maestra de referencia cruzada para F06aj. Cada elemento tiene su id, archivo:línea y descripción.

## Entry points

| id | artifact | file:line |
|---|---|---|
| EP-migration-V001 | V001__init_schema.sql (5 tablas base) | db/migration/V001__init_schema.sql:1 |
| EP-migration-V002 | V002__init_triggers.sql (AFTER + INSTEAD OF) | db/migration/V002__init_triggers.sql:1 |
| EP-migration-V003 | V003__recursive_cte_bom.sql (usp_explode_bom) | db/migration/V003__recursive_cte_bom.sql:1 |
| EP-migration-V004 | V004__dynamic_sql_search.sql | db/migration/V004__dynamic_sql_search.sql:1 |
| EP-migration-V005 | V005__merge_conciliacion.sql (MERGE OUTPUT) | db/migration/V005__merge_conciliacion.sql:1 |
| EP-migration-V006 | V006__global_temp_inventory.sql | db/migration/V006__global_temp_inventory.sql:1 |
| EP-migration-V007 | V007__sql_agent_jobs.sql (3 jobs) | db/migration/V007__sql_agent_jobs.sql:1 |
| EP-migration-V008 | V008__legacy_sprocs.sql | db/migration/V008__legacy_sprocs.sql:1 |
| EP-migration-R-totals | R__recalc_stock_totals.sql (P4) | db/migration/R__recalc_stock_totals.sql:1 |
| EP-migration-R-cache | R__rebuild_report_cache.sql (P5) | db/migration/R__rebuild_report_cache.sql:1 |
| EP-view-stock | dbo.vw_stock_current | db/sql/views.sql:5 |
| EP-view-reconcile-dashboard | dbo.vw_reconcile_dashboard | db/sql/views.sql:14 |
| EP-view-report-top | dbo.vw_report_top_items | db/sql/views.sql:25 |
| EP-synonyms | 5 sinonimos CREATE SYNONYM | db/sql/synonyms.sql:5 |
| EP-functions | fn_stock_available + fn_reconcile_status + fn_report_total_sales | db/sql/functions.sql:1 |
| EP-trigger-after-insert | trg_stock_movements_after_insert | db/migration/V002__init_triggers.sql:5 |
| EP-trigger-instead-of | trg_stock_instead_of_update | db/migration/V002__init_triggers.sql:20 |
| EP-stored-proc-explode-bom | usp_explode_bom | db/migration/V003__recursive_cte_bom.sql:4 |
| EP-stored-proc-search-dynamic | usp_stock_search_dynamic | db/migration/V004__dynamic_sql_search.sql:4 |
| EP-stored-proc-search-raw | usp_stock_search_raw (P1) | db/migration/V004__dynamic_sql_search.sql:18 |
| EP-stored-proc-reconcile-run | usp_reconcile_run | db/migration/V005__merge_conciliacion.sql:4 |
| EP-stored-proc-reconcile-partial | usp_reconcile_partial (P2) | db/migration/V005__merge_conciliacion.sql:30 |
| EP-stored-proc-temp-load | usp_temp_load | db/migration/V006__global_temp_inventory.sql:4 |
| EP-stored-proc-temp-consume | usp_temp_consume (P5) | db/migration/V006__global_temp_inventory.sql:20 |
| EP-stored-proc-legacy-export | usp_legacy_export (S1 dead) | db/migration/V008__legacy_sprocs.sql:4 |
| EP-stored-proc-legacy-purge | usp_legacy_purge (S2) | db/migration/V008__legacy_sprocs.sql:14 |
| EP-stored-proc-recalc-totals | usp_recalc_totals | db/migration/V008__legacy_sprocs.sql:26 |
| EP-stored-proc-rebuild-cache | usp_rebuild_cache | db/migration/V008__legacy_sprocs.sql:36 |
| EP-job-hourly | JOB_HOURLY_RECALC_TOTALS | db/migration/V007__sql_agent_jobs.sql:13 |
| EP-job-daily | JOB_DAILY_REBUILD_REPORT_CACHE | db/migration/V007__sql_agent_jobs.sql:36 |
| EP-job-legacy-purge | JOB_LEGACY_PURGE (P6) | db/migration/V007__sql_agent_jobs.sql:59 |
| EP-test-runner | fx_assert_equal + fx_test_begin/end | db/test/test_runner.sql:1 |
| EP-test-stock | 01_stock_test.sql | db/test/01_stock_test.sql:1 |
| EP-test-reconcile | 02_reconcile_test.sql | db/test/02_reconcile_test.sql:1 |
| EP-test-reports | 03_reports_test.sql | db/test/03_reports_test.sql:1 |
| EP-test-triggers | 04_triggers_test.sql | db/test/04_triggers_test.sql:1 |
| EP-test-sql-agent | 05_sql_agent_test.sql | db/test/05_sql_agent_test.sql:1 |
| EP-test-trap-ecosystem | 06_trap_ecosystem_test.sql | db/test/06_trap_ecosystem_test.sql:1 |
| EP-test-trap-package | 07_trap_package_test.sql | db/test/07_trap_package_test.sql:1 |
| EP-test-deprecated | 08_deprecated_test.sql | db/test/08_deprecated_test.sql:1 |
| EP-legacy-artifact | legacy_artifact.sql (S2) | db/sql/legacy_artifact.sql:1 |
| EP-seed-stock | seed_stock.sql | db/seed/seed_stock.sql:1 |
| EP-seed-movements | seed_movements.sql | db/seed/seed_movements.sql:1 |
| EP-seed-bom | seed_bom.sql (P4 cycle) | db/seed/seed_bom.sql:1 |
| EP-install | db/install.sql (orquestador) | db/install.sql:1 |
| EP-entrypoint | entrypoint.sh | entrypoint.sh:1 |

## Features

- **FEAT-001 stock**: 7 R-NN, 2 decision_points, 7 traces
- **FEAT-002 reconcile**: 7 R-NN, 2 decision_points, 7 traces
- **FEAT-003 dashboard**: 7 R-NN, 2 decision_points, 7 traces

## Trampas ejercitadas

### Ecosistema (E1‑E6)

| id | where | descripcion |
|---|---|---|
| TRAP-E01 | db/migration/V004__dynamic_sql_search.sql:21 | sp_executesql parametrizado vs string-concatenado |
| TRAP-E02 | db/migration/V005__merge_conciliacion.sql:21 | MERGE ... OUTPUT $action INTO reconcile_audit |
| TRAP-E03 | db/migration/V002__init_triggers.sql:5 | AFTER + INSTEAD OF triggers |
| TRAP-E04 | db/migration/V003__recursive_cte_bom.sql:9 | CTE recursiva con UNION ALL |
| TRAP-E05 | db/migration/V006__global_temp_inventory.sql:5 | ##global_stock_temp |
| TRAP-E06 | db/migration/V007__sql_agent_jobs.sql:13 | 3 jobs SQL Agent |

### Paquete (P1‑P6)

| id | where | descripcion |
|---|---|---|
| TRAP-P01 | db/migration/V004__dynamic_sql_search.sql:21 | usp_stock_search_raw concat string |
| TRAP-P02 | db/migration/V005__merge_conciliacion.sql:32 | MERGE sin NOT MATCHED BY SOURCE |
| TRAP-P03 | db/migration/V002__init_triggers.sql:25 | INSTEAD OF omite quantity_on_hand |
| TRAP-P04 | db/seed/seed_bom.sql:5 | CTE recursiva + ciclo A->B->C->A |
| TRAP-P05 | db/migration/V006__global_temp_inventory.sql:20 | temp_consume no limpia ##global |
| TRAP-P06 | db/migration/V007__sql_agent_jobs.sql:59 | JOB_LEGACY_PURGE enabled=0 |

### Superficiales (S1‑S3)

| id | where | descripcion |
|---|---|---|
| TRAP-S01 | db/migration/V008__legacy_sprocs.sql:4 | usp_legacy_export dead |
| TRAP-S02 | db/migration/V008__legacy_sprocs.sql:14 + db/sql/legacy_artifact.sql:1 | usp_legacy_purge + trg_old_audit referencias tablas inexistentes |
| TRAP-S03 | db/test/08_deprecated_test.sql:7 | test trivial con IF 1=0 |

## Call graph

| from | to | kind |
|---|---|---|
| EP-stored-proc-reconcile-run | MOD-schema-reconcile-lines | MERGE |
| EP-stored-proc-reconcile-run | EP-reconcile-audit | OUTPUT_INTO |
| EP-stored-proc-temp-load | EP-stored-proc-temp-consume | shared_resource |
| EP-job-hourly | EP-stored-proc-recalc-totals | TSQL_STEP |
| EP-job-daily | EP-stored-proc-rebuild-cache | TSQL_STEP |
| EP-job-legacy-purge | EP-stored-proc-legacy-purge | TSQL_STEP_DISABLED |
| EP-trigger-after-insert | MOD-stock-audit | INSERT_TRIGGER |
| EP-trigger-instead-of | MOD-schema-stock-items | INSTEAD_OF_TRIGGER |
| EP-stored-proc-explode-bom | MOD-schema-bom-links | RECURSIVE_CTE |
| EP-stored-proc-rebuild-cache | MOD-schema-report-cache | DELETE_INSERT |

## Tests

| file | feature | tests |
|---|---|---|
| db/test/01_stock_test.sql | FEAT-001 stock | 7 |
| db/test/02_reconcile_test.sql | FEAT-002 reconcile | 7 |
| db/test/03_reports_test.sql | FEAT-003 dashboard | 7 |
| db/test/04_triggers_test.sql | FEAT-001 stock (triggers) | 7 |
| db/test/05_sql_agent_test.sql | FEAT-001 stock (sql agent) | 7 |
| db/test/06_trap_ecosystem_test.sql | all (ecosystem) | 6 |
| db/test/07_trap_package_test.sql | all (package) | 6 |
| db/test/08_deprecated_test.sql | all (deprecated) | 1 |

Total: **48 tests T-SQL** + **6 unit tests de la fx_assert_equal runner**.