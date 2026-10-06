# Ground truth de fx-vanilla-js-legacy (F06i)

Aplicacion web legacy con frontend ES5 + jQuery 3.7 + plugin colorbox (lightbox)
y plugin debounce (sin uso) + HTML/CSS/SCSS + Gulp 4, y backend Express 4 en
CommonJS. Plantada para que la skill tenga que rastrear indirecciones
multi-capa (orden de scripts, delegacion de eventos, dispatch por string,
monkey-patching, registry case mismatch, XSS latente por concatenacion,
umbrales inconsistentes de multer).

## Features

1. **busqueda** (FEAT-001): `/api/search?q=` con filtro, escape, validacion y
   rama de clases CSS ocultas (`is-premium`). 7 R-NN.
2. **formulario-de-contacto** (FEAT-002): `POST /api/contact` con multer,
   evaluacion controlada y registry case mismatch. 7 R-NN.
3. **galeria** (FEAT-003): `/api/gallery` con filtro por categoria, lightbox
   colorbox, modo CSV disponible. 7 R-NN.

## Trampas del ecosistema (CC-06)

1. **script_order** (`public/index.html:34-41`): jquery -> colorbox -> debounce
   -> dispatch -> app -> search -> contact -> gallery. Reordenar rompe la
   galeria.
2. **event_delegation** (`public/js/search.js:11`, `public/js/gallery.js:40`):
   handlers enganchados a `document` con selectores lejanos.
3. **inline_handlers** (`public/index.html:17`): `<button onclick="window.App.run('loadGallery')">`.
4. **prototype_mutation** (`public/js/plugins/jquery.colorbox.js:8-16`):
   `Array.prototype.shuffle` y `$.fn.colorbox` anadidos por un plugin.
5. **string_dispatch** (`public/js/dispatch.js`, `public/js/app.js:20-28`):
   `App.run(name)` resuelve por string con whitelist camelCase; el HTML usa
   kebab-case, asi que `App.run('open-search')` devuelve `unknown_action`.
6. **html_concat_css_hide** (`public/scss/_hidden.scss:4` +
   `public/js/search.js:29` + `server/routes/search.js:31,41`): la clase
   `is-premium` cruza backend, JS de cliente y CSS.

## Trampas del paquete (CC-04)

1. **registry_case_mismatch** (`server/plugins/registry.js:11` +
   `server/routes/contact.js:33`): handler registrado como `send-email`,
   buscado como `sendEmail`. Siempre devuelve 500 `handler_not_found`.
2. **sanitize_unused** (`server/lib/sanitize.js` +
   `server/routes/search.js:26-35`): `escapeHtml` solo se usa en la rama
   full; la rama partial concatena HTML sin escapar.
3. **xss_via_concat** (`server/routes/search.js:31-32`): XSS latente en la
   rama partial.
4. **whitelist_mismatch** (`public/js/app.js:14-18` +
   `public/index.html:28`): whitelist camelCase vs HTML kebab-case.
5. **colorbox_race** (`public/js/gallery.js:28-31`): la feature se desactiva
   con un mensaje si el plugin no esta cargado.
6. **multer_threshold_mismatch** (`server/routes/contact.js:16,52`): multer
   acepta 1 MB, validacion interna rechaza 500 KB. Gap de 500 KB.

## Trampas superficiales (CC-05)

1. **dead_code** (`server/lib/deadCode.js`): reexporta `uniqueId`, `deburr`,
   `template`, `shuffle` de lodash. Nadie las invoca.
2. **unused_plugin** (`public/js/plugins/jquery.debounce.js`): `$.fn.debounce`
   existe, nadie lo usa.
3. **dead_endpoint_export** (`server/routes/gallery.js:14-19`):
   `getGalleryAsCSV` se exporta pero `index.js` solo monta el router.

## Archivos clave del fixture

- `server/index.js`: bootstrap Express (sirve `/public`, monta `/api/*`).
- `server/routes/{search,contact,gallery}.js`: endpoints de las 3 features.
- `server/plugins/registry.js` + `handlers/`: registro de handlers por
  string.
- `server/data/{items,gallery}.js`: catalogos hardcoded.
- `server/lib/{sanitize,deadCode}.js`: utilidades.
- `public/index.html`: entrada HTML con orden de scripts y handlers inline.
- `public/js/{app,search,contact,gallery,dispatch}.js`: modulos de feature.
- `public/js/plugins/{jquery.colorbox,jquery.debounce}.js`: plugins jQuery.
- `public/scss/{main,_variables,_mixins,_hidden}.scss`: estilos con
  clases que ocultan features.
- `tests/`: 8 archivos Jest (api, search, contact, gallery, dispatch,
  traps_ecosystem, traps_package, traps_superficial, setup).
