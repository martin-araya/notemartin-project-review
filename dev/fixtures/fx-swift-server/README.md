# fx-swift-server

Fixture F06ab. Paquete Swift multiplataforma (Vapor + Fluent + macros + build tool plugin + CLI) que ejercita las trampas del ecosistema **Swift server-side** y del paquete por feature para validar `notemartin-project-review`.

## Stack

- Swift 6.0+
- Vapor 4.x + FluentSQLiteDriver
- swift-argument-parser 1.3+
- swift-syntax 510 (para macros)
- SPM plugin build-tool
- XCTest + Swift Testing (macOS 13+)
- SQLite en `:memory:` para tests

## Trampas ejercitadas

### Ecosistema (E1‑E6)

1. **Macros `@attached(member)`** que producen `registerRoute(...)` sin estar en el código fuente
2. **Build tool plugin** que genera `Generated/AuditCodes.generated.swift`
3. **`RouteCollection.boot(routes:)`** como punto de wiring de rutas Vapor
4. **Modelos Fluent** con `@Field`/`@Parent` y migraciones declarativas
5. **`actor`** con `Sendable` DTOs como modelo de concurrencia
6. **`#if canImport(FoundationNetworking)`** que cambia el comportamiento entre Linux y macOS

### Paquete (P1‑P6)

1. `@freestanding(declaration)` macro que inyecta `import` que no aparece en el AST literal
2. `@unchecked Sendable class` con `var` mutable (anti‑patrón de concurrencia)
3. `actor` con `try?` silencioso que oculta errores de DB
4. Build tool plugin que **no falla** cuando una dependencia falta (genera archivo vacío)
5. Migración Fluent con índice UNIQUE no idempotente
6. `RouteCollection.boot` que registra catch‑all `*` antes de rutas específicas

### Superficiales (S1‑S3)

1. `LegacyHelper` con funciones sin consumidores
2. `import` no usado en una rama `#else`
3. Variable de entorno `LEGACY_MODE` declarada pero nunca leída

## Features y R-NN

| Feature | R-NN | Cubre trampas |
|---|---|---|
| `api-de-notas` | 7 (R-01..R-07) | E1, E3, E4, P5, P6, R-07 (timeout) |
| `cli-de-importación` | 7 (R-01..R-07) | exit codes, async command, macro inválida |
| `auditoría` | 7 (R-01..R-07) | E2, E5, E6, P1, P2, P3, P4 |

## Cómo correr

### En Linux (contenedor)

```bash
docker build -f dev/fixtures/fx-swift-server/Dockerfile.test -t npr-fx-swift-server dev/fixtures/fx-swift-server/
docker run --rm -v $(pwd)/dev/fixtures/fx-swift-server/.build-cache:/app/.build npr-fx-swift-server swift test --parallel
```

### En macOS (con Swift 6.0+)

```bash
cd dev/fixtures/fx-swift-server
swift test --parallel
```

### Vía runner

```bash
python dev/tools/run_fixture_tests.py --fixture fx-swift-server --container
```