// tests/dispatch.test.js
// Verifica la trampa ecosistema #5: window[name]() con whitelist que no
// incluye la accion solicitada.
describe('FEAT-001 busqueda - dispatch por string', function () {
  beforeEach(function () {
    document.body.innerHTML = '<div id="out"></div>';
    global.fxLoadAppSources();
  });

  it('AppCall con accion valida (camelCase) llama a window[name]', function () {
    window.openSearch = function () { return 'opened'; };
    var r = window.AppCall('openSearch');
    expect(r).toBe('opened');
  });

  it('AppCall con string de guion devuelve unknown_action (trampa paquete #4)', function () {
    var r = window.AppCall('open-search');
    expect(r).toBe('unknown_action');
  });

  it('AppCall lista solo las acciones validas (no "open-search")', function () {
    expect(window.AppKnownActions).toEqual(['openSearch', 'loadGallery', 'submitContact']);
    expect(window.AppKnownActions.indexOf('open-search')).toBe(-1);
  });
});
