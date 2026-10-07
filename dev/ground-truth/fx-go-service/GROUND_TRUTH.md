# Ground truth de fx-go-service (F06s)

Servicio HTTP en **Go 1.22** con **chi v5** como router, **sqlc** para
generar codigo Go desde SQL, **wire** para DI compile-time, **goroutines
+ channels + select** para un worker pool de ingesta, **go:embed** para
plantillas y migraciones, y build tags para implementaciones legacy.
Plantada para que la skill tenga que rastrear las trampas clasicas
del ecosistema Go.

## Features

1. **ingesta-de-eventos** (FEAT-001): crear, listar, contar eventos.
   7 R-NN.
2. **agregacion** (FEAT-002): computar agregaciones, listar,
   reset. 7 R-NN.
3. **exportacion** (FEAT-003): exportar a JSON/CSV/HTML usando
   templates embebidos. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. `implicit_interfaces`: las interfaces (EventRepository, Exporter)
   se implementan estructuralmente sin keyword `implements`.
2. `init_function_and_blank_imports`: `func init()` + `_ "github.com/..."`
   blank imports registran el driver.
3. `go_generate_code`: codigo generado por `sqlc` y `wire` via
   `//go:generate`.
4. `worker_pool_goroutines`: `go p.worker()` + `chan int` + `select`
   con `ctx.Done()`.
5. `build_tags`: `//go:build legacy` en `legacy_export.go`.
6. `go_embed`: `//go:embed templates/*.tmpl` + `embed.FS`.

## Decisiones tecnicas (ver DECISIONS.md D-248..D-256)

- D-248: Go 1.22 + chi v5.1 + sqlc v1.27 + wire v0.6 +
  go-sqlite3 v1.14 + testify v1.9.
- D-249: Apps en ingles (`internal/orders/`, `internal/aggregate/`,
  `internal/export/`); features en espanol en ground truth.
- D-250: sqlc genera codigo en `internal/repo/sqlc/` via
  `sqlc generate` durante el build del contenedor (E03).
- D-251: wire genera `wire_gen.go` con `wire gen ./...` (E03).
- D-252: Interfaces implementadas estructuralmente sin
  keyword `implements` (E01).
- D-253: Prefijo `NPRGT-FXGO-` para 26 unique tokens.
- D-254: `Makefile` envuelve `go test ./... -race -count=1`.
- D-255: Imagen Docker `golang:1.22-bookworm` con `make` + `gcc`
  (necesario para cgo de sqlite3).
- D-256: `requires: [linux, macos, windows]`.

## Archivos clave del fixture

- `manifest.yml`, `Makefile`, `Dockerfile.test`, `README.md`,
  `build-history.sh`, `unique_tokens.txt`.
- `go.mod`: module fx-go-service + deps + `replace` para
  davecheney/profile (modulo privado eliminado).
- `sqlc.yaml`: config de sqlc (E03).
- `queries.sql`: queries SQL con anotaciones sqlc.
- `wire.go`: providers de wire con `//go:build wireinject` (E03).
- `pytest.ini`: `asyncio_mode = auto` (no aplica aqui, es Go).
- `.env.test`: `DATABASE_URL=:memory:`, `HTTP_PORT=8081`,
  `WORKER_COUNT=2`.
- `conftest.go`: helpers de test (no usado por go test).
- `cmd/server/main.go`: entry point con graceful shutdown.
- `cmd/legacy/main.go`: dead legacy binary (S02).
- `internal/domain/`: entidades + interfaces (E01).
- `internal/repo/sqlite/`: SQLiteEventRepository + SQLiteExporter
  con implementacion estructural (E01) + init() y blank import (E02).
- `internal/repo/sqlc/db.go`: stub sqlc-generated (E03).
- `internal/service/`: IngestService, AggregateService, ExportService
  con template embebido (E06).
- `internal/http/`: chi handlers + server + legacy (E04, E05, S01).
- `internal/worker/`: pool con goroutines + channels + select (E04).
- `internal/config/config.go`: config desde env vars.
- `internal/debug.go`: dead debug helper (S03).
- `migrations/001_initial.up.sql`: schema SQLite.
- `templates/export.tmpl`: template original (duplicado en
  `internal/service/templates/`).
- `tests/`: ingest_test.go + aggregate_test.go + export_test.go +
  traps_ecosystem_test.go + traps_package_test.go +
  traps_superficial_test.go (24 tests).