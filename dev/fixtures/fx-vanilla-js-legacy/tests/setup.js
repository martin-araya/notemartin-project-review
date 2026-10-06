// tests/setup.js
// Configuracion global de Jest: expone jQuery en el entorno jsdom
// para que los tests puedan operar sobre el DOM.
var path = require('path');
var fs = require('fs');

// Solo configuramos el entorno DOM si hay window (jsdom). En node
// (tests/api.test.js) este archivo se ignora efectivamente.
if (typeof window === 'undefined' || typeof document === 'undefined') {
  module.exports = {};
} else {

// Carga jQuery real (v3.7.1) desde public/js. Como es un .min.js sin
// exports, lo evaluamos en el contexto global del test.
var jqSrc = fs.readFileSync(path.join(__dirname, '..', 'public', 'js', 'jquery-3.7.1.min.js'), 'utf8');
// eslint-disable-next-line no-eval
global.eval(jqSrc);
global.jQuery = global.$;

// Carga el plugin colorbox para los tests de imagenes.
var cbSrc = fs.readFileSync(path.join(__dirname, '..', 'public', 'js', 'plugins', 'jquery.colorbox.js'), 'utf8');
// eslint-disable-next-line no-eval
global.eval(cbSrc);

// Carga el plugin debounce (no usado en ninguna feature).
var debSrc = fs.readFileSync(path.join(__dirname, '..', 'public', 'js', 'plugins', 'jquery.debounce.js'), 'utf8');
// eslint-disable-next-line no-eval
global.eval(debSrc);

// Carga los modulos de la app.
var appSrc = fs.readFileSync(path.join(__dirname, '..', 'public', 'js', 'app.js'), 'utf8');
var searchSrc = fs.readFileSync(path.join(__dirname, '..', 'public', 'js', 'search.js'), 'utf8');
var contactSrc = fs.readFileSync(path.join(__dirname, '..', 'public', 'js', 'contact.js'), 'utf8');
var gallerySrc = fs.readFileSync(path.join(__dirname, '..', 'public', 'js', 'gallery.js'), 'utf8');
var dispatchSrc = fs.readFileSync(path.join(__dirname, '..', 'public', 'js', 'dispatch.js'), 'utf8');

// Helpers para (re)cargar modulos despues de manipular el DOM.
function loadAppSources() {
  // eslint-disable-next-line no-eval
  global.eval(appSrc);
  // eslint-disable-next-line no-eval
  global.eval(searchSrc);
  // eslint-disable-next-line no-eval
  global.eval(contactSrc);
  // eslint-disable-next-line no-eval
  global.eval(gallerySrc);
  // eslint-disable-next-line no-eval
  global.eval(dispatchSrc);
}

global.fxLoadAppSources = loadAppSources;
module.exports = { loadAppSources: loadAppSources };
}
