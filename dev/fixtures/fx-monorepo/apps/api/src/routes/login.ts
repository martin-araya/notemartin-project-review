import type { FastifyInstance } from 'fastify';
import { z } from 'zod';
import type { LoginRequest, LoginResponse } from '@fx-mono/shared';
import { loginRequestSchema } from '../schemas.js';

export default async function loginRoutes(app: FastifyInstance) {
  // In-memory user store. En produccion esto seria una BD.
  const users: Record<string, { password: string; name: string }> = {
    'admin@example.com': { password: 'admin123', name: 'Admin' },
    'agent@example.com': { password: 'agent123', name: 'Agent' },
  };

  app.post('/', async (request, reply) => {
    const parse = loginRequestSchema.safeParse(request.body);
    if (!parse.success) {
      return reply.code(400).send({ error: 'invalid_payload', issues: parse.error.issues });
    }
    const { email, password } = parse.data as LoginRequest;
    const u = users[email];
    if (!u || u.password !== password) {
      return reply.code(401).send({ error: 'invalid_credentials' });
    }
    const role = email.startsWith('admin') ? 'admin' : email.startsWith('agent') ? 'agent' : 'viewer';
    const token = `tok-${email}-${Date.now()}`;
    const body: LoginResponse = {
      token,
      user: {
        id: `user-${email}`,
        email,
        displayName: u.name,
        role,
        createdAt: new Date().toISOString(),
      },
      expiresAt: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
    };
    return reply.code(200).send(body);
  });

  app.get('/me', async (request, reply) => {
    if (!request.userId) {
      return reply.code(401).send({ error: 'unauthorized' });
    }
    return reply.code(200).send({ userId: request.userId });
  });
}
