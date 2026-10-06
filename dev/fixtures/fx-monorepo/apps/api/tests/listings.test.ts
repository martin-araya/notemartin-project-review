import { describe, it, expect } from 'vitest';
import Fastify, { type FastifyInstance } from 'fastify';
import listingsRoutes from '../src/routes/listings.js';

async function makeApp(): Promise<FastifyInstance> {
  const app = Fastify();
  await app.register(listingsRoutes, { prefix: '/api/listings' });
  return app;
}

describe('listings route', () => {
  it('retorna todos los listings activos sin filtros', async () => {
    const app = await makeApp();
    const res = await app.inject({ method: 'GET', url: '/api/listings' });
    expect(res.statusCode).toBe(200);
    const body = res.json();
    expect(body.items).toHaveLength(5);
    expect(body.total).toBe(5);
    await app.close();
  });

  it('filtra por status=active', async () => {
    const app = await makeApp();
    const res = await app.inject({ method: 'GET', url: '/api/listings?status=active' });
    const body = res.json();
    expect(body.items).toHaveLength(2);
    expect(body.items.every((l: any) => l.status === 'active')).toBe(true);
    await app.close();
  });

  it('filtra por rango de precio (minPrice/maxPrice)', async () => {
    const app = await makeApp();
    const res = await app.inject({ method: 'GET', url: '/api/listings?minPrice=100000&maxPrice=300000' });
    const body = res.json();
    expect(body.items.length).toBeGreaterThan(0);
    expect(body.items.every((l: any) => l.price >= 100000 && l.price <= 300000)).toBe(true);
    await app.close();
  });

  it('retorna 404 para id desconocido', async () => {
    const app = await makeApp();
    const res = await app.inject({ method: 'GET', url: '/api/listings/NOPE' });
    expect(res.statusCode).toBe(404);
    await app.close();
  });
});
