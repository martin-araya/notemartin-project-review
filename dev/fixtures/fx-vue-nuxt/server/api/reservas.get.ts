// GET de la coleccion principal con filtro opcional por usuarioId.
import { getReservas } from '../utils/db';

export default defineEventHandler((event) => {
  const query = getQuery(event);
  const usuarioId = query.usuarioId ? String(query.usuarioId) : undefined;
  return getReservas(usuarioId);
});
