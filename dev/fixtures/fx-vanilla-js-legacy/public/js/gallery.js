// public/js/gallery.js
// FEAT-XXX. Llama a $().colorbox() en document.ready. Si los scripts
// se reordenan, $.fn.colorbox queda undefined y se muestra un
// mensaje visible en la UI.
(function () {
  'use strict';

  function renderGallery(items) {
    var $list = $('#fx-gallery-list');
    if (!items || items.length === 0) {
      $list.html('<li class="empty">Sin imagenes.</li>');
      return;
    }
    var html = '';
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      html += '<li class="gallery-item" data-id="' + it.id + '">' +
              '<a href="' + it.src + '" title="' + it.alt + '">' +
              '<img src="' + it.src + '" alt="' + it.alt + '"></a></li>';
    }
    $list.html(html);
  }

  $(document).ready(function () {
    if (typeof $.fn.colorbox !== 'function') {
      $('#fx-gallery-status').html('<p class="error">Gallery no disponible (plugin no cargado).</p>');
      return;
    }

    $.getJSON('/api/gallery', function (data) {
      renderGallery(data.items);
      $('#fx-gallery-list .gallery-item a').colorbox({ title: function () { return $(this).attr('title'); } });
    });
  });

  // Delegacion del filtro de categoria.
  $(document).on('change', '#fx-gallery-filter', function () {
    var cat = $(this).val();
    $.getJSON('/api/gallery', { category: cat }, function (data) {
      renderGallery(data.items);
    });
  });

  window.loadGallery = function () {
    $.getJSON('/api/gallery', function (data) { renderGallery(data.items); });
  };
}());
