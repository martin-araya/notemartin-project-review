// server/api/profile.get.ts
// GET /api/profile?id=... Devuelve 404 si no existe.
import { getProfile } from '../utils/db';

export default defineEventHandler((event) => {
  const query = getQuery(event);
  const id = query.id ? String(query.id) : '';
  const p = getProfile(id);
  if (!p) {
    setResponseStatus(event, 404);
    return { error: 'not_found' };
  }
  return p;
});
