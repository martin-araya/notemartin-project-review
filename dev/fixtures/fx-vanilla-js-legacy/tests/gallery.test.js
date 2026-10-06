// tests/gallery.test.js
// Verifica la trampa paquete #5: $.fn.colorbox debe estar disponible
// despues de cargar jquery + plugin.
describe('FEAT-003 galeria (frontend)', function () {
  beforeEach(function () {
    document.body.innerHTML =
      '<select id="fx-gallery-filter"><option value=""></option><option value="paisajes">Paisajes</option></select>' +
      '<div id="fx-gallery-status"></div>' +
      '<ul id="fx-gallery-list"></ul>';
  });

  it('$.fn.colorbox esta definido tras cargar jquery + plugin', function () {
    expect(typeof global.$.fn.colorbox).toBe('function');
  });

  it('Array.prototype.shuffle queda definido por el plugin (monkey-patch)', function () {
    expect(typeof Array.prototype.shuffle).toBe('function');
    var a = [1, 2, 3];
    var b = a.shuffle();
    expect(b).not.toBe(a); // devuelve copia
    expect(b.length).toBe(3);
  });

  it('colorbox dispara el custom event fxcolorbox:open', function () {
    var fired = null;
    global.$(document).on('fxcolorbox:open', function (ev, payload) { fired = payload; });
    var $a = global.$('<a href="/img/x.jpg" title="t">x</a>');
    $a.colorbox();
    $a.trigger('click');
    expect(fired).toBeDefined();
    expect(fired.src).toBe('/img/x.jpg');
    expect(fired.title).toBe('t');
  });
});
