import type { PageServerLoad } from './$types';
import { getTareaById } from '$lib/server/db';
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ params }) => {
  const tarea = getTareaById(params.id);
  if (!tarea) throw error(404, 'no encontrado');
  return { tarea };
};
