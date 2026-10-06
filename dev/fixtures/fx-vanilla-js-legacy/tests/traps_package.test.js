// tests/traps_package.test.js
// Verifica la presencia de las 6 trampas del paquete plantadas.
var fs = require('fs');
var path = require('path');

describe('Trampas del paquete (CC-04)', function () {
  var root = path.join(__dirname, '..');
  function read(rel) { return fs.readFileSync(path.join(root, rel), 'utf8'); }

  it('TRAP-P01: registry registra send-email (kebab) y contact.js busca sendEmail (camel)', function () {
    var reg = read('server/plugins/registry.js');
    var contact = read('server/routes/contact.js');
    expect(reg).toMatch(/handlers\[['"]send-email['"]\]/);
    expect(contact).toMatch(/registry\.get\(['"]sendEmail['"]\)/);
  });

  it('TRAP-P02: lib/sanitize.js existe pero NO se usa en la rama partial de search', function () {
    var search = read('server/routes/search.js');
    var sanitize = read('server/lib/sanitize.js');
    expect(sanitize).toMatch(/escapeHtml/);
    // Quitamos los comentarios de bloque y de linea para no confundir
    // el test con menciones textuales.
    var code = search.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/.*$/gm, '');
    var idx = code.indexOf('lower.length < 3');
    expect(idx).toBeGreaterThan(-1);
    // Tomamos solo el cuerpo del if (hasta el matching `}`): lo
    // extraemos contando llaves. Esto evita que el bloque contenga
    // la rama `full` posterior donde SI se usa sanitize.escapeHtml.
    var bodyStart = code.indexOf('{', idx);
    var depth = 0;
    var end = bodyStart;
    for (var i = bodyStart; i < code.length; i++) {
      if (code[i] === '{') depth++;
      else if (code[i] === '}') {
        depth--;
        if (depth === 0) { end = i; break; }
      }
    }
    var block = code.substring(bodyStart, end + 1);
    // La rama partial concatena HTML sin escape.
    expect(block).toMatch(/inline \+= '<li/);
    expect(block).not.toMatch(/sanitize\.escapeHtml/);
  });

  it('TRAP-P03: XSS latente por concatenacion directa de item.name', function () {
    var search = read('server/routes/search.js');
    // La rama partial concatena it.name sin escapeHtml.
    expect(search).toMatch(/inline \+= '<li class="item ' \+ \(it\.premium/);
  });

  it('TRAP-P04: whitelist de AppActions usa camelCase y el HTML usa kebab-case', function () {
    var app = read('public/js/app.js');
    var html = read('public/index.html');
    // Whitelist en camelCase.
    expect(app).toMatch(/AppActions\s*=/);
    expect(app).toMatch(/['"]openSearch['"]/);
    expect(app).toMatch(/['"]loadGallery['"]/);
    expect(app).toMatch(/['"]submitContact['"]/);
    // HTML con kebab-case.
    expect(html).toMatch(/data-action=["']open-search["']/);
    // Verificacion runtime: cargamos app.js y comprobamos que
    // App.run devuelve 'unknown_action' para kebab-case.
    global.fxLoadAppSources();
    expect(window.App.run('open-search')).toBe('unknown_action');
    expect(window.App.run('openSearch')).not.toBe('unknown_action');
  });

  it('TRAP-P05: gallery.js valida $.fn.colorbox antes de usarlo', function () {
    var gallery = read('public/js/gallery.js');
    expect(gallery).toMatch(/Gallery no disponible/);
    expect(gallery).toMatch(/typeof \$\.fn\.colorbox/);
  });

  it('TRAP-P06: thresholds de multer (1MB) y validacion interna (500KB) son distintos', function () {
    var contact = read('server/routes/contact.js');
    expect(contact).toMatch(/fileSize:\s*1024\s*\*\s*1024/);   // multer 1MB
    expect(contact).toMatch(/file\.size\s*>\s*500\s*\*\s*1024/); // validacion 500KB
  });
});
