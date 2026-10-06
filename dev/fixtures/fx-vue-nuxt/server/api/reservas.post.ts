// POST que valida el body con Zod y crea un nuevo item.
import { z } from 'zod';
import { addReserva } from '../utils/db';

const schema = z.object({
  usuarioId: z.string().min(1),
  fecha: z.string().refine((v) => !Number.isNaN(Date.parse(v)), {
    message: 'fecha debe ser un string ISO valido'
  }),
  personas: z.number().int().min(1).max(20),
  sala: z.enum(['A', 'B', 'C'])
});

export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const result = schema.safeParse(body);
  if (!result.success) {
    setResponseStatus(event, 400);
    return { error: 'validation_failed', issues: result.error.issues };
  }
  const nueva = addReserva(result.data);
  setResponseStatus(event, 201);
  return nueva;
});
