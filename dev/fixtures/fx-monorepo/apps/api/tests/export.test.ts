import { describe, it, expect } from 'vitest';
import Fastify, { type FastifyInstance } from 'fastify';
import exportRoutes from '../src/routes/export.js';
import { authPlugin } from '../src/plugins/auth.js';

async function makeApp(): Promise<FastifyInstance> {
  const app = Fastify();
  await app.register(authPlugin);
  await app.register(exportRoutes, { prefix: '/api/export' });
  return app;
}

describe('export route', () => {
  it('retorna 401 sin Authorization header', async () => {
    const app = await makeApp();
    const res = await app.inject({
      method: 'POST',
      url: '/api/export',
      payload: { filters: { status: 'active' }, format: 'csv' },
    });
    expect(res.statusCode).toBe(401);
    await app.close();
  });

  it('retorna 202 con Authorization y payload valido', async () => {
    const app = await makeApp();
    const res = await app.inject({
      method: 'POST',
      url: '/api/export',
      headers: { authorization: 'Bearer test-token' },
      payload: { filters: { status: 'active' }, format: 'csv' },
    });
    expect(res.statusCode).toBe(202);
    const body = res.json();
    expect(body.format).toBe('csv');
    expect(body.url).toContain('report-');
    await app.close();
  });

  it('retorna 400 con format invalido', async () => {
    const app = await makeApp();
    const res = await app.inject({
      method: 'POST',
      url: '/api/export',
      headers: { authorization: 'Bearer test-token' },
      payload: { filters: { status: 'active' }, format: 'xml' },
    });
    expect(res.statusCode).toBe(400);
    await app.close();
  });
});
