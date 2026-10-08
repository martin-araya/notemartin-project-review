# fx-sql-postgres

Fixture F06ah. Repositorio PostgreSQL con Flyway como herramienta de migraciones, PL/pgSQL para funciones y triggers, pg_cron para programar jobs, Row-Level Security (RLS) para multi-tenant, vistas materializadas refrescadas automáticamente, `ON DELETE CASCADE` y SQL dinámico con `EXECUTE format(...)`. Tests pgTAP via `pg_prove`.

## Stack

- PostgreSQL 16 con `pg_cron` 1.6 (instalado desde git)
- Flyway 10 con archivos `V<NUM>__<mv>.sql` y `R__<mv>.sql`
- PL/pgSQL para funciones y triggers
- pgTAP via `pg_prove` para tests
- Imagen Docker basada en `postgres:16-alpine` + JDK 21

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. **Triggers con efectos secundarios** (E1): INSERT/UPDATE/DELETE en `facturas` crean rows en `auditoria`
2. **Row-Level Security** (E2): policies por `tenant_id` + `FORCE ROW LEVEL SECURITY`
3. **SQL dinámico** (E3): `EXECUTE format(...)` con tabla parametrizada
4. **Migraciones versionadas + repetibles** (E4): V1..V7 + R__ con id tracking
5. **`ON DELETE CASCADE`** (E5): foreign keys CASCADE + DEFERRABLE
6. **Vistas materializadas + pg_cron** (E6): `cron.schedule('refresh-mv', ...)` + vista soft-delete

### Paquete (P1‑P6)

1. Trigger que lee `NEW.campo` en DELETE (no válido) — P1
2. Policy RLS sin `FORCE` para tabla crítica — P2
3. Función SQL dinámico sin whitelist de tablas — P3
4. Migración R__ que borra filas antes de reinsertar (no idempotente) — P4
5. `ON DELETE CASCADE` que borra items sin avisar — P5
6. Vista materializada que NO excluye soft-deleted — P6

### Superficiales (S1‑S3)

1. `db/sql/legacy_export.sql` con COPY no usado — S1
2. `db/schema/007_unused_indexes.sql` con CREATE INDEX no usado — S2
3. `db/test/08_deprecated_test.sql` con test trivial — S3

## Features y R-NN

| Feature | R-NN | Cubre trampas |
|---|---|---|
| `facturación` | 7 (R-01..R-07) | E1, E3, E5, P1, P3, P5 |
| `auditoría` | 7 (R-01..R-07) | E1, E6, P1, P4 |
| `multi-tenant` | 7 (R-01..R-07) | E2, E6, P2, P6 |

## Cómo correr

### En contenedor

```bash
docker build -f dev/fixtures/fx-sql-postgres/Dockerfile.test -t npr-fx-sql-postgres dev/fixtures/fx-sql-postgres/
docker run --rm -v $(pwd)/dev/fixtures/fx-sql-postgres/.pg-data:/var/lib/postgresql/data npr-fx-sql-postgres
```

### Vía runner

```bash
python dev/tools/run_fixture_tests.py --fixture fx-sql-postgres --container
```

## Limitación documentada

Los tests pgTAP corren contra una DB PostgreSQL efímera (`fxpg_test`) que se reinicia en cada `docker run`. Los archivos `.g.dart`/`.freezed.dart` no aplican aquí; los archivos migrados viven en `db/migration/` y se ejecutan por Flyway en orden `V1`, `V2`, ..., `V7`, `R__*`.