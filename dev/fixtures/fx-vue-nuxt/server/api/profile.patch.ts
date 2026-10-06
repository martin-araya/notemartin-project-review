// server/api/profile.patch.ts
// PATCH /api/profile. Valida el email con Zod.
import { z } from 'zod';
import { getProfile, updateProfile } from '../utils/db';

const schema = z.object({
  id: z.string().min(1),
  nombre: z.string().min(1).optional(),
  email: z.string().email('email invalido').optional(),
  role: z.enum(['user', 'premium']).optional(),
  premium: z.boolean().optional()
});

export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const result = schema.safeParse(body);
  if (!result.success) {
    setResponseStatus(event, 400);
    return { error: 'validation_failed', issues: result.error.issues };
  }
  if (!getProfile(result.data.id)) {
    setResponseStatus(event, 404);
    return { error: 'not_found' };
  }
  const updated = updateProfile(result.data.id, result.data);
  return updated;
});
