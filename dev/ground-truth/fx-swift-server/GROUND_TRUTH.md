# Ground truth — fx-swift-server (F06ab)

Fixture Swift 6 server-side con Vapor + Fluent + macros + build tool plugin + swift-argument-parser CLI. Ver `ground_truth.json` para la maquina y este documento para la explicacion humana.

## Resumen

| Item | Valor |
|---|---|
| Stack | Swift 6.0.3, Vapor 4.92+, FluentSQLiteDriver, swift-argument-parser 1.3+, swift-syntax 510+ |
| Plataforma | Linux (contenedor swift:6.0.3-jammy) + macOS |
| Productos SPM | FxSwiftServer (lib + ejecutable), FxSwiftMacros (lib), fxsimport (CLI), AuditCodesPlugin (plugin) |
| Features | 3: api-de-notas, cli-de-importacion, auditoria |
| R-NN totales | 21 (7 por feature) |
| Trampas ecosistema | 6 (E1..E6) |
| Trampas paquete | 6 (P1..P6) |
| Trampas superficiales | 3 (S1..S3) |
| Superficies | 10 (8 HTTP + 2 CLI) |
| Unique tokens | 38 con prefijo `NPRGT-FXSWIFTSRV-` |

## Trampas del ecosistema

1. **TRAP-E1 — macros_attached_member** (`Sources/FxSwiftMacros/RouteMacro.swift:8`): `@attached(peer, names:)` genera `registerRoute` en `.build/`.
2. **TRAP-E2 — build_tool_plugin** (`Plugins/AuditCodesPlugin/Plugins/AuditCodesPlugin.swift:9`): SPM `BuildToolPlugin` que produce `Generated/AuditCodes.generated.swift`.
3. **TRAP-E3 — route_collection_boot** (`Sources/FxSwiftServer/Routes/NotesRoutes.swift:11`): wiring de rutas en `RouteCollection.boot(routes:)`.
4. **TRAP-E4 — fluent_models_field_parent_timestamp** (`Sources/FxSwiftServer/Models/Note.swift:10`): `@Field`/`@Parent`/`@Timestamp` con migracion separada.
5. **TRAP-E5 — actor_sendable_concurrency** (`Sources/FxSwiftServer/Services/AuditRecorder.swift:11`): `actor` + DTOs `Sendable struct`.
6. **TRAP-E6 — canImport_foundation_networking** (`Sources/FxSwiftServer/Services/UrlSessionProvider.swift:14`): `#if canImport(FoundationNetworking)` cambia el comportamiento entre plataformas.

## Trampas del paquete

1. **TRAP-P1 — import_macro_freestanding** (`Sources/FxSwiftServer/App.swift:14`): `@ImportModuleDecl` expande a `import` que no esta en el AST literal.
2. **TRAP-P2 — unchecked_sendable_class** (`Sources/FxSwiftServer/DTOs/LegacyNoteDTO.swift:7`): `class @unchecked Sendable` con `var`.
3. **TRAP-P3 — silent_try_audit** (`Sources/FxSwiftServer/Services/AuditRecorder.swift:18`): `try?` o `return false` que oculta errores.
4. **TRAP-P4 — build_plugin_noop_fallback** (`Plugins/AuditCodesPlugin/Plugins/AuditCodesPlugin.swift:30`): el plugin genera archivo vacio cuando una dep falta.
5. **TRAP-P5 — unique_index_non_idempotent** (`Sources/FxSwiftServer/Migrations/CreateNote.swift:17`): UNIQUE index no idempotente.
6. **TRAP-P6 — catch_all_before_specific** (`Sources/FxSwiftServer/Routes/AuditRoutes.swift:14`): wildcard `*` registrado antes que las rutas.

## Trampas superficiales

1. **TRAP-S1 — legacy_helper_unused** (`Sources/FxSwiftServer/Services/LegacyHelper.swift:5`): helper sin consumidores.
2. **TRAP-S2 — unused_import_in_else_branch** (`Sources/FxSwiftServer/Services/UrlSessionProvider.swift:21`): `_ = URLSession.self` en `#else`.
3. **TRAP-S3 — env_var_unused** (`Sources/FxSwiftServer/Configure.swift:24`): `LEGACY_MODE` leido pero nunca usado.

## Features

Ver `ground_truth.json` para el detalle de trazas, decision_points, outcomes y config.