// server/routes/contact.js
// Endpoint POST /api/contact con multer. Acepta un adjunto opcional.
// El handler de envio se busca por nombre en el registry de plugins.
var express = require('express');
var multer = require('multer');
var validator = require('validator');
var registry = require('../plugins/registry');

var upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 1024 * 1024 }
});

var router = express.Router();

router.post('/', upload.single('attachment'), function (req, res) {
  var body = req.body || {};
  var file = req.file;

  if (!body.email || !validator.isEmail(String(body.email))) {
    return res.status(400).json({ error: 'invalid_email', message: 'Email no valido' });
  }

  // Busqueda del handler por nombre. La clave real registrada es
  // 'send-email' (kebab-case). Si el caller pasa otra variante,
  // devolvemos un error explicito.
  var handler = registry.get('sendEmail');
  if (!handler) {
    return res.status(500).json({ error: 'handler_not_found',
                                  message: 'Handler "sendEmail" no registrado' });
  }

  // Validacion interna: el umbral aqui es 500 KB.
  if (file && file.size > 500 * 1024) {
    return res.status(413).json({ error: 'attachment_too_large_v2',
                                  message: 'Adjunto excede 500 KB' });
  }
  if (!file) {
    return res.status(200).json({ ok: true, mode: 'no_attachment' });
  }
  if (file.size <= 500 * 1024) {
    return res.status(200).json({ ok: true, mode: 'with_attachment', size: file.size });
  }
  return res.status(413).json({ error: 'attachment_too_large_v1',
                                message: 'Adjunto excede 1 MB' });
});

module.exports = router;
