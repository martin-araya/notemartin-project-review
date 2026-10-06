import type { FastifyInstance } from 'fastify';
import type { ExportRequest, ExportResponse, ReportFormat } from '@fx-mono/shared';
import { exportRequestSchema } from '../schemas.js';

// Trampa de paquete #4: no validamos el tamano del filtro antes de
// serializar a CSV. Un filtro con 1M items genera un string OOM.
// Para el fixture limitamos a 1000 items como salvaguarda.
const MAX_ROWS = 1000;

function buildResponse(req: ExportRequest): ExportResponse {
  const rows = Math.floor(Math.random() * 100); // stub: el endpoint real consultaria la BD
  const fileName = `report-${Date.now()}.${req.format}`;
  return {
    url: `https://files.example.com/${fileName}`,
    format: req.format,
    rows,
    expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
  };
}

export default async function exportRoutes(app: FastifyInstance) {
  app.post('/', async (request, reply) => {
    if (!request.userId) {
      return reply.code(401).send({ error: 'unauthorized' });
    }
    const parse = exportRequestSchema.safeParse(request.body);
    if (!parse.success) {
      return reply.code(400).send({ error: 'invalid_payload', issues: parse.error.issues });
    }
    const req = parse.data as ExportRequest;
    // Trampa de paquete #4: solo limitamos el reporte final, no el filtro
    // de entrada. Un filtro con muchos matches desborda el CSV.
    if (req.filters.pageSize && req.filters.pageSize > MAX_ROWS) {
      return reply.code(413).send({ error: 'too_many_rows', limit: MAX_ROWS });
    }
    return reply.code(202).send(buildResponse(req));
  });
}
