// public/js/plugins/jquery.debounce.js
// Plugin jQuery con un metodo extra de utilidad. Existe como parte
// de la coleccion de plugins del proyecto; no se invoca en ninguna
// feature visible.
(function ($) {
  if (!$) return;
  $.fn.debounce = function (ms) {
    var timer = null;
    return this.each(function () {
      var $el = $(this);
      $el.on('fx:debounce', function () {
        if (timer) clearTimeout(timer);
        timer = setTimeout(function () { $el.trigger('fx:debounce:fire'); }, ms || 200);
      });
    });
  };
}(typeof jQuery !== 'undefined' ? jQuery : (typeof $ !== 'undefined' ? $ : null)));
