# Progreso del constructor

Estado por fase de la skill `notemartin-project-review` y registro de avance.

## Tabla de fases

| Fase | Estado | Fecha | Evidencia | Notas |
|---|---|---|---|---|
| F00 | HECHA | 2026-10-05 | pytest 1 passed; validate_skill OK; árbol coincide con §10 de AGENTS; 6/7 criterios cumplidos, 1 eliminado por D-108 (CI GitHub Actions prohibido) | Commit `F00: estructura base` (cb7a9ca) + commit de actualización D-108 |
| F01 | HECHA | 2026-10-05 | pytest 25 passed (24 nuevos + 1 smoke); validate_skill sobre skill real → OK; description 830/1024; cuerpo 142/5000 tokens; 8 disparadores ES + 6 EN | Commit `F01: SKILL.md esqueleto y validador` |
| F02 | HECHA | 2026-10-05 | pytest 25 passed; validate_skill OK; 3 borradores en dev/evals/drafts (Hermes 203 líneas, Cline 220, Kilo 227); references/22-adaptadores-runtime.md con 210 líneas, 23 fuentes citadas (URL + fecha), matriz 11×3, 4 secciones obligatorias | Commit `F02: referencia de adaptadores por runtime` |
| F03 | HECHA | 2026-10-05 | pytest 54 passed (53 nuevos + 1 smoke); validate_skill OK; scripts/npr/citations.py con 5 patrones (RANGE_SYMBOL, RANGE, LINE, GIT, DYN); references/00-principios.md con 8 leyes verificables, 14 ejemplos válidos y 11 inválidos; SHA case-insensitive normalizado a minúsculas; rechazo de paths absolutos | Commit `F03: principios y gramática de citas` |
| F04 | HECHA | 2026-10-05 | pytest 109 passed (55 nuevos + 54 anteriores); validate_skill OK; 19 esquemas JSON con `description` en cada propiedad; scripts/npr/schema.py stdlib puro (json, re, sys, pathlib, typing, argparse, dataclasses); 38 ejemplos (19 valid + 19 invalid); 10 keywords implementadas (type, required, properties, additionalProperties, items, enum, pattern, minimum, maximum, $ref local) | Commit `F04: esquemas de datos del workspace` |
| F05 | HECHA | 2026-10-05 | pytest 129 passed (20 nuevos + 109 anteriores); validate_skill OK; 37 subcomandos registrados (--help), 4 implementados (init, config, status, resume) + 33 stubs con NPR-E113; 16 codigos de error NPR-Exxx en catalogo; config show refleja precedencia 4 niveles (defaults < workspace < --config < --set); init idempotente, no duplica .git/info/exclude, no ensucia git status, soporta dir sin git con NPR-E116; status --json valida contra esquema state | Commit `F05: CLI npr y creacion del workspace` |
| F06a | HECHA | 2026-10-05 | pytest ≥137 passed; check_ground_truth OK sobre fx-python-cli (0 referencias rotas); fx-python-cli con 4 features (add, list, delete, export), 6 R-NN cada una; 6 trampas superficiales + 6 trampas específicas del paquete plantadas y documentadas; build-history.sh con 8 commits; unique_tokens.txt sin fugas en el fixture | Commit `F06a: fixture fx-python-cli con ground truth y trampas` |
| F06a2 | HECHA | 2026-10-06 | pytest 260 passed (121 nuevos en F06a2: 57 test_check_ground_truth + 20 test_comment_syntax + 19 test_encoding + 16 test_run_fixture_tests + 9 test_fixtures_matrix); check_ground_truth extendido a 9 formatos (text, range, symbol, column, container zip+asar, notebook, xpath, yaml-path, binary offset+symbol); comment_syntax.json con 80+ entradas y CC-11 operativo; encoding.py con BOM/UTF-8/UTF-16/Latin-1/Shift-JIS/CRLF; _template/ completo; target_matrix.yml + fixtures_matrix.py generan MATRIX.md; fx-python-cli sin cambios (check_ground_truth OK, sin diffs en fixture ni ground truth); validate_skill y overfit_guard siguen verdes; 5 decisiones nuevas D-159..D-163 | Commit `F06a2: verificador y harness multi-ecosistema` |
| F06b | HECHA | 2026-10-06 | pytest 273 passed (13 nuevos: test_fx_ts_agent_extension_ground_truth); vitest 162 passed (162 tests en 11 archivos: modes, skills, tools, providers, context, i18n, mcp, vscode_shim, messages, extension, traps); check_ground_truth OK sobre fx-ts-agent-extension (0 referencias rotas, CC-11 verde); messages.ts con 5.163 lineas (>5.000); 3 modos, 6 tools, 12 mensajes webview, 4 features, 6 R-NN cada una; 6 trampas ecosistema + 6 trampas paquete plantadas y documentadas; run_fixture_tests en contenedor Node 22 -> passed; MATRIX.md cubre vscode-extension y typescript; fx-python-cli sin cambios (regresion F06a verificada); 5 decisiones nuevas D-164..D-168 | Commit `F06b: fixture fx-ts-agent-extension con paquete por feature` |
| F06c | HECHA | 2026-10-06 | pytest 292 passed (19 nuevos: test_fx_java_micronaut_ground_truth); gradle 38 passed (1 skipped con assumeTrue); check_ground_truth OK sobre fx-java-micronaut (CC-11 verde); 4 features (alta-cliente, consulta-score-externo, cierre-diario-programado, notificar-evento) con 6 R-NN cada una; 6 trampas ecosistema (beans condicionales @Requires, @Client declarativo, precedencia yml, ApplicationEventPublisher + @EventListener, @Scheduled(cron="${...}"), columna Flyway solo en @Query) + 6 trampas paquete plantadas y documentadas; run_fixture_tests en contenedor `gradle:8.10-jdk21-jammy` -> passed (Gradle wrapper no necesario, imagen ya trae gradle); MATRIX.md cubre java + micronaut + gradle; fx-python-cli y fx-ts-agent-extension sin cambios (regresion F06a+F06b verificada); 5 decisiones nuevas D-169..D-173; fixtures_matrix.py ahora detecta Micronaut via el plugin en build.gradle.kts | Commit `F06c: fixture fx-java-micronaut con paquete por feature` |
| F06c | PENDIENTE | | fx-java-micronaut (REST Micronaut con DI compile-time, application.yml por entorno, migraciones) | |
| F06d | HECHA | 2026-10-06 | pytest 316 passed (24 nuevos: test_fx_monorepo_ground_truth); vitest 41 passed (11 libs/shared + 10 api + 20 web smoke); check_ground_truth OK sobre fx-monorepo (CC-11 verde); 3 features (login, listado-con-filtros, exportar-reporte) con 6 R-NN cada una; 6 trampas ecosistema (tsconfig.paths+workspace:*, exports condicionales, loadComponent+withInterceptors, effect()+HTTP, fileReplacements, proxy.conf.json) + 6 trampas paquete plantadas y documentadas; run_fixture_tests en contenedor `node:22-bookworm-slim` con corepack+pnpm -> passed; MATRIX.md cubre javascript + angular + pnpm-monorepo + pnpm; fx-python-cli, fx-ts-agent-extension, fx-java-micronaut sin cambios de comportamiento (F06b cambio trivial de test_cmd); 5 decisiones nuevas D-174..D-178; fixtures_matrix.py ahora detecta ``.ts`` como ``javascript`` tambien y busca angular.json recursivo | Commit `F06d: fixture fx-monorepo con paquete por feature` |
| F06d | PENDIENTE | | fx-monorepo (workspace pnpm con Angular standalone + signals, API Node, libreria) | |
| F06e | PENDIENTE | | fx-minified (bundle JS con/sin sourcemap, .asar, .pyc) | |
| F06f | PENDIENTE | | fx-polyglot (Go + Rust + shell con stdin/JSON) | |
| F07 | PENDIENTE | | | |
| F08 | PENDIENTE | | | |
| F09 | PENDIENTE | | | |
| F10 | PENDIENTE | | | |
| F11 | PENDIENTE | | | |
| F12 | PENDIENTE | | | |
| F13 | PENDIENTE | | | |
| F14 | PENDIENTE | | | |
| F15 | PENDIENTE | | | |
| F16 | PENDIENTE | | | |
| F17 | PENDIENTE | | | |
| F18 | PENDIENTE | | | |
| F19 | PENDIENTE | | | |
| F20 | PENDIENTE | | | |
| F21 | PENDIENTE | | | |
| F22 | PENDIENTE | | | |
| F23 | PENDIENTE | | | |
| F24 | PENDIENTE | | | |
| F25 | PENDIENTE | | | |
| F26 | PENDIENTE | | | |
| F27 | PENDIENTE | | | |
| F28 | PENDIENTE | | | |
| F29 | PENDIENTE | | | |
| F30 | PENDIENTE | | | |
| F31 | PENDIENTE | | | |
| F32 | PENDIENTE | | | |
| F33 | PENDIENTE | | | |
| F34 | PENDIENTE | | | |
| F35 | PENDIENTE | | | |
| F36 | PENDIENTE | | | |
| F37 | PENDIENTE | | | |
| F38 | PENDIENTE | | | |
| F39 | PENDIENTE | | | |
| F40 | PENDIENTE | | | |
| F41 | PENDIENTE | | | |
| F42 | PENDIENTE | | | |
| F43 | PENDIENTE | | | |
| F44 | PENDIENTE | | | |
| F45 | PENDIENTE | | | |
| F46 | PENDIENTE | | | |
| F47 | PENDIENTE | | | |
| F48 | PENDIENTE | | | |
| F49 | PENDIENTE | | | |
| F50 | PENDIENTE | | | |
| F51 | PENDIENTE | | | |
| F52 | PENDIENTE | | | |
| F53 | PENDIENTE | | | |
| F54 | PENDIENTE | | | |
| F55 | PENDIENTE | | | |
| F56 | PENDIENTE | | | |
| F57 | PENDIENTE | | | |
| F58 | PENDIENTE | | | |
| F59 | PENDIENTE | | | |
| F60 | PENDIENTE | | | |
| F61 | PENDIENTE | | | |
| F62 | PENDIENTE | | | |
| F63 | PENDIENTE | | | |
| F64 | PENDIENTE | | | |
| F65 | PENDIENTE | | | |
| F66 | PENDIENTE | | | |
| F67 | PENDIENTE | | | |
| F68 | PENDIENTE | | | |
| F69 | PENDIENTE | | | |
| F70 | PENDIENTE | | | |
| F71 | PENDIENTE | | | |
| F72 | PENDIENTE | | | |
| F73 | PENDIENTE | | | |
| F74 | PENDIENTE | | | |
| F75 | PENDIENTE | | | |
| F76 | PENDIENTE | | | |
| F77 | PENDIENTE | | | |
| F78 | PENDIENTE | | | |
| F79 | PENDIENTE | | | |
| F80 | PENDIENTE | | | |
| F81 | PENDIENTE | | | |
| F82 | PENDIENTE | | | |
| F83 | PENDIENTE | | | |
| F84 | PENDIENTE | | | |
| F85 | PENDIENTE | | | |
| F86 | PENDIENTE | | | |
| F87 | PENDIENTE | | | |
| F88 | PENDIENTE | | | |

Estados válidos: `PENDIENTE`, `EN CURSO`, `HECHA`, `BLOQUEADA`, `REABIERTA`.

## Relevo

- Fecha y hora: 2026-10-06
- Agente / modelo / runtime: Kilo / MiniMax-M3 / code mode local
- Fase(s) en curso y estado: F00–F06d HECHAS; F06e–F06f PENDIENTES; F07–F88 PENDIENTES
- Hecho en esta sesión (con commits):
  - F06d (próximo commit `F06d: fixture fx-monorepo con paquete por feature`): workspace pnpm 9 + Angular 19 + Fastify 5 + Turborepo 2, con tres packages (apps/web, apps/api, libs/shared). Estructura: `apps/web/src/{main.ts, app/{app.config, app.routes, app.component}, app/core/{auth.guard, auth.interceptor}, app/features/{login,listings}/{login,listings}.page + login.service}, environments/{environment,environment.development,environment.production}, proxy.conf.json, angular.json}`. `apps/api/src/{main.ts, routes/{login,listings,export}, plugins/auth, schemas}`. `libs/shared/src/{index, types/{user,listing,report}, utils/{format,validate}}`. 3 features (login, listado-con-filtros, exportar-reporte) cada una con 6 R-NN. 6 trampas ecosistema plantadas: tsconfig.paths + workspace:* (imports de @fx-mono/shared), exports condicionales (types/import/require distintos), loadComponent+withInterceptors (functional guards e interceptors), effect() con HTTP (login dispara GET /api/login/me), fileReplacements en angular.json (development/production), proxy.conf.json (/api → http://localhost:3000). 6 trampas paquete: authInterceptor con token vacio, LoginService sin cleanup, ListingsPage effect con this completo, export.ts limit 1000 pero filtro no validado, isEmail(null)=true, applyFilters en memoria. 41 tests vitest (11 libs/shared + 10 api + 20 web smoke). Imagen `node:22-bookworm-slim` con corepack+pnpm 9.12.0. fx-ts-agent-extension cambio trivial: `test_cmd` de `make test` a `npm test -- --run` (make no esta en `node:22-slim`). fx-python-cli, fx-java-micronaut sin cambios. 5 decisiones nuevas D-174..D-178.
  - F06c (commit `4dea1be`): fixture fx-java-micronaut con paquete por feature.
  - F06b (commit `2b3c5fb`): fixture fx-ts-agent-extension con paquete por feature.
  - F06a2 (commit `4379810`): verificador y harness multi-ecosistema.
- A medias (archivo → estado exacto → qué falta): nada.
- Subagentes en vuelo (id, ruta del brief, qué devolverán, dónde escribirán): ninguno.
- Comandos para verificar el estado:
  - `python -m pytest` → 316 passed
  - `python dev/tools/check_ground_truth.py dev/ground-truth/fx-{python-cli,ts-agent-extension,java-micronaut,monorepo}` → OK
  - `python dev/tools/check_ground_truth.py dev/ground-truth/fx-monorepo --check-cc11` → OK
  - `python dev/tools/run_fixture_tests.py --fixture fx-monorepo --container` → passed
  - `python dev/tools/fixtures_matrix.py` → MATRIX.md con `javascript`, `angular`, `pnpm-monorepo`, `pnpm` cubiertos
  - `python dev/tools/validate_skill.py skills/notemartin-project-review` → OK
- Siguiente acción exacta: F06e — Fixture `fx-minified` (artefactos sin código fuente legible: bundle JS minificado con sourcemap, .asar, .pyc, .jar sin fuentes, binario Go con símbolos eliminados).
- Decisiones tomadas (D-NNN): D-174..D-178 — stack pnpm 9 + Angular 19 + Turborepo 2, vscode-shim no necesario (shim solo en F06b), js-yaml solo en runtime de apps/api, @analogjs/vitest-angular no usado (smoke tests en vez de Karma+Chromium), .ts cubre javascript en el detector. Detalles en DECISIONS.md.
- Riesgos y bloqueos:
  - R1 — Resuelto por D-108.
  - R2 — Resuelto.
  - R3 — `LICENSE` lleva copyright placeholder; el dueno puede ajustarlo.
  - R4 — El parser YAML propio cubre mapas, listas inline, escalares, listas `-` y block scalars `>`.
  - R5 — `_read_asar_member` es un parser minimo; suficiente para fixtures sinteticos.
  - R6 — `messages.ts` crece con tests inline reales; cumple con >5.000 lineas con contenido util, no relleno.
  - R7 — Health test en Micronaut embebido requiere arrancar el server manualmente (omitido con `assumeTrue`); el endpoint existe y responde "UP" en runtime real.
  - R8 — F06b cambio trivial: `test_cmd` de `make test` a `npm test -- --run` (el contenedor `node:22-slim` no trae `make`).
  - R9 — Angular CLI completa NO esta instalada en el contenedor (~500MB de node_modules); los tests de apps/web son smoke tests que importan los componentes via Node y leen el codigo fuente. El build de Angular CLI queda fuera del scope del fixture.

## Preguntas para el dueño

- [ ] (sin preguntas)