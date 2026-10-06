// public/js/plugins/jquery.colorbox.js
// Plugin jQuery que anade $.fn.colorbox y una utilidad shuffle a
// Array.prototype. El plugin es necesario para la feature de imagenes;
// sin el, el frontend muestra un mensaje de "no disponible".
(function ($) {
  if (!$) return;
  if (!Array.prototype.shuffle) {
    Array.prototype.shuffle = function () {
      var arr = this.slice();
      for (var i = arr.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
      }
      return arr;
    };
  }
  $.fn.colorbox = function (options) {
    var settings = options || {};
    return this.each(function () {
      var $el = $(this);
      $el.on('click.fxcolorbox', function (ev) {
        ev.preventDefault();
        var src = $el.attr('href') || $el.data('src') || '';
        var title = settings.title || $el.attr('title') || '';
        $(document).trigger('fxcolorbox:open', [{ src: src, title: title }]);
      });
    });
  };
}(typeof jQuery !== 'undefined' ? jQuery : (typeof $ !== 'undefined' ? $ : null)));
