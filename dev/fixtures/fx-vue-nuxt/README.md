# Fixture F06j — fx-vue-nuxt

Aplicacion **Nuxt 3** con Vue 3 (`<script setup>`), Pinia y Nitro.
Plantada para que la skill tenga que rastrear indirecciones propias
del ecosistema Nuxt: auto-imports sin `import`, middlewares via
`definePageMeta`, plugins con `provide`, rutas de servidor por
nombre de archivo, `defineModel` + `emits` y cross-store en Pinia.

## Stack

- **Frontend:** Nuxt 3.13 + Vue 3.5 con Composition API y `<script setup>`.
- **Estado:** Pinia 2.x + `@pinia/nuxt`.
- **Server API:** Nitro (rutas en `server/api/` por convencion de
  nombre de archivo + metodo HTTP).
- **Validacion:** Zod en rutas de servidor.
- **CSS:** Sass via preprocesador built-in de Nuxt.
- **Tests:** Vitest 1 + @nuxt/test-utils 3 + happy-dom.

## Como se ejecutan los tests

```bash
make test           # npx vitest run
make build          # nuxt prepare (genera .nuxt/)
make history        # regenera la historia git (8 commits)
```

En contenedor:

```bash
python dev/tools/run_fixture_tests.py --fixture fx-vue-nuxt --container
```

## Estructura

- `nuxt.config.ts`: configuracion Nuxt (modulos, css, runtimeConfig).
- `app.vue`: layout raiz con `<NuxtLayout><NuxtPage /></NuxtLayout>`.
- `pages/`: paginas con auto-imports; `reservas/[id].vue` usa route
  param dinamico.
- `components/`: `ReservaCard`, `ReservaForm`, `PerfilEditor`,
  `NotificacionItem`, `HiddenPremium`.
- `composables/`: `useReservas`, `useProfile`, `useDateFmt` (este
  ultimo sin uso, dead code).
- `stores/`: `reservations`, `profile`, `notifications` (este ultimo
  llama a `reservations.cancelar` desde su action).
- `middleware/`: `auth.global.ts` (global), `reservas-only.ts` (named).
- `plugins/`: `0.api-base.ts` (provide `$api`), `1.i18n.ts` (provide
  `$t` con fallback silencioso).
- `server/api/`: `reservas.get.ts`, `reservas.post.ts`,
  `reservas/[id].delete.ts`, `profile.get.ts`, `profile.patch.ts`,
  `notifications.get.ts`.
- `server/utils/db.ts`: store en memoria con seed.
- `assets/css/`: estilos con clases que ocultan features.
- `tests/`: 6 archivos Vitest.

## Features

1. **reservas**: listado, creacion, eliminacion, cross-store con
   notifications. 7 R-NN.
2. **perfil**: edicion, validacion, middleware auth (con bug de
   loop). 7 R-NN.
3. **notificaciones**: listado, mark read, cross-store a
   reservations. 7 R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06): auto-imports, definePageMeta middleware,
  plugins provide, server/api por nombre, defineModel+emits con bug
  preventDefault, cross-store Pinia.
- 6 del paquete (CC-04): useDateFmt unused, plugin $t fallback
  silencioso, action sin validar permisos, fetch sin timeout, v-model
  string vs Zod Date, auth.global redirect loop.
- 3 superficiales (CC-05): useDateFmt, seedReservasExtra, HiddenPremium
  import explicito.