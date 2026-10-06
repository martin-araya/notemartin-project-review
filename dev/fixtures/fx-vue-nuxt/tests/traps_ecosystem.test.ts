// tests/traps_ecosystem.test.js
// Verifica la presencia literal de las 6 trampas del ecosistema
// plantadas en el codigo del fixture.
var fs = require('fs');
var path = require('path');

describe('Trampas del ecosistema (CC-06)', function () {
  var root = path.join(__dirname, '..');
  function read(rel) { return fs.readFileSync(path.join(root, rel), 'utf8'); }

  it('TRAP-E01: pages/reservas/index.vue no tiene lineas de import (auto-imports)', function () {
    var src = read('pages/reservas/index.vue');
    var bloque = src.substring(src.indexOf('<script'), src.indexOf('</script>'));
    expect(bloque).not.toMatch(/^import\s+/m);
  });

  it('TRAP-E02: pages/reservas/index.vue define middleware via definePageMeta', function () {
    var src = read('pages/reservas/index.vue');
    expect(src).toMatch(/definePageMeta\s*\(\s*\{[^}]*middleware/);
  });

  it('TRAP-E03: plugins/ proveen $api y $t con provide', function () {
    var p1 = read('plugins/0.api-base.ts');
    var p2 = read('plugins/1.i18n.ts');
    expect(p1).toMatch(/provide:\s*\{\s*api/);
    expect(p2).toMatch(/provide:\s*\{\s*t\b/);
  });

  it('TRAP-E04: server/api/ define rutas por nombre de archivo + metodo', function () {
    var root = path.join(__dirname, '..');
    var files = fs.readdirSync(path.join(root, 'server/api'));
    expect(files).toContain('reservas.get.ts');
    expect(files).toContain('reservas.post.ts');
    expect(files.some(function (f) { return f.startsWith('reservas'); })).toBe(true);
  });

  it('TRAP-E05: components/ReservaForm.vue usa defineModel y defineEmits', function () {
    var src = read('components/ReservaForm.vue');
    expect(src).toMatch(/defineModel/);
    expect(src).toMatch(/defineEmits/);
  });

  it('TRAP-E06: stores/notifications.ts llama a la store de otro modulo', function () {
    var src = read('stores/notifications.ts');
    expect(src).toMatch(/useReservationsStore/);
    expect(src).toMatch(/\.cancelar\(/);
  });
});
