// Functional HTTP interceptor (trampa del ecosistema #3). En un proyecto
// Angular real: import { HttpInterceptorFn } from '@angular/common/http';
// Aqui definimos el contrato como type.

export type HttpInterceptorFn = (
  req: unknown,
  next: (req: unknown) => unknown
) => unknown;

/**
 * Trampa de paquete #1: este interceptor agrega ``Authorization: Bearer <token>``
 * SIEMPRE, incluso si el token es vacio. El backend recibe un token basura
 * (o vacio) y responde 401 si el endpoint requiere auth.
 */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // En el fixture simulamos: cualquier token (incluso vacio) genera el header.
  const token = readToken();
  const headers = (req as any).headers ?? {};
  const newReq = {
    ...(req as any),
    headers: { ...headers, Authorization: `Bearer ${token}` },
  };
  return next(newReq);
};

function readToken(): string {
  // Trampa de paquete #1: no validamos que el token no este vacio.
  return (globalThis as any).__FX_TOKEN__ ?? '';
}

/**
 * Segundo interceptor funcional (logging) registrado en
 * ``provideHttpClient(withInterceptors([authInterceptor, loggingInterceptor]))``.
 */
export const loggingInterceptor: HttpInterceptorFn = (req, next) => {
  // Log trivial; en produccion serializaria a un sink.
  const r = req as any;
  if (r && r.method) {
    // eslint-disable-next-line no-console
    console.log(`[http] ${r.method} ${r.url ?? ''}`);
  }
  return next(req);
};
