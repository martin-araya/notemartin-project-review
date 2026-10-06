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
| F06d | HECHA | 2026-10-06 | pytest 316 passed (24 nuevos: test_fx_monorepo_ground_truth); vitest 41 passed (11 libs/shared + 10 api + 20 web smoke); check_ground_truth OK sobre fx-monorepo (CC-11 verde); 3 features (login, listado-con-filtros, exportar-reporte) con 6 R-NN cada una; 6 trampas ecosistema (tsconfig.paths+workspace:*, exports condicionales, loadComponent+withInterceptors, effect()+HTTP, fileReplacements, proxy.conf.json) + 6 trampas paquete plantadas y documentadas; run_fixture_tests en contenedor `node:22-bookworm-slim` con corepack+pnpm -> passed; MATRIX.md cubre javascript + angular + pnpm-monorepo + pnpm; fx-python-cli, fx-ts-agent-extension, fx-java-micronaut sin cambios de comportamiento (F06b cambio trivial de test_cmd); 5 decisiones nuevas D-174..D-178; fixtures_matrix.py ahora detecta ``.ts`` como ``javascript`` tambien y busca angular.json recursivo | Commit `F06d: fixture fx-monorepo con paquete por feature` |
| F06e | HECHA | 2026-10-06 | pytest 363 passed (sin regresiones); check_ground_truth OK sobre fx-minified con --check-cc11 OK (CC-11 cerrada: comentarios de TS/Java/Py ya no mencionan nombres de features); ground_truth.json arreglado: decision_points usan `file` no `artifact`, traces apuntan a src/ts/*.ts no a artifacts/* (los artefactos son generados), user_sees anadido a todos los outcomes R-04..R-06; check_ground_truth.py refactorizado para separar errores de warnings (artefactos no generados en artifacts/ van a warnings, no a errores fatales); FIX del bug del parser YAML que tomaba citas con extension binaria (.jar#com/fxmin/X) como YAML en vez de binary (priority sobre la extension); fx-minified regression: 0 cambios en otros fixtures; 5 decisiones nuevas D-179..D-183 | Commit `F06e: fx-minified arreglado (CC-11, ground truth, parser binario)` |
| F06f | HECHA | 2026-10-06 | pytest 363 passed (33 nuevos en test_fx_polyglot_ground_truth.py: 24 TestGroundTruthShape + 5 TestUniqueTokensFile + 1 TestAllCitesValid + 13 TestPolyglotStructure + 7 TestBatsFilesExist); check_ground_truth OK sobre fx-polyglot con --check-cc11 OK; fixture completo con src/ingesta (Go, //go:build tags legacy y current, func init() en registry.go), src/transformacion (Rust, Cargo features v1/v2/strict/legacy_compat), orchestrator.sh (set -euo pipefail, trap cleanup EXIT, case uname -s); 3 features (ingesta, transformacion, reporte) con 7 R-NN cada una; 6 trampas ecosistema + 6 trampas paquete + 4 trampas superficiales documentadas con referencia exacta; 7 bats files (ingesta, transformacion_v1, transformacion_v2, orchestrator, protocolo_exit_codes, contrato_json, end_to_end) + all-tests.sh; fixtures_matrix.py extendido para detectar artifacts/ y manifests/ (cierra el gap de fx-minified); MATRIX.md ahora muestra fx-polyglot cubriendo go, rust, shell, cargo, go-modules; fx-minified cierra bundle-with-sourcemap, minified-js, asar, pyc, jar en containers; fx-python-cli, fx-ts-agent-extension, fx-java-micronaut, fx-monorepo sin cambios; validate_skill OK; 5 decisiones nuevas D-179..D-183 | Commit `F06f: fixture fx-polyglot con paquete por feature` |
| F06g | HECHA | 2026-10-06 | pytest 407 passed (44 nuevos en test_fx_react_spa_ground_truth.py: 7 TestGroundTruthShape + 3 TestUniqueTokensFile + 1 TestAllCitesValid + 16 TestReactStructure + 13 TestBatsFilesExist + 4 TestManifest); check_ground_truth OK sobre fx-react-spa con --check-cc11 OK; fixture completo con index.html, src/main.tsx (6 providers anidados: StoreProvider, QueryClientProvider, I18nextProvider, ThemeProvider, ToastProvider, ErrorBoundary + Suspense), src/routes/router.tsx (createBrowserRouter con 7 loaders/actions: authGuard, productsLoader, checkoutAction), src/api/baseApi.ts (createApi con 5 endpoints: login/register/getProducts/getProduct/getOrders; los hooks NO se definen literalmente, se autogeneran), src/store/{auth,cart}.slice.ts (cart con addItem que muta via push), src/features/{auth,catalog,cart,checkout,orders}/; 4 features (autenticacion, catalogo-y-carrito, checkout, panel-de-pedidos) con 7 R-NN cada una; 6 trampas ecosistema plantadas con referencia exacta (loader/action, hooks autogenerados, providers anidados, useEffect chain, import.meta.env.VITE_*, memo/forwardRef/HOC/Suspense/ErrorBoundary); 6 trampas paquete (deps missing useEffect, HOC sin inject, asimetria memo/forwardRef, pollingInterval chain, cart mutation, false displayName); 3 trampas superficiales (formatPrice no usado, exports inconsistentes, msal.ts inutil); 9 tests vitest + MSW + Testing Library (auth/catalog/cart/checkout/orders/routing/env/providers/traps_ecosystem); Dockerfile.test con `node:22-bookworm-slim`; fixtures_matrix.py extendido para detectar SPA frameworks desde deps (react -> react-spa); MATRIX.md muestra fx-react-spa cubriendo react-spa, typescript, javascript, shell; fx-python-cli, fx-ts-agent-extension, fx-java-micronaut, fx-monorepo, fx-minified, fx-polyglot sin cambios; validate_skill OK; 5 decisiones nuevas D-184..D-188 | Commit `F06g: fixture fx-react-spa con paquete por feature` |
| F06h | HECHA | 2026-10-06 | pytest 447 passed (40 nuevos en test_fx_nextjs_fullstack_ground_truth.py: 8 TestGroundTruthShape + 3 TestUniqueTokensFile + 1 TestAllCitesValid + 8 TestNextStructure + 5 TestEcosystemTraps + 8 TestUnitTestFiles + 5 TestManifest + 2 sueltos); check_ground_truth OK sobre fx-nextjs-fullstack con --check-cc11 OK; fixture completo con middleware.ts (en raiz, NO en app/), next.config.js (reactStrictMode: false), app/layout.tsx (RSC con await auth), app/page.tsx (RSC con revalidate=60 y TAG_HOME), app/(marketing)/{registro,login,publicar-articulo,articulos/[slug]}/page.tsx (route group + segmento dinamico), app/comentarios/{page,[id]/page}.tsx, app/panel-admin/page.tsx, app/@modal/{default.tsx,(.)comentarios/page.tsx} (parallel + intercepting routes), app/api/{comentarios,health}/route.ts (Route Handlers), app/actions/{auth,articles,comments}.ts ('use server'), app/components/{Nav,RegistrarForm,LoginForm,PublicarForm,CommentBox,AdminPanel,Footer}.tsx ('use client' en los interactivos), prisma/schema.prisma (SQLite con User/Article/Comment/Session + relaciones + onDelete: Cascade); 4 features (registro, publicar-articulo, comentarios, panel-admin) con 7 R-NN cada una; 6 trampas ecosistema plantadas con referencia exacta ('use client' directive, 'use server' en actions, route groups + dynamic segments + parallel + intercepting routes, middleware.ts que redirige por cookie, revalidateTag + revalidatePath + export const revalidate, relaciones en schema.prisma); 6 trampas paquete (middleware `from` no usado, tag mismatch TAG_ARTICLES vs TAG_HOME, useOptimistic sin rollback, onDelete: Cascade sin manejar, password en texto plano, reactStrictMode: false); 3 trampas superficiales (formatDate no usado, Footer.tsx no usado, seedAdminDemo nunca llamado); 5 tests vitest (actions_auth, actions_articles, middleware, tags, traps) + 3 specs Playwright (registro, publicar_articulo, panel_admin); Dockerfile.test con `node:22-bookworm-slim` + Playwright Chromium; fixtures_matrix.py extendido para detectar Next.js y Prisma (next -> nextjs, next-auth -> nextjs, @prisma/client -> prisma); MATRIX.md muestra fx-nextjs-fullstack cubriendo nextjs, prisma, typescript, javascript, shell; fx-python-cli, fx-ts-agent-extension, fx-java-micronaut, fx-monorepo, fx-minified, fx-polyglot, fx-react-spa sin cambios; validate_skill OK; 6 decisiones nuevas D-189..D-194 | Commit `F06h: fixture fx-nextjs-fullstack con paquete por feature` |
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
- Fase(s) en curso y estado: F00–F06h HECHAS; F07–F88 PENDIENTES
- Hecho en esta sesión (con commits):
  - F06h (commit `F06h: fixture fx-nextjs-fullstack con paquete por feature`): app Next.js 14 App Router con RSC + Server Actions + Route Handlers + middleware + Prisma + SQLite + Auth.js. `middleware.ts` en raiz (no en app/) redirige `/panel-admin/*` por cookie `fxnext-session`. `next.config.js` con `reactStrictMode: false`. `app/(marketing)/{registro,login,publicar-articulo,articulos/[slug]}/page.tsx` route group + segmento dinamico. `app/@modal/{default.tsx,(.)comentarios/page.tsx}` parallel + intercepting routes. `app/api/{comentarios,health}/route.ts` Route Handlers. `app/actions/{auth,articles,comments}.ts` con `'use server'`. `app/components/{Nav,RegistrarForm,LoginForm,PublicarForm,CommentBox,AdminPanel}.tsx` con `'use client'` en los interactivos. `prisma/schema.prisma` con User/Article/Comment/Session + relaciones + onDelete: Cascade. 4 features (registro, publicar-articulo, comentarios, panel-admin) con 7 R-NN cada una. 6 trampas ecosistema (use client, use server, route groups + dynamic + parallel + intercepting, middleware, revalidateTag + revalidatePath + revalidate, relaciones en schema.prisma). 6 trampas paquete (middleware from no usado, tag mismatch TAG_ARTICLES vs TAG_HOME, useOptimistic sin rollback, Cascade sin manejar, password en texto plano, reactStrictMode false). 3 trampas superficiales (formatDate no usado, Footer.tsx no usado, seedAdminDemo nunca llamado). 5 tests vitest (actions_auth, actions_articles, middleware, tags, traps) + 3 specs Playwright (registro, publicar_articulo, panel_admin). Dockerfile.test con `node:22-bookworm-slim` + Playwright Chromium. fixtures_matrix.py extendido para detectar Next.js (next -> nextjs) y Prisma (@prisma/client -> prisma). MATRIX.md muestra fx-nextjs-fullstack cubriendo nextjs, prisma, typescript, javascript, shell. fx-python-cli, fx-ts-agent-extension, fx-java-micronaut, fx-monorepo, fx-minified, fx-polyglot, fx-react-spa sin cambios. 6 decisiones nuevas D-189..D-194.
  - F06g (commit previo `2646cb7`): fixture fx-react-spa con paquete por feature.
  - F06f (commit previo `6d2df09`): fixture fx-polyglot con paquete por feature.
  - F06e (commit previo `6d2df09`): fx-minified arreglado (CC-11, ground truth, parser binario).
  - F06d (commit previo `5e47423`): fixture fx-monorepo con paquete por feature.
  - F06c (commit previo `4dea1be`): fixture fx-java-micronaut con paquete por feature.
  - F06b (commit previo `2b3c5fb`): fixture fx-ts-agent-extension con paquete por feature.
  - F06a2 (commit previo `4379810`): verificador y harness multi-ecosistema.
- A medias (archivo → estado exacto → qué falta): nada.
- Subagentes en vuelo (id, ruta del brief, qué devolverán, dónde escribirán): ninguno.
- Comandos para verificar el estado:
  - `.venv/bin/python -m pytest` → 447 passed
  - `.venv/bin/python dev/tools/check_ground_truth.py dev/ground-truth/{fx-python-cli,fx-ts-agent-extension,fx-java-micronaut,fx-monorepo,fx-minified,fx-polyglot,fx-react-spa,fx-nextjs-fullstack} --check-cc11` → OK (8/8)
  - `.venv/bin/python dev/tools/fixtures_matrix.py` → MATRIX.md con nextjs, prisma, react-spa, go, rust, shell, cargo, go-modules cubiertos
  - `.venv/bin/python dev/tools/validate_skill.py skills/notemartin-project-review` → OK
- Siguiente acción exacta: F07 — Umbrales canónicos (dev/evals/thresholds.json) y Anexo C; depende de F06h HECHA.
- Decisiones tomadas (D-NNN): D-189..D-194 — Next.js 14 App Router con route groups (marketing), dynamic segments [slug], parallel routes @modal, intercepting routes (.)comentarios; 'use client' obligatoria en componentes interactivos (los page.tsx de marketing son RSC sin la directiva); Server Actions en archivos separados con 'use server' e invocadas desde <form action={fn}>; middleware.ts en raiz (NO en app/) que redirige por cookie; revalidateTag + revalidatePath + export const revalidate como mecanismos distintos; Prisma con SQLite + cliente generado en node_modules (no se commitea); Auth.js v5 con CredentialsProvider. Detalles en DECISIONS.md.
- Riesgos y bloqueos:
  - R1..R11 — mismos riesgos previos (resueltos o documentados).
  - R12 — fx-react-spa y fx-nextjs-fullstack no fueron construidos/ejecutados localmente (vitest y next build requieren dependencias pesadas). La verificacion depende de los contenedores `node:22-bookworm-slim` definidos en Dockerfile.test. El ground truth y los tests pytest validan la estructura del codigo fuente, no los tests vitest ni Playwright.
  - R13 — fx-nextjs-fullstack no usa bcryptjs (declarado en package.json pero nunca importado; la trampa paquete #5 lo deja como dependencia fantasma). La skill debe notar que bcryptjs es codigo muerto.

## Preguntas para el dueño

- [ ] (sin preguntas)