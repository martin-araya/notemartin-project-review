// tests/traps_superficial.test.js
// Verifica la presencia de las 3 trampas superficiales.
var fs = require('fs');
var path = require('path');

describe('Trampas superficiales (CC-05)', function () {
  var root = path.join(__dirname, '..');
  function read(rel) { return fs.readFileSync(path.join(root, rel), 'utf8'); }

  it('SUPERFICIAL-1: deadCode.js existe y exporta 4 funciones no usadas', function () {
    var src = read('server/lib/deadCode.js');
    expect(src).toMatch(/uniqueId/);
    expect(src).toMatch(/deburr/);
    expect(src).toMatch(/template/);
    expect(src).toMatch(/shuffle/);
  });

  it('SUPERFICIAL-2: plugin jquery.debounce.js existe y nadie lo invoca', function () {
    var plugin = read('public/js/plugins/jquery.debounce.js');
    expect(plugin).toMatch(/\$\.fn\.debounce/);
    // Ningun otro archivo del proyecto usa $.fn.debounce.
    function checkNoUsage(dir) {
      var entries = fs.readdirSync(dir);
      for (var i = 0; i < entries.length; i++) {
        var full = path.join(dir, entries[i]);
        var stat = fs.statSync(full);
        if (stat.isDirectory()) {
          if (entries[i] === 'node_modules' || entries[i] === 'dist') continue;
          checkNoUsage(full);
        } else if (/\.js$/.test(entries[i]) && !/jquery\.debounce\.js$/.test(entries[i])) {
          var t = fs.readFileSync(full, 'utf8');
          expect(t).not.toMatch(/\$\.fn\.debounce/);
        }
      }
    }
    checkNoUsage(path.join(root, 'public'));
  });

  it('SUPERFICIAL-3: getGalleryAsCSV existe pero no se invoca en rutas', function () {
    var gallery = read('server/routes/gallery.js');
    expect(gallery).toMatch(/getGalleryAsCSV/);
    // index.js monta galleryModule.router pero no llama getGalleryAsCSV.
    var index = read('server/index.js');
    expect(index).not.toMatch(/getGalleryAsCSV/);
  });
});
