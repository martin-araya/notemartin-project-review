// public/js/contact.js
// FEAT-XXX. Envia el formulario por fetch a /api/contact y muestra
// el resultado. La cadena window[name] se materializa en otra
// pagina, no aqui.
(function () {
  'use strict';

  $(document).on('submit', '#fx-contact-form', function (ev) {
    ev.preventDefault();
    var $form = $(this);
    var formData = new FormData($form[0]);
    var $out = $('#fx-contact-output');
    $out.html('<p>Enviando...</p>');
    fetch('/api/contact', { method: 'POST', body: formData })
      .then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); })
      .then(function (resp) {
        var cls = 'info';
        if (resp.status >= 400) cls = 'error';
        if (resp.status === 200) cls = 'ok';
        $out.html('<p class="' + cls + '">' + (resp.body.message || JSON.stringify(resp.body)) + '</p>');
      })
      .catch(function (e) {
        $out.html('<p class="error">Error de red: ' + e.message + '</p>');
      });
  });

  window.submitContact = function () {
    $('#fx-contact-form').trigger('submit');
  };
}());
