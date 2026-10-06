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
| F06i | HECHA | 2026-10-06 | pytest 521 passed (74 nuevos en test_fx_vanilla_js_legacy_ground_truth.py: 12 TestGroundTruthShape + 3 TestUniqueTokensFile + 2 TestAllCitesValid + 19 TestJqueryStructure + 5 TestJquerySource + 5 TestServerSource + 7 TestTrapsEcosystem + 5 TestTrapsPackage + 3 TestTrapsSuperficial + 4 TestManifest + 9 TestGroundTruthDocs); jest 39 tests passed (api 12 + search 4 + contact 4 + gallery 3 + dispatch 3 + traps_ecosystem 6 + traps_package 6 + traps_superficial 3); check_ground_truth OK sobre fx-vanilla-js-legacy con --check-cc11 OK; fixture completo con Node 22 + Express 4 CommonJS + jQuery 3.7.1 + plugin colorbox (monkey-patching Array.prototype.shuffle + $.fn.colorbox) + plugin debounce (no usado) + validator + multer 1.x + lodash + Gulp 4; server/ (index.js bootstrap, routes/{search,contact,gallery}.js, plugins/registry.js + handlers/{sendEmail,searchItems,listGallery}.js, data/{items,gallery}.js, lib/{sanitize,deadCode}.js); public/ (index.html + search.html + contact.html + gallery.html con orden de scripts deliberado y onclick inline, js/jquery-3.7.1.min.js real (88KB), js/plugins/{jquery.colorbox,jquery.debounce}.js, js/{app,search,contact,gallery,dispatch}.js, scss/{main,_variables,_mixins,_hidden}.scss, css/main.css compilado, gulpfile.js); 3 features (busqueda, formulario-de-contacto, galeria) con 7 R-NN cada una; 6 trampas ecosistema (script order, event delegation, inline handlers, prototype mutation, string dispatch, html-concat+css-hide); 6 trampas paquete (registry case mismatch sendEmail vs send-email, sanitize unused en partial, XSS via concat, whitelist mismatch camelCase vs kebab, colorbox race, multer threshold mismatch 1MB vs 500KB); 3 trampas superficiales (deadCode lodash con 4 funciones no usadas, plugin debounce no invocado, getGalleryAsCSV no enrutado); 8 tests jest + setup.js con env detection (node vs jsdom); Dockerfile.test con `node:22-bookworm-slim`; fixtures_matrix.py extendido para detectar `gulp` (gulpfile.js) y `jquery` (package.json dep); target_matrix.yml anadido `frameworks: [jquery]` y `build_systems: [gulp]`; MATRIX.md muestra fx-vanilla-js-legacy cubriendo jquery, gulp, javascript, source-text; fx-python-cli, fx-ts-agent-extension, fx-java-micronaut, fx-monorepo, fx-minified, fx-polyglot, fx-react-spa, fx-nextjs-fullstack sin cambios de comportamiento; validate_skill y overfit_guard siguen verdes; 3 decisiones nuevas D-195..D-197 (stack del fixture, naming prefix, target_matrix update) | Commit `F06i: fixture fx-vanilla-js-legacy con paquete por feature` |
| F06j | HECHA | 2026-10-06 | pytest 589 passed (68 nuevos en test_fx_vue_nuxt_ground_truth.py: 12 TestGroundTruthShape + 3 TestUniqueTokensFile + 2 TestAllCitesValid + 16 TestNuxtStructure + 12 TestNuxtSource + 6 TestTrapsEcosystem + 6 TestTrapsPackage + 3 TestTrapsSuperficial + 4 TestManifest + 7 TestManifest fixtures); vitest 27 tests passed (reservas 4 + perfil 4 + notifications 4 + traps_ecosystem 6 + traps_package 6 + traps_superficial 3) en 6 archivos; check_ground_truth OK sobre fx-vue-nuxt con --check-cc11 OK; fixture completo con Nuxt 3.13 + Vue 3.5 con `<script setup>` + Pinia 2.2 + @pinia/nuxt + Nitro + zod 3.23 + Sass; pages/ (index.vue con auto-imports y dead-import de HiddenPremium, reservas/index.vue con definePageMeta + middleware reservas-only, reservas/[id].vue con useAsyncData y route param, perfil/index.vue con definePageMeta + middleware global auth, notificaciones/index.vue con filtro all/unread); components/ (ReservaCard con clase premium-hide, ReservaForm con defineModel + defineEmits + preventDefault, PerfilEditor dead code, NotificacionItem con clase archived, HiddenPremium dead-import); composables/ (useReservas con $fetch sin retry, useProfile con computed reactivos, useDateFmt dead code, useSession para auth); stores/ (reservations con cancelar sin owner check, profile con getters isPremium/role, notifications con markRead cross-store a reservations.cancelar); middleware/ (auth.global.ts con redirect a /login sin comprobar ruta, reservas-only.ts para premium); plugins/ (0.api-base.ts provee $api, 1.i18n.ts provee $t con fallback silencioso); server/api/ (reservas.get.ts con filtro, reservas.post.ts con zod safeParse, reservas/[id].delete.ts sin owner check, profile.get.ts, profile.patch.ts con validacion email, notifications.get.ts); server/utils/db.ts con seed en memoria (12 items + 3 perfiles + 3 notificaciones) y seedExtra dead code; assets/css/ (main.scss + _hidden.scss con clase premium-hide); types/index.ts con interfaces Reserva/Profile/Notificacion; 3 features (reservas, perfil, notificaciones) con 7 R-NN cada una; 6 trampas ecosistema (auto_imports, define_page_meta, plugin_provide, server_api_by_name, define_model_emits, pinia_cross_store); 6 trampas paquete (dead_code_composable, i18n_silent_fallback, store_no_owner_check, fetch_no_retry, vmodel_string_vs_date, auth_redirect_loop); 3 trampas superficiales (useDateFmt, seedExtra, HiddenPremium import explicito); 6 archivos vitest con happy-dom + alias ~/; Dockerfile.test con `node:22-bookworm-slim` + `nuxt prepare`; fixtures_matrix.py extendido para detectar `nuxt` (PACKAGE_JSON_MARKERS) y `nuxt.config.ts` (FRAMEWORK_FILES); target_matrix.yml anadido `frameworks: [nuxt]`; MATRIX.md muestra fx-vue-nuxt cubriendo nuxt, vue-spa, javascript, source-text, ademas de los axes ya cubiertos; fx-python-cli, fx-ts-agent-extension, fx-java-micronaut, fx-monorepo, fx-minified, fx-polyglot, fx-react-spa, fx-nextjs-fullstack, fx-vanilla-js-legacy sin cambios de comportamiento; validate_skill y overfit_guard siguen verdes; 3 decisiones nuevas D-198..D-200 | Commit `F06j: fixture fx-vue-nuxt con paquete por feature` |
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
- Fase(s) en curso y estado: F00–F06j HECHAS; F07–F88 PENDIENTES
- Hecho en esta sesión (con commits):
  - F06j (commit `F06j: fixture fx-vue-nuxt con paquete por feature`): aplicacion Nuxt 3.13 con Vue 3.5 (`<script setup>` + Composition API), Pinia 2.2 + `@pinia/nuxt`, Nitro para `server/api/`, zod 3.23 para validacion en server, Sass built-in, Vitest 3 + `@nuxt/test-utils` 3 + happy-dom para tests. 3 features (reservas, perfil, notificaciones) con 7 R-NN cada una. pages/ con 5 archivos: index (landing con auto-imports y dead-import de HiddenPremium), reservas/index (definePageMeta + middleware reservas-only), reservas/[id] (useAsyncData + route param), perfil/index (definePageMeta + middleware global auth), notificaciones/index (filtro all/unread). components/ con ReservaCard (clase premium-hide), ReservaForm (defineModel + defineEmits + preventDefault), PerfilEditor (dead), NotificacionItem (clase archived), HiddenPremium (dead-import con ruta completa). composables/ con useReservas ($fetch sin retry), useProfile (computed reactivos), useDateFmt (dead), useSession. stores/ con reservations (cancelar sin owner check), profile (getters isPremium/role), notifications (markRead cross-store a reservations.cancelar). middleware/ con auth.global.ts (redirect /login sin comprobar ruta destino) y reservas-only.ts (premium). plugins/ con 0.api-base.ts (provee $api) y 1.i18n.ts (provee $t con fallback silencioso). server/api/ con 6 endpoints (reservas.get/post + [id].delete, profile.get/patch, notifications.get) con zod safeParse en POST/PATCH. server/utils/db.ts con seed en memoria (12 items + 3 perfiles + 3 notificaciones) y seedExtra dead code. assets/css/ con main.scss + _hidden.scss (clase premium-hide). 27 tests vitest passed (reservas 4 + perfil 4 + notifications 4 + traps_ecosystem 6 + traps_package 6 + traps_superficial 3) en 6 archivos. 68 tests pytest nuevos en test_fx_vue_nuxt_ground_truth.py (10 clases: TestGroundTruthShape, TestUniqueTokensFile, TestAllCitesValid, TestNuxtStructure, TestNuxtSource, TestTrapsEcosystem, TestTrapsPackage, TestTrapsSuperficial, TestManifest, TestGroundTruthDocs). 28 unique tokens con prefijo NPRGT-FXVUE- sin fugas en el fixture. CC-11 cerrado tras eliminar el path-file-prefix de los comentarios (los archivos `tests/perfil.test.ts`, `server/api/reservas.get.ts`, `server/api/reservas.post.ts` y `server/api/reservas/[id].delete.ts` tenian menciones del nombre de feature en la primera linea de comentario; renombradas a comentarios genericos). fixtures_matrix.py extendido: `nuxt` -> `nuxt` en PACKAGE_JSON_MARKERS, `nuxt.config.ts` -> `nuxt` en FRAMEWORK_FILES. target_matrix.yml anadido frameworks: [nuxt]. MATRIX.md muestra fx-vue-nuxt cubriendo nuxt, vue-spa, javascript, source-text. Regresion verificada en los 9 fixtures previos: check_ground_truth OK (10/10). validate_skill y overfit_guard siguen verdes. pytest total 589 passed (521 anteriores + 68 nuevos). 3 decisiones nuevas D-198..D-200.
  - F06i (commit previo `b0f7bc4`): fx-vanilla-js-legacy con paquete por feature.
  - F06h (commit previo): fixture fx-nextjs-fullstack con paquete por feature.
  - F06g..F06b: fx-react-spa, fx-polyglot, fx-minified arreglado, fx-monorepo, fx-java-micronaut, fx-ts-agent-extension.
  - F06a2 (commit previo): verificador y harness multi-ecosistema.
- A medias (archivo → estado exacto → qué falta): nada.
- Subagentes en vuelo (id, ruta del brief, qué devolverán, dónde escribirán): ninguno.
- Comandos para verificar el estado:
  - `PYTHONPATH=. .venv/bin/pytest dev/tests/ -q` → 589 passed
  - `PYTHONPATH=. .venv/bin/python dev/tools/check_ground_truth.py dev/ground-truth/fx-vue-nuxt --check-cc11` → OK
  - `PYTHONPATH=. .venv/bin/python dev/tools/fixtures_matrix.py` → MATRIX.md con `nuxt` y `vue-spa` cubiertos por fx-vue-nuxt
  - `PYTHONPATH=. .venv/bin/python dev/tools/validate_skill.py skills/notemartin-project-review` → OK
  - `cd dev/fixtures/fx-vue-nuxt && npx vitest run` → 27 passed en 6 archivos
- Siguiente acción exacta: F07 — Umbrales canónicos (dev/evals/thresholds.json) y Anexo C; depende de F06 (cualquier subfase HECHA).
- Decisiones tomadas (D-NNN): D-198..D-200. D-198: stack del fixture (Nuxt 3.13 + Vue 3.5 + Pinia 2.2 + Nitro + zod 3.23 + Sass + Vitest 3 + happy-dom). D-199: prefijo NPRGT-FXVUE- para 28 unique tokens. D-200: extension de target_matrix.yml con frameworks: [nuxt] + deteccion en fixtures_matrix.py (nuxt en PACKAGE_JSON_MARKERS, nuxt.config.ts en FRAMEWORK_FILES).
- Riesgos y bloqueos:
  - R1..R14 — riesgos previos resueltos o documentados.
  - R15 — fx-vue-nuxt usa Vitest 3.2 con @nuxt/test-utils 3.14 (peer dep exige Vitest 3.x). Si en el futuro se quiere bajar a Vitest 1/2 habra que migrar la config. CC-11 obligo a eliminar el `// archivo.ts` de la primera linea de los tests y archivos de server/api que tenian el nombre de feature en el path.

## Preguntas para el dueño

- [ ] (sin preguntas)