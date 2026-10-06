// server/index.js
// Bootstrap de la aplicacion Express: sirve /public y monta /api/*.
// El plugin jquery.colorbox se carga despues de jQuery pero antes
// de app.js; si un bundler ingenuo los reordena, la llamada
// $().colorbox() falla con un mensaje visible en la UI.
var express = require('express');
var path = require('path');

var registry = require('./plugins/registry');
var searchRouter = require('./routes/search');
var contactRouter = require('./routes/contact');
var galleryModule = require('./routes/gallery');

var app = express();

app.use(express.urlencoded({ extended: false }));
app.use(express.json());

app.use(express.static(path.join(__dirname, '..', 'public')));

app.use('/api/search', searchRouter);
app.use('/api/contact', contactRouter);
app.use('/api/gallery', galleryModule.router);

app.get('/api/health', function (req, res) {
  registry.init();
  res.json({ ok: true, handlers: registry.keys() });
});

if (require.main === module) {
  var port = process.env.PORT || 3000;
  app.listen(port, function () {
    console.log('fx-vanilla-js-legacy listening on ' + port);
  });
}

module.exports = app;
