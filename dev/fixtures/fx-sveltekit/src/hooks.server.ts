// src/hooks.server.ts
// Hook global del servidor. Trampa: el handle anade un header
// `x-fx-auth: always` pero nunca lee `event.locals.user` ni lo
// comprueba, asi que cualquier sesion queda como autenticada.
import type { Handle } from '@sveltejs/kit';
import { currentUserId } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
  const cookie = event.cookies.get('fx_session');
  const userId = currentUserId(cookie);
  // El bug esta aqui: asignamos locals.user pero no lo
  // validamos en ningun endpoint. La skill debe notar que
  // cualquier peticion parece "autenticada" porque el handle
  // nunca falla.
  event.locals.user = { id: userId, role: 'user' };

  const response = await resolve(event);
  response.headers.set('x-fx-auth', 'always');
  return response;
};
