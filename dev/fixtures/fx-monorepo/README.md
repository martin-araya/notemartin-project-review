# fx-monorepo (F06d)

Fixture de **monorepo TypeScript** orquestado con **Turborepo** sobre **pnpm
workspaces**. Modela la arquitectura de un producto real con frontend Angular,
backend Fastify y librería compartida.

## Estructura

```
.
├── apps/
│   ├── web/      Angular 19 (standalone + signals) — frontend
│   └── api/      Fastify 5 — backend REST
└── libs/
    └── shared/   Types + utils compartidos (@fx-mono/shared)
```

## Stack

- **pnpm** 9 con workspaces
- **Turborepo** 2 para orquestar tasks (`test`, `build`, `lint`)
- **Angular 19** (standalone components, signals, lazy routes)
- **Fastify 5** para la API
- **Vitest 1** como test runner
- **zod** para validación de payloads

## 3 features (cada una con ≥ 6 R-NN)

1. **FEAT-001 login** — POST `/api/login` + página `/login` con signals.
2. **FEAT-002 listado-con-filtros** — GET `/api/listings?status=&minPrice=&maxPrice=`
   + página `/listings` con `effect()` que dispara HTTP al cambiar filtros.
3. **FEAT-003 exportar-reporte** — POST `/api/export` con filtros, retorna CSV.

## 6 trampas del ecosistema (CC-06)

1. **`tsconfig.paths` + `workspace:*`**: el frontend importa `@fx-mono/shared`
   via path alias, y el `package.json` usa el protocolo `workspace:*` para
   que pnpm resuelva la versión correcta.
2. **`exports` condicionales en `package.json`**: `libs/shared/package.json`
   tiene entradas distintas para `types`/`import`/`require`.
3. **Rutas lazy + functional guards + `withInterceptors(...)`**: `app.routes.ts`
   usa `loadComponent`, `auth.guard.ts` es una `CanActivateFn`, y
   `provideHttpClient(withInterceptors([authInterceptor, loggingInterceptor]))`
   registra interceptors funcionales.
4. **`effect()` con HTTP**: `LoginComponent` usa `effect()` que dispara un GET
   a `/api/login/me` cuando el signal `token()` cambia.
5. **`fileReplacements` en `angular.json`**: las configuraciones `development`
   y `production` reemplazan `environment.ts` por sus variantes.
6. **`proxy.conf.json`**: el único lugar donde `/api` se redirige al backend
   en `http://localhost:3000`. El frontend siempre habla `/api/*`.

## 6 trampas del paquete (CC-04)

1. `authInterceptor` agrega `Authorization: Bearer <token>` siempre, incluso
   si el token es vacío.
2. `LoginService` no desuscribe del observable en ngOnDestroy (memory leak).
3. `ListingsPage.effect()` se dispara con CUALQUIER cambio de signal, no solo
   `filters()` (re-renders innecesarios).
4. `export.ts` no valida el tamaño del filtro: un array de 1M items genera
   un string OOM.
5. `validate.isEmail(null)` retorna `true` (combinación de tipos `string |
   null` con bug).
6. `listings.ts` aplica filtros en memoria en vez de en SQL (N+1 si hay
   10k items).

## Toolchain de tests

- **Node 22** en contenedor `node:22-bookworm-slim`.
- **pnpm 9.12.0** vía `corepack`.
- **Vitest** para libs/shared y apps/api (no requiere browser).
- **Smoke tests** para apps/web (verifican que los componentes y rutas
  se importan sin error; evitamos Karma+Chromium en CI).

## Ejecución

```bash
# Vía harness (recomendado — Docker automático)
python dev/tools/run_fixture_tests.py --fixture fx-monorepo

# Manual (requiere Node 22 + pnpm 9)
cd dev/fixtures/fx-monorepo
pnpm install
pnpm test
```

## Ground truth

`dev/ground-truth/fx-monorepo/ground_truth.json` documenta los 3 features con
sus trazas, decision points, outcomes, errores, configuración, estados,
telemetría, interacciones y callgraph.

## Notas

- **Sin red en runtime**: `pnpm install` se ejecuta dentro del build de
  Docker (donde hay red). El host de desarrollo no necesita conexión.
- **Sin Angular CLI instalado**: el build de Angular solo se valida como
  smoke test (import + type-check) en vitest. Un build real de Angular CLI
  (~500MB de dependencias) queda fuera del scope del fixture.
