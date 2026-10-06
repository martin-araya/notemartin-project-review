import type { FastifyInstance } from 'fastify';
import type { Listing, ListingFilters, PaginatedListings, ListingStatus } from '@fx-mono/shared';
import { listingFiltersSchema } from '../schemas.js';

// In-memory listing store. Trampa de paquete #6: aplicamos filtros en
// memoria en vez de en SQL (N+1 si hay 10k items).
const listings: Listing[] = [
  mkListing('L1', 'Casa en el centro', 250000, 'active'),
  mkListing('L2', 'Departamento moderno', 180000, 'active'),
  mkListing('L3', 'Terreno rural', 50000, 'draft'),
  mkListing('L4', 'Local comercial', 320000, 'sold'),
  mkListing('L5', 'Oficina céntrica', 1200, 'archived'),
];

function mkListing(id: string, title: string, price: number, status: ListingStatus): Listing {
  const now = new Date().toISOString();
  return {
    id, title, description: `Desc ${title}`,
    price, currency: 'USD', status,
    ownerId: 'user-admin@example.com',
    createdAt: now, updatedAt: now,
  };
}

function applyFilters(all: Listing[], f: ListingFilters): Listing[] {
  // Trampa de paquete #6: filtros en memoria, no en SQL.
  return all.filter((l) => {
    if (f.status && l.status !== f.status) return false;
    if (typeof f.minPrice === 'number' && l.price < f.minPrice) return false;
    if (typeof f.maxPrice === 'number' && l.price > f.maxPrice) return false;
    if (f.query && !l.title.toLowerCase().includes(f.query.toLowerCase())) return false;
    if (f.ownerId && l.ownerId !== f.ownerId) return false;
    return true;
  });
}

export default async function listingsRoutes(app: FastifyInstance) {
  app.get('/', async (request, reply) => {
    const parse = listingFiltersSchema.safeParse(request.query ?? {});
    if (!parse.success) {
      return reply.code(400).send({ error: 'invalid_filters', issues: parse.error.issues });
    }
    const filters = parse.data as ListingFilters;
    const filtered = applyFilters(listings, filters);
    const page = filters.page ?? 1;
    const pageSize = filters.pageSize ?? 20;
    const start = (page - 1) * pageSize;
    const items = filtered.slice(start, start + pageSize);
    const out: PaginatedListings = {
      items, total: filtered.length, page, pageSize,
    };
    return reply.code(200).send(out);
  });

  app.get<{ Params: { id: string } }>('/:id', async (request, reply) => {
    const found = listings.find((l) => l.id === request.params.id);
    if (!found) return reply.code(404).send({ error: 'not_found' });
    return reply.code(200).send(found);
  });
}
