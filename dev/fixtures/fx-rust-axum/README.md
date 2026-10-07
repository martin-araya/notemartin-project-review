# Fixture F06t — fx-rust-axum

Servicio **Rust 1.81** asincrono con **Axum 0.7** como router HTTP,
**tokio 1.40** como runtime async, **sqlx 0.8** para SQLite async,
**serde 1.0** para serializacion, **thiserror 1.0** para errores,
una **proc macro derive custom** que genera `impl` automaticamente
(via `proc-macro2` + `quote` + `syn`), una **blanket impl** generica,
**cargo features** con `legacy`, extractors de Axum como argumentos
de los handlers, flujo de errores con `?` y `From` derivations,
y un **build.rs** con un bloque `unsafe` FFI. Plantada para que la
skill tenga que rastrear las trampas clasicas del ecosistema Rust.

## Stack

- **Lenguaje:** Rust 1.81 (stable).
- **HTTP:** Axum 0.7.
- **Async:** tokio 1.40.
- **DB:** sqlx 0.8 con `sqlite` (in-memory para tests).
- **Serializacion:** serde 1.0.
- **Errores:** thiserror 1.0.
- **Proc macro:** `proc-macro2` + `quote` + `syn 2`.
- **Tests:** `cargo test --workspace` (sin framework externo, stdlib).

## Como se ejecutan los tests

```bash
make test           # cargo test --workspace
make build          # cargo build --workspace
make history        # regenera la historia git (8 commits)
```

En contenedor (Rust 1.81 + make + gcc + cgo):

```bash
python dev/tools/run_fixture_tests.py --fixture fx-rust-axum --container
```

## Estructura

- `Cargo.toml`: workspace con crates `fxrust-axum` (main) y
  `fxrust-derive` (proc macro).
- `rust-toolchain.toml`: `channel = "stable"`, `version = "1.81"`.
- `build.rs`: build script con `cargo:warning=...` (E06).
- `src/main.rs` + `src/bin/server.rs`: entry points.
- `src/infra/`: db pool, error con `From`, config, blanket impl.
- `src/catalog/`, `src/pricing/`, `src/sync/`: las 3 features con
  entities, services, handlers (E04).
- `src/features_legacy.rs`: codigo gated por `#[cfg(feature = "legacy")]`
  (E03, S02).
- `src/unsafe_ffi.rs`: bloque `unsafe` con FFI (E06).
- `src/debug.rs`: helper dead (S03).
- `derive-macro/src/lib.rs`: proc macro `Entity` (E01).
- `migrations/`: SQL de sqlx.

## Features

1. **catalogo** (FEAT-001): crear, listar, obtener, actualizar,
   eliminar items. 7 R-NN.
2. **precios** (FEAT-002): crear, listar, obtener, actualizar,
   eliminar precios. 7 R-NN.
3. **sincronizacion** (FEAT-003): crear, listar, obtener, marcar
   como completado jobs de sync. 7 R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06): proc macro derive, blanket impl,
  cargo features, axum extractors, error flow con `?`, build.rs +
  unsafe FFI.
- 6 del paquete (CC-04): proc macro genera codigo incorrecto,
  blanket impl conflict, cargo feature typo, axum extractor order,
  from impl cycles, build.rs fails.
- 3 superficiales (CC-05): dead debug helper, dead legacy feature,
  dead unused function.