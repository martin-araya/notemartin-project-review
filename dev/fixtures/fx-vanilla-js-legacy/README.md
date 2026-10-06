# Fixture F06i — fx-vanilla-js-legacy

Aplicacion web **legacy sin framework moderno**: frontend ES5 + jQuery 3.7 + plugins + HTML/CSS/SCSS + Gulp, con backend Express 4 en CommonJS.

Stack:

- **Frontend:** JavaScript ES5 (`var`, funciones nombradas, sin arrow / `let` / `const` / template literals), jQuery 3.7, plugin jQuery `colorbox` (lightbox) que hace monkey-patching, plugin `debounce` (no usado), Gulp 4 (compila SCSS y minifica JS a `dist/`, opcional en CI).
- **Backend:** Node 22, Express 4 (CommonJS), `validator` (emails), `multer` (uploads con umbral), `lodash` (3 funciones usadas, 1 dead code export), `supertest` para tests de integracion.
- **Tests:** Jest 29 + jest-environment-jsdom + supertest.

## Como se ejecutan los tests

```bash
make test           # npm test -- --runInBand --verbose
make build          # compila SCSS a public/css/main.css
make history        # regenera la historia git (8 commits)
```

En contenedor:

```bash
python dev/tools/run_fixture_tests.py --fixture fx-vanilla-js-legacy --container
```

## Estructura

- `server/` — backend Express: `index.js`, `routes/{search,contact,gallery}.js`, `plugins/registry.js`, `data/{items,gallery}.js`, `lib/{sanitize,deadCode}.js`.
- `public/` — frontend estatico servido por Express:
  - `index.html`, `search.html`, `contact.html`, `gallery.html`.
  - `js/jquery-3.7.1.min.js` (real, sin sourcemap inline para no inflar el repo).
  - `js/plugins/{jquery.colorbox,jquery.debounce}.js`.
  - `js/{app,search,contact,gallery,dispatch}.js`.
  - `scss/{main,_variables,_mixins,_hidden}.scss` + `css/main.css` (generado, commiteado para CI sin Gulp).
- `tests/` — Jest con 8 archivos (search, contact, gallery, dispatch, traps_ecosystem, traps_package, api, setup).
- `gulpfile.js` — pipeline de build (opcional, no requerido por la suite Jest).

## Features

1. **busqueda** (FEAT-001): `/api/search?q=` con filtro, escape, validacion y rama de clases CSS ocultas.
2. **formulario-de-contacto** (FEAT-002): `POST /api/contact` con multer, evaluacion de whitelist, registry case mismatch.
3. **galeria** (FEAT-003): `/api/gallery` con filtro, lightbox colorbox, modo CSV no usado.

Cada feature tiene 7 R-NN documentados en `dev/ground-truth/fx-vanilla-js-legacy/ground_truth.json`.

## Trampas plantadas

- 6 del ecosistema (CC-06): orden de `<script>`, delegacion de eventos, handlers inline, mutacion de prototipos, `window[name]()` / `eval`, HTML concatenado y clases CSS que ocultan features.
- 6 del paquete (CC-04): registry case mismatch, sanitize unused, XSS latente por concatenacion, whitelist rota, colorbox race condition, multer thresholds mismatch.
- 3 superficiales (CC-05): deadCode lodash, plugin debounce no usado, getGalleryAsCSV no invocado.
