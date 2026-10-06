// Load + form actions para el modulo principal. Trampa: la
// action `?/foo` que no existe no se maneja explicitamente;
// SvelteKit devuelve 404 silencioso.
import type { Actions, PageServerLoad } from './$types';
import { fail } from '@sveltejs/kit';
import { getTareas, addTarea, removeTarea } from '$lib/server/db';
import { z } from 'zod';

const schema = z.object({
  titulo: z.string().min(1).max(120)
});

export const load: PageServerLoad = async ({ parent }) => {
  const { tareas: all, user } = await parent();
  // Filtra a las del usuario actual.
  return { tareas: all.filter((t) => t.usuarioId === user.id), user };
};

export const actions: Actions = {
  create: async ({ request }) => {
    const data = await request.formData();
    const parsed = schema.safeParse({ titulo: data.get('titulo') });
    if (!parsed.success) {
      return fail(400, { error: 'validation_failed', issues: parsed.error.issues });
    }
    const nueva = addTarea({
      titulo: parsed.data.titulo,
      completada: false,
      premium: false,
      usuarioId: 'u-1'
    });
    return { ok: true, tarea: nueva };
  },
  delete: async ({ request }) => {
    const data = await request.formData();
    const id = String(data.get('id') || '');
    if (!id) return fail(400, { error: 'id_required' });
    const ok = removeTarea(id);
    if (!ok) return fail(404, { error: 'not_found' });
    return { ok: true };
  }
};
