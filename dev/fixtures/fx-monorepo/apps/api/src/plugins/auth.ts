import type { FastifyInstance, FastifyRequest } from 'fastify';

// Plugin de autenticacion. Verifica el header Authorization.
// No valida firma (es solo un shim del fixture); el token es un string
// cualquiera. En produccion se validaria contra un IdP.
//
// El plugin usa ``fastify-plugin`` para evitar el encapsulamiento de
// Fastify y que el hook aplique a todas las rutas registradas
// posteriormente.
import fp from 'fastify-plugin';

export const authPlugin = fp(async function authPlugin(app: FastifyInstance) {
  app.decorateRequest('userId', null);

  app.addHook('onRequest', async (request: FastifyRequest) => {
    const header = request.headers.authorization;
    if (header && header.startsWith('Bearer ')) {
      const token = header.slice('Bearer '.length).trim();
      if (token.length > 0) {
        // Mapeamos el token al userId deterministico. En produccion,
        // esto se validaria contra un JWT firmado.
        (request as any).userId = `user-${token.slice(0, 6)}`;
      }
    }
  });
});

declare module 'fastify' {
  interface FastifyRequest {
    userId?: string | null;
  }
}
