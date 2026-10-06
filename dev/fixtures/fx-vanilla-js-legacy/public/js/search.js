// public/js/search.js
// FEAT-XXX. La logica se monta por delegacion de eventos en document,
// no atada al HTML. La clase .is-premium se aplica a resultados
// premium y el CSS la oculta.
(function () {
  'use strict';

  $(document).on('submit', '#fx-search-form', function (ev) {
    ev.preventDefault();
    var $form = $(this);
    var q = $form.find('input[name="q"]').val();
    var $out = $('#fx-search-output');
    if (!q || !q.trim()) {
      $out.html('<p class="error">Escribe un termino.</p>');
      return;
    }
    $.getJSON('/api/search', { q: q }, function (data) {
      if (data && data.error) {
        $out.html('<p class="error">' + (data.message || data.error) + '</p>');
        return;
      }
      $out.html('<ul class="fx-results">' + (data.html || '') + '</ul>');
      $out.find('li.is-premium').each(function () {
        $(this).attr('title', 'Contenido premium');
      });
    });
  });

  // Abre el formulario.
  window.openSearch = function () {
    $('#fx-search-output').html('<p>Buscador abierto.</p>');
  };

  // Enganche del link superior.
  $(document).on('click', '#fx-open-search-link', function (ev) {
    ev.preventDefault();
    var result = window.App.run('open-search');
    if (result === 'unknown_action') {
      $('#fx-search-output').html('<p class="error">Accion no disponible.</p>');
    }
  });
}());
