# Fixture F06k — fx-sveltekit

Aplicacion **SvelteKit 2** con Svelte 5 (runes), `adapter-node`,
file-based routing y form actions. Plantada para que la skill
tenga que rastrear indirecciones del ecosistema SvelteKit:
convention de archivos (`+page.svelte`, `+page.server.ts`,
`+server.ts`, `hooks.server.ts`), `load` universal vs server,
form actions con `?/delete` + `use:enhance`, runes
(`$state`, `$derived`, `$effect`), aliases `$lib` / `$env` y
stores cross-call en `*.svelte.ts`.

## Stack

- **Frontend:** SvelteKit 2.x + Svelte 5 con runes.
- **Server:** `adapter-node` para SSR en runtime Node.
- **Validacion:** Zod 3.23 en form actions.
- **Tests:** Vitest 2.1 + `@testing-library/svelte` 5.2.
- **CSS:** Sass 1.77.

## Como se ejecutan los tests

```bash
make test           # npm test -- --run (Vitest)
make build          # vite build
make history        # regenera la historia git (8 commits)
```

En contenedor:

```bash
python dev/tools/run_fixture_tests.py --fixture fx-sveltekit --container
```

## Estructura

- `svelte.config.js`: `adapter-node` + `vitePreprocess`.
- `vite.config.ts`: plugin de Svelte + configuracion de Vitest.
- `src/app.html`: shell HTML.
- `src/hooks.server.ts`: middleware global con `handle`.
- `src/lib/server/`: `db.ts` (seed en memoria), `auth.ts`
  (sesion stub).
- `src/lib/stores/`: `tasks.svelte.ts`, `tags.svelte.ts`,
  `share.svelte.ts` (cross-store).
- `src/lib/components/`: `TaskCard`, `TaskForm`, `TagPicker`,
  `ShareButton`, `HiddenPremium`.
- `src/lib/utils/`: `formatDate.ts` (dead code), `slugify.ts`.
- `src/routes/`: `+layout.{svelte,server.ts}`, `+page.svelte`,
  `tareas/{+page.svelte,+page.server.ts,[id]/+page.svelte,
  [id]/+page.server.ts}`, `etiquetas/{+page.svelte,+page.server.ts}`,
  `compartir/{+page.svelte,+page.server.ts}`.
- `src/styles/`: main.scss + _hidden.scss.
- `tests/`: 6 archivos Vitest.

## Features

1. **tareas** (FEAT-001): list, create, delete con form actions
   `?/create` y `?/delete`. 7 R-NN.
2. **etiquetas** (FEAT-002): assign cross-store + filter. 7 R-NN.
3. **compartir** (FEAT-003): share con validacion Zod y rate
   limit. 7 R-NN.

## Trampas plantadas

- 6 del ecosistema (CC-06): file conventions, load universal vs
  server, form actions, hooks.server.ts, runes, alias $lib.
- 6 del paquete (CC-04): formatDate unused, cross-store
  semantica incorrecta, hooks sin auth, $effect sin cleanup,
  action not found, load con side effect.
- 3 superficiales (CC-05): formatDate, seedTasksExtra,
  HiddenPremium dead-import.