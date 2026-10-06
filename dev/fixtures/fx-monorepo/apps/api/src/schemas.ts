import { z } from 'zod';

// Schemas de zod reutilizables en apps/api. Usamos ``z.coerce.number()`` para
// que los query params (que Fastify entrega como string) se conviertan
// automaticamente.

export const loginRequestSchema = z.object({
  email: z.string(),
  password: z.string().min(1),
});

export const listingFiltersSchema = z.object({
  status: z.enum(['draft', 'active', 'sold', 'archived']).optional(),
  minPrice: z.coerce.number().nonnegative().optional(),
  maxPrice: z.coerce.number().nonnegative().optional(),
  query: z.string().optional(),
  ownerId: z.string().optional(),
  page: z.coerce.number().int().positive().default(1),
  pageSize: z.coerce.number().int().positive().max(100).default(20),
});

export const exportRequestSchema = z.object({
  filters: listingFiltersSchema,
  format: z.enum(['csv', 'json']),
});
