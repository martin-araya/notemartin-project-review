// server/utils/db.ts
// Store en memoria con seed inicial. La funcion de inflado solo
// se invoca desde los tests; no la usa la aplicacion.
import type { Reserva, Profile, Notificacion } from '../../types';

const reservas: Reserva[] = [
  { id: 'r-001', usuarioId: 'u-1', fecha: '2026-11-01T19:00:00.000Z', personas: 2, sala: 'A' },
  { id: 'r-002', usuarioId: 'u-1', fecha: '2026-11-05T20:00:00.000Z', personas: 4, sala: 'B' },
  { id: 'r-003', usuarioId: 'u-2', fecha: '2026-11-08T18:30:00.000Z', personas: 2, sala: 'A' },
  { id: 'r-004', usuarioId: 'u-1', fecha: '2026-11-10T21:00:00.000Z', personas: 6, sala: 'C', premium: true },
  { id: 'r-005', usuarioId: 'u-3', fecha: '2026-11-12T19:30:00.000Z', personas: 3, sala: 'B' },
  { id: 'r-006', usuarioId: 'u-1', fecha: '2026-11-15T20:30:00.000Z', personas: 2, sala: 'A' },
  { id: 'r-007', usuarioId: 'u-2', fecha: '2026-11-18T19:00:00.000Z', personas: 8, sala: 'C', premium: true },
  { id: 'r-008', usuarioId: 'u-1', fecha: '2026-11-20T21:00:00.000Z', personas: 4, sala: 'B' },
  { id: 'r-009', usuarioId: 'u-3', fecha: '2026-11-22T19:30:00.000Z', personas: 2, sala: 'A' },
  { id: 'r-010', usuarioId: 'u-1', fecha: '2026-11-25T20:00:00.000Z', personas: 5, sala: 'B' },
  { id: 'r-011', usuarioId: 'u-2', fecha: '2026-11-28T19:00:00.000Z', personas: 3, sala: 'A' },
  { id: 'r-012', usuarioId: 'u-1', fecha: '2026-12-01T20:30:00.000Z', personas: 4, sala: 'C' }
];

const profiles: Profile[] = [
  { id: 'u-1', nombre: 'Ana Garcia',  email: 'ana@example.com',  role: 'premium', premium: true  },
  { id: 'u-2', nombre: 'Luis Perez',  email: 'luis@example.com', role: 'user',    premium: false },
  { id: 'u-3', nombre: 'Marta Lopez', email: 'marta@example.com', role: 'user',    premium: false }
];

const notificaciones: Notificacion[] = [
  { id: 'n-001', usuarioId: 'u-1', mensaje: 'Tu item r-001 es manana',  leida: false, fecha: '2026-10-31' },
  { id: 'n-002', usuarioId: 'u-1', mensaje: 'Promo premium disponible', leida: false, fecha: '2026-10-30' },
  { id: 'n-003', usuarioId: 'u-2', mensaje: 'Confirmacion',            leida: true,  fecha: '2026-10-29' }
];

export function getReservas(usuarioId?: string): Reserva[] {
  if (!usuarioId) return reservas.slice();
  return reservas.filter((r) => r.usuarioId === usuarioId);
}

export function getReservaById(id: string): Reserva | undefined {
  return reservas.find((r) => r.id === id);
}

export function addReserva(r: Omit<Reserva, 'id'>): Reserva {
  const id = 'r-' + String(reservas.length + 1).padStart(3, '0');
  const nueva: Reserva = { id, ...r };
  reservas.push(nueva);
  return nueva;
}

export function removeReserva(id: string): boolean {
  const idx = reservas.findIndex((r) => r.id === id);
  if (idx === -1) return false;
  reservas.splice(idx, 1);
  return true;
}

export function getProfile(id: string): Profile | undefined {
  return profiles.find((p) => p.id === id);
}

export function updateProfile(id: string, patch: Partial<Profile>): Profile | undefined {
  const idx = profiles.findIndex((p) => p.id === id);
  if (idx === -1) return undefined;
  profiles[idx] = { ...profiles[idx], ...patch };
  return profiles[idx];
}

export function getNotificaciones(usuarioId?: string): Notificacion[] {
  if (!usuarioId) return notificaciones.slice();
  return notificaciones.filter((n) => n.usuarioId === usuarioId);
}

export function markNotificacionLeida(id: string): Notificacion | undefined {
  const idx = notificaciones.findIndex((n) => n.id === id);
  if (idx === -1) return undefined;
  notificaciones[idx] = { ...notificaciones[idx], leida: true };
  return notificaciones[idx];
}

// Dead code: solo lo invocan los tests para inflar el array.
export function seedExtra(count: number): void {
  for (let i = 0; i < count; i++) {
    reservas.push({
      id: 'x-' + String(i).padStart(3, '0'),
      usuarioId: 'u-test',
      fecha: '2026-12-31T20:00:00.000Z',
      personas: 1,
      sala: 'X'
    });
  }
}
