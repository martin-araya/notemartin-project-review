// tests/contact.test.js
// Verifica la superficie del feature de contacto a nivel de DOM.
describe('FEAT-002 formulario-de-contacto (frontend)', function () {
  beforeEach(function () {
    document.body.innerHTML =
      '<form id="fx-contact-form">' +
      '<input type="email" name="email" value="user@example.com">' +
      '<textarea name="message">hola</textarea>' +
      '<div id="fx-contact-output"></div>' +
      '</form>';
    global.fxLoadAppSources();
  });

  it('expone window.submitContact tras cargar contact.js', function () {
    expect(typeof window.submitContact).toBe('function');
  });

  it('App.run("submitContact") ejecuta el handler', function () {
    var called = false;
    window.submitContact = function () { called = true; return 'ok'; };
    var result = window.App.run('submitContact');
    expect(called).toBe(true);
    expect(result).toBe('ok');
  });

  it('App.run("submit-contact") cae en unknown_action (mismatch con HTML)', function () {
    var result = window.App.run('submit-contact');
    expect(result).toBe('unknown_action');
  });
});
