// Form action con validacion Zod. Trampa: la accion rate-limit
// (5 publicaciones por minuto) NO esta implementada; cualquier
// POST pasa. La skill debe notar que el rate-limit es
// declarativo pero no real.
import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import { getTareas, addShare } from '$lib/server/db';
import { z } from 'zod';

const schema = z.object({
  tareaId: z.string().min(1),
  email: z.string().email('email invalido')
});

export const load: PageServerLoad = async () => {
  return { tareas: getTareas() };
};

export const actions: Actions = {
  compartir: async ({ request }) => {
    const data = await request.formData();
    const parsed = schema.safeParse({
      tareaId: data.get('tareaId'),
      email: data.get('email')
    });
    if (!parsed.success) {
      return fail(400, { error: 'validation_failed', issues: parsed.error.issues });
    }
    const target = getTareas().find((t) => t.id === parsed.data.tareaId);
    if (!target) return fail(404, { error: 'target_not_found' });
    addShare({ tareaId: parsed.data.tareaId, email: parsed.data.email });
    throw redirect(303, '/tareas');
  }
};
