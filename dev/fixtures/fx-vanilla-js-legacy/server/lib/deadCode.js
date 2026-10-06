// server/lib/deadCode.js
// Reexporta utilidades de lodash que el resto del servidor no invoca.
var _ = require('lodash');

module.exports = {
  uniqueId: function (prefix) { return _.uniqueId(prefix); },
  deburr: function (str) { return _.deburr(str); },
  template: function (tpl) { return _.template(tpl); },
  shuffle: function (arr) { return _.shuffle(arr); }
};
