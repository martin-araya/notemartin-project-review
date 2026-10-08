# Ground truth — fx-sql-oracle-plsql (F06ai)

Fixture Oracle Database Free 23c con PL/SQL packages (spec + body), sinonimos publicos, `EXECUTE IMMEDIATE` con nombres construidos, `PRAGMA AUTONOMOUS_TRANSACTION`, triggers `INSTEAD OF` sobre vistas, jobs de `DBMS_SCHEDULER` y DB links a base remota. Migraciones via Liquibase 4.x. Tests utPLSQL via `sqlcl`. Ver `ground_truth.json` para la maquina y este documento para la explicacion humana.

## Resumen

| Item | Valor |
|---|---|
| Stack | Oracle 23c + Liquibase 4.27 + PL/SQL + utPLSQL + SQLcl |
| Plataforma | Linux (CI), macOS (dev), contenedor `gvenzl/oracle-free:23.5-alpine-slim` |
| Features | 3: apertura-de-cuenta, cálculo-de-intereses, cierre-de-mes |
| R-NN totales | 21 (7 por feature) |
| Trampas ecosistema | 6 (E1..E6) |
| Trampas paquete | 6 (P1..P6) |
| Trampas superficiales | 3 (S1..S3) |
| Surfaces | 18 (5 tablas + 4 packages + 2 triggers + 1 vista + 3 sinonimos + 2 scheduler-jobs + 1 db-link) |
| Unique tokens | 33 con prefijo `NPRGT-FXORAPL-` |

## Trampas del ecosistema

1. **TRAP-E1 — spec_vs_body_private_proc** (`pkg_accounts_body.sql:8`): `p_internal_validate` solo en body.
2. **TRAP-E2 — public_synonyms** (`synonyms.sql:1`): 5 sinonimos publicos + 1 trampa P2.
3. **TRAP-E3 — execute_immediate_dynamic** (`pkg_interest_body.sql:23`): `EXECUTE IMMEDIATE` con tabla.
4. **TRAP-E4 — autonomous_transaction_trigger** (`004-autonomous-trigger.sql:8`): `PRAGMA AUTONOMOUS_TRANSACTION`.
5. **TRAP-E5 — instead_of_trigger** (`005-instead-of-trigger.sql:8`): trigger `INSTEAD OF UPDATE` sobre vista.
6. **TRAP-E6 — scheduler_and_db_links** (`006-scheduler-jobs.sql:1` + `007-db-link.sql:1`): `DBMS_SCHEDULER` + `DATABASE LINK`.

## Trampas del paquete

1. **TRAP-P1 — autonomous_tx_no_others** (`pkg_accounts_body.sql:18`): sin `EXCEPTION WHEN OTHERS`.
2. **TRAP-P2 — synonym_invalid_table** (`synonyms.sql:21`): sinonimo a tabla inexistente.
3. **TRAP-P3 — dynamic_sql_unsafe** (`pkg_interest_body.sql:27`): SQLi con `EXECUTE IMMEDIATE`.
4. **TRAP-P4 — trigger_no_others_handler** (`004-autonomous-trigger.sql:14`): sin handler.
5. **TRAP-P5 — instead_of_missing_column** (`005-instead-of-trigger.sql:12`): omite `opened_at`.
6. **TRAP-P6 — scheduler_job_disabled** (`006-scheduler-jobs.sql:6`): `enabled => FALSE`.

## Trampas superficiales

1. **TRAP-S1 — legacy_package_unused** (`pkg_legacy_spec.sql:1`).
2. **TRAP-S2 — legacy_synonym_unused** (`legacy_synonym.sql:1`).
3. **TRAP-S3 — deprecated_test_placeholder** (`07-deprecated-test.sql:1`).

## Features

Ver `ground_truth.json` para el detalle de trazas, decision_points, outcomes y config.

## Limitación operativa

Oracle Database Free 23c pesa ~1.5 GB; la primera ejecucion tarda ~3-5 min en arrancar y aplicar migrations. Los tests utPLSQL corren contra una DB efímera (auto-start del contenedor) que se reinicia en cada `docker run`. El archivo `pkg_legacy_spec.sql` está en `db/packages/` como evidencia textual de trampa S1.