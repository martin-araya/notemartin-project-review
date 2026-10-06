// server/plugins/registry.js
// Registro global de handlers para los mensajes internos. Las claves
// se almacenan en kebab-case.
var handlers = {};
var initialized = false;

function init() {
  if (initialized) return;
  handlers['send-email']  = require('./handlers/sendEmail').run;
  handlers['search']      = require('./handlers/searchItems').run;
  handlers['list-gallery'] = require('./handlers/listGallery').run;
  initialized = true;
}

function get(name) {
  if (handlers.hasOwnProperty(name)) return handlers[name];
  return null;
}

function keys() {
  return Object.keys(handlers);
}

module.exports = { init: init, get: get, keys: keys };
