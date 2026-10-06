// DELETE /api/... No valida que el caller sea dueno: la accion es
// destructiva a discrecion del cliente.
import { removeReserva } from '../../utils/db';

export default defineEventHandler((event) => {
  const id = String(getRouterParam(event, 'id') || '');
  if (!id) {
    setResponseStatus(event, 400);
    return { error: 'id_required' };
  }
  const ok = removeReserva(id);
  if (!ok) {
    setResponseStatus(event, 404);
    return { error: 'not_found' };
  }
  return { ok: true };
});
