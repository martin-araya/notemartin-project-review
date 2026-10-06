// tests/traps_ecosystem.test.js
// Verifica la presencia de las 6 trampas del ecosistema plantadas.
var fs = require('fs');
var path = require('path');

describe('Trampas del ecosistema (CC-06)', function () {
  var root = path.join(__dirname, '..');

  function read(rel) {
    return fs.readFileSync(path.join(root, rel), 'utf8');
  }

  it('TRAP-E01: orden de <script> en index.html respeta la cadena jQuery -> colorbox -> app -> gallery', function () {
    var html = read('public/index.html');
    var jq = html.indexOf('jquery-3.7.1.min.js');
    var cb = html.indexOf('jquery.colorbox.js');
    var dp = html.indexOf('dispatch.js');
    var ap = html.indexOf('/js/app.js');
    var ga = html.indexOf('gallery.js');
    expect(jq).toBeGreaterThan(-1);
    expect(cb).toBeGreaterThan(jq);
    expect(dp).toBeGreaterThan(cb);
    expect(ap).toBeGreaterThan(dp);
    expect(ga).toBeGreaterThan(ap);
  });

  it('TRAP-E02: delegacion de eventos en document para #fx-search-form', function () {
    var src = read('public/js/search.js');
    expect(src).toMatch(/\$\(document\)\.on\(['"]submit['"],\s*['"]#fx-search-form['"]/);
  });

  it('TRAP-E03: handlers inline en index.html', function () {
    var html = read('public/index.html');
    expect(html).toMatch(/onclick=["']window\.App\.run\(/);
  });

  it('TRAP-E04: monkey-patching de Array.prototype y $.fn.colorbox en el plugin', function () {
    var plugin = read('public/js/plugins/jquery.colorbox.js');
    expect(plugin).toMatch(/Array\.prototype\.shuffle/);
    expect(plugin).toMatch(/\$\.fn\.colorbox/);
  });

  it('TRAP-E05: dispatch por string con window[name] y whitelist', function () {
    var src = read('public/js/dispatch.js');
    expect(src).toMatch(/window\[name\]/);
    expect(src).toMatch(/knownActions/);
  });

  it('TRAP-E06: clase CSS is-premium aplicada desde JS y definida en SCSS', function () {
    var scss = read('public/scss/_hidden.scss');
    var js = read('public/js/search.js');
    var html = read('public/index.html');
    expect(scss).toMatch(/\.is-premium/);
    expect(js).toMatch(/is-premium/);
    // La trampa aparece tambien en la respuesta del backend.
    expect(html).toMatch(/<script src="\/js\/jquery/);
  });
});
