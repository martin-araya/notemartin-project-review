// server/plugins/handlers/searchItems.js
function run(query, cb) {
  var items = require('../../data/items');
  var q = String(query || '').toLowerCase();
  var found = items.filter(function (it) {
    return it.name.toLowerCase().indexOf(q) !== -1;
  });
  return cb(null, found);
}

module.exports = { run: run };
