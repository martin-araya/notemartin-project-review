// server/routes/gallery.js
// Endpoint del modulo de imagenes. Ademas de getGallery() expone
// getGalleryAsCSV() accesible via /api/gallery/csv (no se invoca
// en el frontend).
var express = require('express');
var gallery = require('../data/gallery');

var router = express.Router();

function getGallery(category) {
  if (!category) return gallery;
  return gallery.filter(function (it) { return it.category === category; });
}

function getGalleryAsCSV(category) {
  var list = getGallery(category);
  return list.map(function (it) { return it.id + ',' + it.src + ',' + it.alt; }).join('\n');
}

router.get('/', function (req, res) {
  var category = (req.query.category || '').toString();
  var list = getGallery(category);
  return res.status(200).json({ items: list, count: list.length });
});

router.get('/csv', function (req, res) {
  var category = (req.query.category || '').toString();
  return res.type('text/csv').status(200).send(getGalleryAsCSV(category));
});

module.exports = { router: router, getGallery: getGallery, getGalleryAsCSV: getGalleryAsCSV };
