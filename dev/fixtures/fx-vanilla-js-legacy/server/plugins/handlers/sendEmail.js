// server/plugins/handlers/sendEmail.js
// Handler real de envio de email. La clave real del registry lo
// monta como 'send-email' (kebab-case), por lo que las llamadas
// desde las rutas deben respetar esa convencion.
function run(payload, cb) {
  if (!payload || !payload.to) {
    return cb(new Error('to required'));
  }
  // En produccion iria SMTP; aqui solo devolvemos OK.
  return cb(null, { ok: true, sentTo: payload.to });
}

module.exports = { run: run };
