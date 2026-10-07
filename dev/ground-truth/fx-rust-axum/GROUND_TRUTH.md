# Ground truth de fx-rust-axum (F06t)

Servicio **Rust 1.81** asincrono con **Axum 0.7** como router HTTP,
**tokio 1.40** como runtime async, **sqlx 0.8** para SQLite async,
**serde 1.0** para serializacion, **thiserror 1.0** para errores,
una **proc macro derive custom** que genera `impl` automaticamente
(via `proc-macro2` + `quote` + `syn 2`), una **blanket impl** generica,
**cargo features** con `legacy`, extractors de Axum como argumentos
de los handlers, flujo de errores con `?` y `From` derivations,
y un **build.rs** con un bloque `unsafe` FFI. Plantada para que
la skill tenga que rastrear las trampas clasicas del ecosistema Rust.

## Features

1. **catalogo** (FEAT-001): crear, listar, obtener, actualizar,
   eliminar items. 7 R-NN.
2. **precios** (FEAT-002): crear, listar, obtener, actualizar,
   eliminar precios. 7 R-NN.
3. **sincronizacion** (FEAT-003): crear, listar, obtener, marcar
   como completado jobs de sync. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. `proc_macro_derive`: `#[derive(Entity)]` invoca `entity_derive` que
   genera un `impl` con `ENTITY_NAME` y `entity_name()`.
2. `blanket_impl`: `impl<T: Serialize> Json for T` blanket sobre
   cualquier tipo que implemente Serialize.
3. `cargo_features`: `#[cfg(feature = "legacy")]` en
   `features_legacy.rs` gated por la feature `legacy`.
4. `axum_extractors`: `State<SqlitePool>`, `Json<Req>`, `Path<id>`,
   `Query<T>` en las firmas de los handlers.
5. `error_flow_with_question`: `AppError` con `#[from]` para
   `sqlx::Error` y `anyhow::Error`; el operador `?` en los services.
6. `build_rs_and_unsafe_ffi`: `build.rs` con `cargo:warning`;
   `src/unsafe_ffi.rs` con `extern "C"` + `unsafe { c_legacy_hash }`.

## Decisiones tecnicas (ver DECISIONS.md D-258..D-266)

- D-258: Rust 1.81 + Axum 0.7 + tokio 1.40 + sqlx 0.8 + serde 1.0 +
  thiserror 1.0 + proc-macro2 1 + quote 1 + syn 2.
- D-259: Single-crate con modulos (`src/catalog/`, `src/pricing/`,
  `src/sync/`, `src/infra/`) + crate `fxrust-derive` separado
  para la proc macro.
- D-260: Apps y handlers en ingles (`catalog`, `pricing`, `sync`);
  features en espanol en ground truth.
- D-261: sqlx con query builder programatico (no macro compile-time)
  para evitar chequeo de schema en build.
- D-262: Prefijo `NPRGT-FXRUST-` para 25 unique tokens.
- D-263: `Makefile` envuelve `cargo test --workspace`.
- D-264: Imagen Docker `rust:1.81-bookworm` con `make` + `gcc`
  (cgo de sqlite3).
- D-265: `requires: [linux, macos, windows]`.
- D-266: Deteccion extendida de `axum`, `tokio`, `sqlx` en
  `Cargo.toml` para `fixtures_matrix.py` y `target_matrix.yml`.

## Archivos clave del fixture

- `manifest.yml`, `Makefile`, `Dockerfile.test`, `README.md`,
  `build-history.sh`, `unique_tokens.txt`.
- `Cargo.toml`: workspace con crate `fxrust-axum` y crate
  `fxrust-derive` (proc macro).
- `rust-toolchain.toml`: `channel = "stable"`, `version = "1.81"`.
- `build.rs`: build script con `cargo:warning`.
- `.env.test`: `DATABASE_URL=sqlite::memory:`, `HTTP_PORT=8082`.
- `src/main.rs` + `src/bin/server.rs`: entry points.
- `src/lib.rs`: mod exports.
- `src/catalog/`, `src/pricing/`, `src/sync/`: las 3 features con
  entities, services, handlers (E04).
- `src/infra/`: db, error, config, blanket_impl (E02, E05).
- `src/features_legacy.rs`: codigo gated (E03, S02).
- `src/unsafe_ffi.rs`: bloque unsafe con FFI (E06).
- `src/debug.rs`: dead debug helper (S03).
- `derive-macro/src/lib.rs`: proc macro `Entity` (E01).
- `migrations/001_initial.sql`: schema SQLite.
- `tests/`: catalog, pricing, sync, traps_ecosystem, traps_package,
  traps_superficial (27 tests).