// Module file
// Interface State del feature store. La entidad usa `id` por
// defecto en entity adapter; las entidades con clave distinta
// (e.g. `comentarioId`) requieren selectId custom.
export interface Item {
  id: string;
  nombre: string;
  estado: 'pendiente' | 'aprobado' | 'rechazado';
  premium?: boolean;
  usuarioId?: string;
  monto?: number;
}

export interface SolicitudesState extends Array<Item> {}

export const SOLICITUDES_FEATURE_KEY = 'solicitudes';
