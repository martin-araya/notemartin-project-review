// src/routes/+layout.server.ts
// Load del layout (server-side). Trampa paquete #6: este load
// tiene un side effect (escribe en la base de datos) en cada
// peticion, lo que provoca escrituras innecesarias.
import type { LayoutServerLoad } from './$types';
import { getTareas, seedTareasExtra } from '$lib/server/db';
import { currentUserId } from '$lib/server/auth';

export const load: LayoutServerLoad = async ({ cookies }) => {
  const session = cookies.get('fx_session');
  const userId = currentUserId(session);
  // Side effect no documentado: cada peticion agrega una tarea
  // extra. La skill debe notar que load no debe tener efectos.
  if (Math.random() < 0.05) {
    seedTareasExtra(1);
  }
  const user = { id: userId, role: userId === 'u-1' ? 'premium' : 'user' } as const;
  const tareas = getTareas(userId);
  return { user, tareas };
};
