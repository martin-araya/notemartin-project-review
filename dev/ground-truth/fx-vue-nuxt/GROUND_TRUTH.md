# Ground truth de fx-vue-nuxt (F06j)

Aplicacion **Nuxt 3** con Vue 3 (`<script setup>`), Pinia y Nitro.
Plantada para que la skill tenga que rastrear indirecciones propias
del ecosistema Nuxt: auto-imports sin `import`, middlewares via
`definePageMeta`, plugins con `provide`, rutas de servidor por
nombre de archivo + metodo HTTP, `defineModel` + `emits` y
cross-store en Pinia.

## Features

1. **reservas** (FEAT-001): listado, creacion, eliminacion,
   cross-store con notifications. 7 R-NN.
2. **perfil** (FEAT-002): edicion, validacion, middleware auth (con
   bug de loop). 7 R-NN.
3. **notificaciones** (FEAT-003): listado, mark read, cross-store a
   reservations. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. **auto_imports** (`pages/reservas/index.vue:1-27`): sin lineas de
   import. useReservas, useReservationsStore, ref, computed, onMounted,
   ReservaCard, ReservaForm entran via auto-imports de Nuxt.
2. **define_page_meta** (`pages/reservas/index.vue:6-8` +
   `pages/perfil/index.vue:4-6`): `middleware: ['reservas-only']`
   (named) y `['auth']` (global por sufijo `.global.ts`).
3. **plugin_provide** (`plugins/0.api-base.ts:21-23` +
   `plugins/1.i18n.ts:12-22`): $api y $t son globales sin import. El
   prefijo numerico del nombre (0., 1.) determina el orden de carga.
4. **server_api_by_name** (`server/api/reservas.get.ts` +
   `server/api/reservas.post.ts` + `server/api/reservas/[id].delete.ts`):
   Nitro mapea cada archivo a una ruta HTTP segun el patron
   `nombre.METHOD.ts`. reservas/[id].delete.ts -> DELETE
   /api/reservas/:id.
5. **define_model_emits** (`components/ReservaForm.vue:9-21`):
   defineModel para v-model personalizado y defineEmits para
   'submit'/'cancelar'. El preventDefault se aplica tambien al
   submit del padre (trampa).
6. **pinia_cross_store** (`stores/notifications.ts:39-52`): markRead
   importa useReservationsStore y llama a other.cancelar(id). Los
   ids no coinciden; la cancelacion falla con 404 silencioso.

## Trampas del paquete (CC-04)

1. **dead_code_composable** (`composables/useDateFmt.ts`): formatDate()
   que nadie invoca.
2. **i18n_silent_fallback** (`plugins/1.i18n.ts:18-21`): $t devuelve
   string vacio sin warn para claves no registradas.
3. **store_no_owner_check** (`stores/reservations.ts:46-55`): cancelar()
   no valida que el caller sea dueno del item.
4. **fetch_no_retry** (`composables/useReservas.ts:1-18`): $fetch
   directo sin reintento. Si el server cuelga, espera
   indefinidamente.
5. **vmodel_string_vs_date** (`components/ReservaForm.vue:9` +
   `server/api/reservas.post.ts:8`): fecha como string, server
   valida con Date.parse; inputs mal formados dan 400.
6. **auth_redirect_loop** (`middleware/auth.global.ts:5-11`): redirige
   a /login sin comprobar la ruta destino, generando bucle.

## Trampas superficiales (CC-05)

1. **dead_code_composable** (`composables/useDateFmt.ts`): formatDate()
   que nadie invoca.
2. **dead_code_function** (`server/utils/db.ts:80-90`): seedExtra(count)
   que la app no invoca.
3. **explicit_import_breaks_auto** (`pages/index.vue:10`): HiddenPremium
   se importa con ruta completa, rompiendo el patron de
   auto-imports.

## Archivos clave del fixture

- `nuxt.config.ts`: modulos (`@pinia/nuxt`), css (`~/assets/css/main.scss`),
  imports.dirs (`stores`), runtimeConfig.
- `app.vue`: layout raiz con `<NuxtLayout><NuxtPage /></NuxtLayout>`.
- `pages/`: `index.vue` (landing), `reservas/index.vue` (listado +
  form), `reservas/[id].vue` (detalle), `perfil/index.vue` (editor),
  `notificaciones/index.vue` (lista con filtro).
- `components/`: `ReservaCard`, `ReservaForm`, `PerfilEditor`,
  `NotificacionItem`, `HiddenPremium`.
- `composables/`: `useReservas`, `useProfile`, `useDateFmt` (dead),
  `useSession`.
- `stores/`: `reservations`, `profile`, `notifications` (cross-store).
- `middleware/`: `auth.global.ts` (global), `reservas-only.ts` (named).
- `plugins/`: `0.api-base.ts` ($api), `1.i18n.ts` ($t).
- `server/api/`: `reservas.get.ts`, `reservas.post.ts`,
  `reservas/[id].delete.ts`, `profile.get.ts`, `profile.patch.ts`,
  `notifications.get.ts`.
- `server/utils/db.ts`: store en memoria con seed.
- `assets/css/`: estilos con clases que ocultan features.
- `tests/`: 6 archivos Vitest (reservas, perfil, notifications,
  traps_ecosystem, traps_package, traps_superficial).
