/**
 * @jest-environment node
 */
// tests/api.test.js
// Tests de integracion con supertest contra la app Express.
var request = require('supertest');
var app = require('../server/index');

describe('GET /api/health', function () {
  it('devuelve ok y lista los handlers registrados', function (done) {
    request(app)
      .get('/api/health')
      .expect(200)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.ok).toBe(true);
        expect(Array.isArray(res.body.handlers)).toBe(true);
        expect(res.body.handlers).toContain('send-email');
        expect(res.body.handlers).toContain('search');
        expect(res.body.handlers).toContain('list-gallery');
        done();
      });
  });
});

describe('GET /api/search', function () {
  it('R-02 success_empty cuando no hay termino', function (done) {
    request(app)
      .get('/api/search?q=xyzzy')
      .expect(200)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.mode).toBe('full');
        expect(res.body.count).toBe(0);
        expect(res.body.html).toBe('');
        done();
      });
  });

  it('R-01 success_results con termino de 3+ caracteres', function (done) {
    request(app)
      .get('/api/search?q=camiseta')
      .expect(200)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.mode).toBe('full');
        expect(res.body.count).toBeGreaterThan(0);
        expect(res.body.html).toMatch(/<li/);
        done();
      });
  });

  it('R-03 success_partial con termino corto (sin escape)', function (done) {
    request(app)
      .get('/api/search?q=ca')
      .expect(200)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.mode).toBe('partial');
        expect(res.body.html).toMatch(/<li/);
        // Trampa paquete #2: la rama "partial" NO escapa; el HTML
        // contiene nombres de producto sin pasar por escapeHtml.
        expect(res.body.html).toMatch(/Camiseta/);
        done();
      });
  });

  it('R-04 error_xss_attempt cuando q tiene < o >', function (done) {
    request(app)
      .get('/api/search?q=<script>')
      .expect(400)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.error).toBe('q_invalid');
        done();
      });
  });

  it('R-05 error_validation_q_missing sin parametro q', function (done) {
    request(app)
      .get('/api/search')
      .expect(400)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.error).toBe('q_missing');
        done();
      });
  });

  it('R-07 success_hidden_premium incluye clase is-premium', function (done) {
    request(app)
      .get('/api/search?q=chaqueta')
      .expect(200)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.html).toMatch(/is-premium/);
        done();
      });
  });
});

describe('GET /api/gallery', function () {
  it('lista todas las imagenes sin filtro', function (done) {
    request(app)
      .get('/api/gallery')
      .expect(200)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.count).toBe(12);
        done();
      });
  });

  it('R-02 success_filter_category filtra por categoria', function (done) {
    request(app)
      .get('/api/gallery?category=premium')
      .expect(200)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.count).toBe(3);
        expect(res.body.items[0].category).toBe('premium');
        done();
      });
  });
});

describe('POST /api/contact', function () {
  it('R-03 error_invalid_email sin email valido', function (done) {
    request(app)
      .post('/api/contact')
      .type('form')
      .send({ email: 'no-es-email', message: 'hola' })
      .expect(400)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.error).toBe('invalid_email');
        done();
      });
  });

  it('R-07 error_handler_not_found por case mismatch en el registry', function (done) {
    request(app)
      .post('/api/contact')
      .type('form')
      .send({ email: 'user@example.com', message: 'hola' })
      .expect(500)
      .end(function (err, res) {
        if (err) return done(err);
        expect(res.body.error).toBe('handler_not_found');
        expect(res.body.message).toMatch(/sendEmail/);
        done();
      });
  });
});
