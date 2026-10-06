// server/routes/search.js
// Endpoint del modulo de texto. Devuelve HTML en linea para terminos
// cortos y JSON estructurado para terminos de 3+ caracteres. Los items
// con premium=true reciben la clase CSS que el frontend sabe ocultar.
var express = require('express');
var items = require('../data/items');
var sanitize = require('../lib/sanitize');

var router = express.Router();

function isInjection(value) {
  return /[<>"]/.test(String(value || ''));
}

router.get('/', function (req, res) {
  var q = (req.query.q || '').toString();
  if (!q || q.trim().length === 0) {
    return res.status(400).json({ error: 'q_missing', message: 'Parametro q obligatorio' });
  }
  if (isInjection(q)) {
    return res.status(400).json({ error: 'q_invalid', message: 'Caracteres no permitidos en q' });
  }
  var lower = q.toLowerCase();
  if (lower.length < 3) {
    // Rama con resultados parciales: concatena HTML sin escape.
    var inline = '';
    items.forEach(function (it) {
      if (it.name.toLowerCase().indexOf(lower) !== -1) {
        inline += '<li class="item ' + (it.premium ? 'is-premium' : '') + '">' +
                  it.name + ' - ' + it.price + ' EUR</li>';
      }
    });
    return res.status(200).json({ mode: 'partial', html: inline, count: inline ? inline.split('</li>').length - 1 : 0 });
  }
  var found = items.filter(function (it) {
    return it.name.toLowerCase().indexOf(lower) !== -1;
  });
  var html = found.map(function (it) {
    return '<li class="item ' + (it.premium ? 'is-premium' : '') + '">' +
           sanitize.escapeHtml(it.name) + ' - ' + it.price + ' EUR</li>';
  }).join('');
  return res.status(200).json({ mode: 'full', html: html, count: found.length, items: found });
});

module.exports = router;
