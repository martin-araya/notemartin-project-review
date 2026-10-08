# fx-sql-oracle-plsql

Fixture F06ai. Esquema Oracle Database Free 23c con PL/SQL packages, sinonimos publicos, `EXECUTE IMMEDIATE` con nombres construidos, `PRAGMA AUTONOMOUS_TRANSACTION`, triggers `INSTEAD OF`, jobs de `DBMS_SCHEDULER` y DB links a base remota. Migraciones via Liquibase 4.x. Tests via utPLSQL 3.x.

## Stack

- Oracle Database Free 23c (imagen `gvenzl/oracle-free:23.5-alpine-slim`)
- Liquibase 4.27 (descargado en Dockerfile.test)
- PL/SQL packages con spec + body
- utPLSQL 3.x via `sqlcl`
- JDK 21 para Liquibase

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. Spec frente a body: procedimientos privados solo en body (E1)
2. Sinonimos publicos que redirigen objetos (E2)
3. `EXECUTE IMMEDIATE` con nombres construidos (E3)
4. `PRAGMA AUTONOMOUS_TRANSACTION` (E4)
5. Triggers `INSTEAD OF` sobre vistas (E5)
6. `DBMS_SCHEDULER.CREATE_JOB` + DB links a base remota (E6)

### Paquete (P1‑P6)

1. `PRAGMA AUTONOMOUS_TRANSACTION` que inserta en audit sin manejo de excepcion (P1)
2. Sinonimo publico apuntando a tabla inexistente (P2)
3. `EXECUTE IMMEDIATE` con tabla parametrizada sin whitelist (P3 SQLi)
5. Trigger sin `WHEN OTHERS` (P4)
6. `INSTEAD OF UPDATE` que omite columna critica (P5)
8. `DBMS_SCHEDULER.CREATE_JOB` sin `enabled => TRUE` (P6)

### Superficiales (S1‑S3)

1. `pkg_legacy_spec.sql` declarado pero no usado (S1)
2. `legacy_synonym.sql` apuntando a tabla inexistente (S2)
3. `07-deprecated-test.sql` con `ut.expect(true).to_be_true` trivial (S3)

## Features y R-NN

| Feature | R-NN | Cubre trampas |
|---|---|---|
| `apertura-de-cuenta` | 7 (R-01..R-07) | E1, E3, P1, P2 |
| `cálculo-de-intereses` | 7 (R-01..R-07) | E3, P3, P5 |
| `cierre-de-mes` | 7 (R-01..R-07) | E5, E6, P5, P6 |

## Cómo correr

### En contenedor

```bash
docker build -f dev/fixtures/fx-sql-oracle-plsql/Dockerfile.test -t npr-fx-sql-oracle-plsql dev/fixtures/fx-sql-oracle-plsql/
docker run --rm -v $(pwd)/dev/fixtures/fx-sql-oracle-plsql/.oracle-data:/opt/oracle/oradata npr-fx-sql-oracle-plsql
```

### Vía runner

```bash
python dev/tools/run_fixture_tests.py --fixture fx-sql-oracle-plsql --container
```

## Limitación documentada

Oracle Database Free 23c pesa ~1.5 GB; la primera vez tarda ~3-5 min en arrancar y aplicar migrations. Los tests utPLSQL corren contra una DB efímera (auto-start del contenedor). El archivo `pkg_legacy_spec.sql` está en `db/packages/` como evidencia textual de trampa S1.