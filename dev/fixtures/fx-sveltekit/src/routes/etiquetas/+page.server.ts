import type { PageServerLoad } from './$types';
import { getEtiquetas, getTareas } from '$lib/server/db';

export const load: PageServerLoad = async ({ parent }) => {
  const { user } = await parent();
  return {
    etiquetas: getEtiquetas(),
    tareas: getTareas(user.id)
  };
};
