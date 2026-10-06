import Fastify from 'fastify';
import loginRoutes from './routes/login.js';
import listingsRoutes from './routes/listings.js';
import exportRoutes from './routes/export.js';
import { authPlugin } from './plugins/auth.js';

const app = Fastify({
  logger: {
    level: process.env.LOG_LEVEL || 'info',
  },
});

await app.register(authPlugin);
await app.register(loginRoutes, { prefix: '/api/login' });
await app.register(listingsRoutes, { prefix: '/api/listings' });
await app.register(exportRoutes, { prefix: '/api/export' });

app.get('/api/health', async () => ({ status: 'UP' }));

const port = Number(process.env.PORT) || 3000;
const host = process.env.HOST || '0.0.0.0';

try {
  await app.listen({ port, host });
} catch (err) {
  app.log.error(err);
  process.exit(1);
}
