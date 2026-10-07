# Fixture F06s — fx-go-service

Servicio HTTP en **Go 1.22** con **chi v5** como router, **sqlc** para
generar codigo Go desde SQL, **wire** para DI compile-time,
**goroutines + channels + select** para un worker pool de ingesta,
**go:embed** para plantillas y migraciones, y build tags para
implementaciones legacy. Plantada para que la skill tenga que
rastrear las trampas clasicas del ecosistema Go.

## Stack

- **Lenguaje:** Go 1.22.
- **HTTP:** go-chi/chi v5.
- **ORM/SQL:** sqlc con driver `mattn/go-sqlite3`.
- **DI:** google/wire (compile-time).
- **Tests:** testify v1.10 + go test con `-race`.

## Como se ejecutan los tests

```bash
make test           # go test ./... -race -count=1
make build          # go build
make history        # regenera la historia git (8 commits)
```

En contenedor (Go 1.22 + make + gcc + sqlc + wire):

```bash
python dev/tools/run_fixture_tests.py --fixture fx-go-service --container
```

## Estructura

- `cmd/server/main.go`: entry point que abre DB, crea repos,
  servicios, HTTP server (chi) y worker pool.
- `cmd/legacy/main.go`: dead binary legacy (trampa S02).
- `internal/domain/`: entidades `Event`, `Aggregate` + interfaces
  `EventRepository`, `Exporter` (trampa E01: implementadas
  estructuralmente sin `implements`).
- `internal/repo/sqlite/`: `SQLiteEventRepository` con
  `init()` + `import _ "github.com/mattn/go-sqlite3"` (trampa E02).
- `internal/repo/sqlc/`: codigo generado por `//go:generate sqlc`
  (trampa E03).
- `internal/service/`: `IngestService`, `AggregateService`,
  `ExportService`.
- `internal/http/`: chi handlers + `legacy_export.go` con
  `//go:build legacy` (trampa E05, dead S01).
- `internal/worker/`: pool con goroutines + channels + select
  (trampa E04).
- `internal/config/`: `Config` desde env vars.
- `internal/debug.go`: dead debug helper (trampa S03).
- `templates/export.tmpl`: plantilla embebida via `//go:embed`
  (trampa E06).
- `migrations/001_initial.up.sql`: schema SQLite.
- `sqlc.yaml` + `queries.sql`: codigo generado por sqlc (trampa E03).
- `wire.go`: providers para wire (trampa E03).

## Features

1. **ingesta-de-eventos** (FEAT-001): crear, listar, contar
   eventos por tipo. 7 R-NN.
2. **agregacion** (FEAT-002): computar agregaciones, listar
   resultados, reset. 7 R-NN.
3. **exportacion** (FEAT-003): exportar a JSON/CSV/HTML usando
   templates embebidos. 7 R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06): interfaces implicitas, init() +
  blank imports, codigo generado por go:generate, worker pool
  con goroutines/channels/select, build tags, go:embed.
- 6 del paquete (CC-04): race condition en worker pool,
  goroutine leak, implicit interface mismatch, init side effects
  en tests, channel deadlock, build tag typo.
- 3 superficiales (CC-05): dead legacy_export.go, dead legacy
  binary, dead debug helper.