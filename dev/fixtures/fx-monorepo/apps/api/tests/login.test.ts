import { describe, it, expect } from 'vitest';
import Fastify, { type FastifyInstance } from 'fastify';
import loginRoutes from '../src/routes/login.js';
import { authPlugin } from '../src/plugins/auth.js';

async function makeApp(): Promise<FastifyInstance> {
  const app = Fastify();
  await app.register(authPlugin);
  await app.register(loginRoutes, { prefix: '/api/login' });
  return app;
}

describe('login route', () => {
  it('retorna 200 + token con credenciales validas', async () => {
    const app = await makeApp();
    const res = await app.inject({
      method: 'POST',
      url: '/api/login',
      payload: { email: 'admin@example.com', password: 'admin123' },
    });
    expect(res.statusCode).toBe(200);
    const body = res.json();
    expect(body.token).toBeTruthy();
    expect(body.user.email).toBe('admin@example.com');
    expect(body.user.role).toBe('admin');
    await app.close();
  });

  it('retorna 401 con password incorrecto', async () => {
    const app = await makeApp();
    const res = await app.inject({
      method: 'POST',
      url: '/api/login',
      payload: { email: 'admin@example.com', password: 'wrong' },
    });
    expect(res.statusCode).toBe(401);
    await app.close();
  });

  it('retorna 400 con payload invalido (password vacio)', async () => {
    const app = await makeApp();
    const res = await app.inject({
      method: 'POST',
      url: '/api/login',
      payload: { email: 'admin@example.com', password: '' },
    });
    expect(res.statusCode).toBe(400);
    await app.close();
  });
});
