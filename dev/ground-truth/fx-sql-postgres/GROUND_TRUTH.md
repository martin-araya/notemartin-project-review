# Ground truth — fx-sql-postgres (F06ah)

Fixture PostgreSQL 16 con Flyway 10 como herramienta de migraciones, PL/pgSQL para funciones y triggers, pg_cron para programar jobs, Row-Level Security (RLS) para multi-tenant, vistas materializadas refrescadas automáticamente, `ON DELETE CASCADE` con `DEFERRABLE` y SQL dinámico con `EXECUTE format(...)`. Tests pgTAP via `pg_prove`.

## Resumen

| Item | Valor |
|---|---|
| Stack | PostgreSQL 16 + Flyway 10 + PL/pgSQL + pg_cron 1.6 + pgTAP 1.x |
| Plataforma | Linux (CI), macOS (dev), container `postgres:16-alpine` |
| Features | 3: facturación, auditoría, multi-tenant |
| R-NN totales | 21 (7 por feature) |
| Trampas ecosistema | 6 (E1..E6) |
| Trampas paquete | 6 (P1..P6) |
| Trampas superficiales | 3 (S1..S3) |
| Surfaces | 19 (4 tablas + 3 triggers + 2 policies + 5 funciones + 2 vistas + 3 cron-jobs + 1 FK constraint) |
| Unique tokens | 32 con prefijo `NPRGT-FXSQLPG-` |

## Trampas del ecosistema

1. **TRAP-E1 — audit_triggers_side_effects** (`V2__add_audit_triggers.sql:1`): 3 triggers con `f_audit_factura()`.
2. **TRAP-E2 — row_level_security** (`V3__add_rls_policies.sql:1`): 13 policies + ENABLE per tabla.
3. **TRAP-E3 — dynamic_sql_execute_format** (`V4__add_dynamic_sql_fn.sql:1`): `EXECUTE format()` con tabla.
4. **TRAP-E4 — repeatable_migrations** (`R__recalc_factura_totals.sql:1`): R__ corre tras V*.
5. **TRAP-E5 — on_delete_cascade** (`V6__add_cascade_constraints.sql:1`): FK CASCADE + DEFERRABLE.
6. **TRAP-E6 — pg_cron_and_materialized_views** (`V7__add_pg_cron_jobs.sql:1`): 3 jobs cron + materialized view.

## Trampas del paquete

1. **TRAP-P1 — trigger_new_in_delete** (`V2__add_audit_triggers.sql:21`): `NEW.id` en DELETE.
2. **TRAP-P2 — rls_no_force_approach** (`V3__add_rls_policies.sql:1`): postgres superuser bypass.
3. **TRAP-P3 — dynamic_sql_no_whitelist** (`V4__add_dynamic_sql_fn.sql:1`): SQLi potencial.
4. **TRAP-P4 — repeatable_non_idempotent** (`R__recalc_factura_totals.sql:1`): TRUNCATE + INSERT.
5. **TRAP-P5 — cascade_silent_delete** (`V6__add_cascade_constraints.sql:6`): CASCADE sin notify.
6. **TRAP-P6 — materialized_view_no_soft_delete_filter** (`V7__add_pg_cron_jobs.sql:15`): sin `WHERE deleted_at IS NULL`.

## Trampas superficiales

1. **TRAP-S1 — legacy_export_unused** (`legacy_export.sql:1`).
2. **TRAP-S2 — unused_indexes** (`007_unused_indexes.sql:1`).
3. **TRAP-S3 — deprecated_test_placeholder** (`08_deprecated_test.sql:1`).

## Features

Ver `ground_truth.json` para el detalle de trazas, decision_points, outcomes y config.

## Limitación operativa

Los tests pgTAP corren contra una DB PostgreSQL efímera (`fxpg_test`) que se reinicia en cada `docker run`. El contenedor pesa ~1.5 GB (postgres + pg_cron 1.6 desde git + pg_prove + JDK 21 + Flyway 10). La primera ejecución tarda ~3-5 min descargando + compilando pg_cron + aceptando licencias.