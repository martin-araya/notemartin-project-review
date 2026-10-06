// public/js/dispatch.js
// String dispatch via window[name]() con whitelist declarada. La
// whitelist usa camelCase para coincidir con las funciones globales
// definidas por los modulos de feature.
(function () {
  'use strict';

  // Acciones validas (camelCase) usadas en el whitelist.
  var knownActions = ['openSearch', 'loadGallery', 'submitContact'];

  function callByName(name) {
    if (knownActions.indexOf(name) === -1) {
      return 'unknown_action';
    }
    if (typeof window[name] === 'function') {
      try { return window[name](); } catch (e) { return 'threw:' + e.message; }
    }
    return 'undefined';
  }

  window.AppCall = window.AppCall || callByName;
  window.AppKnownActions = knownActions;
}());
