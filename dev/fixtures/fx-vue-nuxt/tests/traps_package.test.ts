// tests/traps_package.test.js
// Verifica la presencia de las 6 trampas del paquete plantadas.
var fs = require('fs');
var path = require('path');

describe('Trampas del paquete (CC-04)', function () {
  var root = path.join(__dirname, '..');
  function read(rel) { return fs.readFileSync(path.join(root, rel), 'utf8'); }

  it('TRAP-P01: composables/useDateFmt.ts existe pero no se invoca desde pages/components', function () {
    var src = read('composables/useDateFmt.ts');
    expect(src).toMatch(/formatDate/);
    var usaFecha = false;
    function walk(dir) {
      var entries = fs.readdirSync(dir);
      for (var i = 0; i < entries.length; i++) {
        var full = path.join(dir, entries[i]);
        var stat = fs.statSync(full);
        if (stat.isDirectory()) { walk(full); continue; }
        if (!/\.(vue|ts|js)$/.test(entries[i])) continue;
        if (entries[i] === 'useDateFmt.ts') continue;
        var t = fs.readFileSync(full, 'utf8');
        if (t.indexOf('useDateFmt') !== -1) usaFecha = true;
      }
    }
    walk(path.join(root, 'pages'));
    walk(path.join(root, 'components'));
    expect(usaFecha).toBe(false);
  });

  it('TRAP-P02: plugins/1.i18n.ts tiene fallback silencioso (return "" sin warn)', function () {
    var src = read('plugins/1.i18n.ts');
    expect(src).toMatch(/return\s+['"]['"]/);
    expect(src).not.toMatch(/console\.warn/);
  });

  it('TRAP-P03: stores/reservations.ts cancelar no valida owner', function () {
    var src = read('stores/reservations.ts');
    var start = src.indexOf('async cancelar');
    var end = src.indexOf('}\n    }', start);
    var body = src.substring(start, end === -1 ? src.length : end);
    expect(body).toMatch(/cancelar/);
    expect(body).not.toMatch(/owner|usuarioId|permisos/);
  });

  it('TRAP-P04: composables/useReservas.ts hace $fetch sin reintento', function () {
    var src = read('composables/useReservas.ts');
    expect(src).toMatch(/\$fetch/);
    expect(src).not.toMatch(/retry/);
  });

  it('TRAP-P05: components/ReservaForm.vue v-model fecha como string, server valida Date', function () {
    var form = read('components/ReservaForm.vue');
    var post = read('server/api/reservas.post.ts');
    expect(form).toMatch(/fecha\s*=\s*defineModel.*default/);
    expect(post).toMatch(/Date\.parse/);
  });

  it('TRAP-P06: middleware/auth.global.ts ignora to.path y redirige a /login siempre', function () {
    var src = read('middleware/auth.global.ts');
    expect(src).toMatch(/navigateTo\(['"]\/login['"]\)/);
    expect(src).not.toMatch(/to\.path/);
  });
});
