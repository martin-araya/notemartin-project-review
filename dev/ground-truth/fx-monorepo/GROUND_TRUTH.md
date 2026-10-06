# Ground truth: fx-monorepo (F06d)

Fixture de monorepo pnpm + Angular + Fastify + libreria compartida, orquestado
con Turborepo. Modela la arquitectura de un producto real con frontend Angular,
backend Fastify y libreria compartida.

## Vision general

- **Stack:** pnpm 9 + Turborepo 2 + Angular 19 (standalone + signals) + Fastify 5
  + zod + Vitest 1.
- **Paquetes:** `apps/web` (frontend), `apps/api` (backend), `libs/shared`
  (libreria compartida con exports condicionales).
- **Orquestacion:** `pnpm test` corre `turbo run test` que invoca `vitest run`
  en cada workspace que tenga tests.
- **Imagen Docker:** `node:22-bookworm-slim` con corepack + pnpm 9.12.0.

## 3 features (cada una con >= 6 R-NN)

1. **FEAT-001 login** — POST `/api/login` con validacion zod, retorna token +
   user. El frontend guarda el token y dispara un `effect()` que llama a
   `/api/login/me`.
2. **FEAT-002 listado-con-filtros** — GET `/api/listings?status=&minPrice=`
   `&maxPrice=`. La pagina web tiene un `effect()` que se dispara con cada
   cambio de signal (no solo `filters`).
3. **FEAT-003 exportar-reporte** — POST `/api/export` con filtros + format
   (csv/json), retorna URL pre-firmada. Limite de 1000 rows.

## 6 trampas del ecosistema (CC-06)

1. **tsconfig.paths + workspace:***: apps/web importa `@fx-mono/shared`
   via path alias, y los package.json usan `workspace:*` para pnpm.
2. **Exports condicionales**: `libs/shared/package.json` tiene
   `types`/`import`/`require` distintos.
3. **Lazy routes + functional guards + `withInterceptors(...)`**:
   `loadComponent` con import() dinamico, `CanActivateFn` y `HttpInterceptorFn`
   como funciones, registrados via `provideHttpClient(withInterceptors([...]))`.
4. **`effect()` con HTTP**: `LoginPage.effectRef()` depende de `this.token`
   y dispara un GET cuando cambia.
5. **`fileReplacements` de environments**: las configs `development` y
   `production` de `angular.json` reemplazan `environment.ts`.
6. **`proxy.conf.json`**: el unico lugar donde `/api` se redirige al backend.

## 6 trampas del paquete (CC-04)

1. `authInterceptor` agrega `Authorization: Bearer ${token}` incluso con
   token vacio.
2. `LoginService` no desuscribe `pendingLogin` (memory leak).
3. `ListingsPage.effectRef()` lee `this` completo (N+1, re-fires innecesarios).
4. `export.ts` tiene limit de 1000 rows pero no valida el filtro de entrada
   (combinacion de setting + comportamiento).
5. `isEmail(null)` retorna `true` (bug en validacion de null).
6. `applyFilters` corre en memoria en vez de delegar a SQL.

## Decisiones y variantes

- **Imagen `node:22-bookworm-slim` con corepack**: la imagen oficial de
  Node + pnpm via corepack. Sin Gradle, sin wrapper de pnpm pregenerado.
- **`@analogjs/vitest-angular` no usado**: evitamos Karma + Chromium en CI.
  Los tests de Angular son smoke tests que importan los componentes via
  Node (sin browser) y verifican contenido del codigo fuente.
- **`fastify-plugin` para auth**: el plugin de auth usa `fastify-plugin` para
  escapar el encapsulamiento de Fastify y aplicar el hook a todas las rutas.
- **No Angular CLI build**: el fixture NO corre `ng build` (pesado). Solo
  valida que el module graph compila con tsc y que los smoke tests pasan.
