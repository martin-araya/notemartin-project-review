// server/plugins/handlers/listGallery.js
function run(category, cb) {
  var gallery = require('../../data/gallery');
  if (!category) return cb(null, gallery);
  var filtered = gallery.filter(function (it) { return it.category === category; });
  return cb(null, filtered);
}

module.exports = { run: run };
