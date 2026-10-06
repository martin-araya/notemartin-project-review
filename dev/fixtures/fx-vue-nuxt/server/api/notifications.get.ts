// server/api/notifications.get.ts
// GET /api/notifications?usuarioId=...
import { getNotificaciones } from '../utils/db';

export default defineEventHandler((event) => {
  const query = getQuery(event);
  const usuarioId = query.usuarioId ? String(query.usuarioId) : undefined;
  return getNotificaciones(usuarioId);
});
