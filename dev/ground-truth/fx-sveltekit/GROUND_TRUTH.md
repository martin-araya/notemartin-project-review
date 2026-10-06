# Ground truth de fx-sveltekit (F06k)

Aplicacion **SvelteKit 2** con Svelte 5 (runes `$state`, `$derived`,
`$effect`), `adapter-node`, file-based routing y form actions
(`?/create`, `?/delete`, `?/compartir`). Plantada para que la
skill tenga que rastrear indirecciones del ecosistema SvelteKit:
convenciones de archivos, `load` server vs universal, hooks
globales, runes y stores con `cross-store` semantica incorrecta.

## Features

1. **tareas** (FEAT-001): list, create, delete con form actions
   `?/create` y `?/delete`. 7 R-NN.
2. **etiquetas** (FEAT-002): catalogo + filtro por titulo con
   `$derived`. 7 R-NN.
3. **compartir** (FEAT-003): `?/compartir` con validacion Zod y
   `redirect 303`. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. **file_conventions**: `+page.svelte` + `+page.server.ts` +
   `+layout.{svelte,server.ts}` + `[id]/`. La skill debe derivar
   rutas y handlers del nombre de archivo y sufijo `.server.ts`.
2. **load_universal_vs_server**: `+layout.server.ts` define
   `LayoutServerLoad` con side effect. Las paginas tienen su
   propio load que recibe parent data.
3. **form_actions_enhance**: `<form method="POST" action="?/create"
   use:enhance>`. Action `?/foo` (inexistente) devuelve 404
   silencioso.
4. **hooks_handle**: `src/hooks.server.ts:handle` inyecta
   `locals.user` y anade `x-fx-auth: always` sin validar.
5. **runes**: `$state`, `$derived`, `$effect` en TagPicker y
   en /etiquetas.
6. **alias_lib**: imports usan `$lib/...` (mapea a `src/lib/`).

## Trampas del paquete (CC-04)

1. **dead_code_composable**: `utils/formatDate.ts` exporta
   `formatDate()` que nadie invoca.
2. **store_cross_call_semantic**: `shareStore.compartir` llama a
   `tasks.remove(id)` en vez de crear un share; la cross-store
   semantica es incorrecta.
3. **handle_no_auth_check**: hooks nunca falla, cualquier
   peticion llega como 'autenticada'.
4. **effect_memory_leak**: `$effect` con `setInterval` que solo
   se limpia al desmontar (raro en SvelteKit).
5. **action_not_found_silent**: `?/foo` no se maneja; SvelteKit
   devuelve 404 sin redirect.
6. **load_with_side_effect**: `+layout.server.ts` llama a
   `seedTareasExtra(1)` con prob 0.05 en cada peticion.

## Trampas superficiales (CC-05)

1. **dead_code_util**: `formatDate` (idem P01).
2. **dead_code_function**: `seedTareasExtra` (idem P06 como side
   effect).
3. **explicit_import_breaks_convention**: `+page.svelte` importa
   HiddenPremium con path explicito (es lo mismo que el
   shortform `$lib/components/HiddenPremium.svelte` pero lo hace
   dead-import).

## Archivos clave del fixture

- `svelte.config.js`: `adapter-node` + `vitePreprocess`.
- `vite.config.ts`: plugin de SvelteKit + Vitest 2.
- `src/hooks.server.ts`: middleware global con handle.
- `src/lib/server/{db,auth,types}.ts`: store + sesion + interfaces.
- `src/lib/stores/{tasks,tags,share}.svelte.ts`: stores Svelte 5
  con rune `$state`.
- `src/lib/components/`: TaskCard, TaskForm, TagPicker,
  ShareButton, HiddenPremium.
- `src/lib/utils/`: `formatDate.ts` (dead), `slugify.ts`.
- `src/routes/`: `+layout.{svelte,server.ts}`, `+page.svelte`,
  `tareas/{+page.svelte,+page.server.ts,[id]/+page.svelte,
  [id]/+page.server.ts}`, `etiquetas/{+page.svelte,+page.server.ts}`,
  `compartir/{+page.svelte,+page.server.ts}`.
- `src/styles/`: main.scss + _hidden.scss.
- `tests/`: 6 archivos Vitest.
