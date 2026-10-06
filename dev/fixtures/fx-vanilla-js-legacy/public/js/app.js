// public/js/app.js
// Entry point. Define window.App y conecta el bus de eventos del plugin
// colorbox. El orden de carga es critico: jQuery -> colorbox -> app.js.
window.App = window.App || {};

(function () {
  'use strict';

  // Whitelist de acciones conocidas. Coinciden con las funciones
  // window.openSearch, window.loadGallery, window.submitContact.
  // El HTML, en cambio, usa data-action en kebab-case.
  var AppActions = {
    'openSearch':    function () { return window.openSearch && window.openSearch(); },
    'loadGallery':   function () { return window.loadGallery && window.loadGallery(); },
    'submitContact': function () { return window.submitContact && window.submitContact(); }
  };

  function dispatch(name) {
    if (Object.prototype.hasOwnProperty.call(AppActions, name)) {
      return AppActions[name]();
    }
    return 'unknown_action';
  }

  // Escucha del custom event disparado por el plugin colorbox.
  $(document).on('fxcolorbox:open', function (ev, payload) {
    if (window.console && console.log) {
      console.log('[fxcolorbox] open', payload && payload.src);
    }
  });

  // Enganche de clicks en elementos con data-action.
  $(document).on('click', '[data-action]', function (ev) {
    var name = $(this).attr('data-action');
    dispatch(name);
  });

  window.App.run = dispatch;
  window.App.actions = AppActions;
}());
