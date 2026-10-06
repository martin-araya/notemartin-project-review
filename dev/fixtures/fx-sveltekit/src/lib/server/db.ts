// src/lib/server/db.ts
// Store en memoria con seed inicial. La funcion de inflado solo se
// invoca desde los tests para inflar el array; no la usa la app.
import type { Tarea, Etiqueta, Share } from './types';

const tareas: Tarea[] = [
  { id: 't-001', titulo: 'Comprar pan',  completada: false, premium: false, usuarioId: 'u-1' },
  { id: 't-002', titulo: 'Llamar al medico', completada: true,  premium: false, usuarioId: 'u-1' },
  { id: 't-003', titulo: 'Revisar email',   completada: false, premium: false, usuarioId: 'u-2' },
  { id: 't-004', titulo: 'Suscripcion premium', completada: false, premium: true, usuarioId: 'u-1' },
  { id: 't-005', titulo: 'Pagar factura',  completada: false, premium: false, usuarioId: 'u-1' },
  { id: 't-006', titulo: 'Comprar regalo',  completada: false, premium: true,  usuarioId: 'u-2' },
  { id: 't-007', titulo: 'Hacer ejercicio', completada: true,  premium: false, usuarioId: 'u-1' },
  { id: 't-008', titulo: 'Leer libro',     completada: false, premium: false, usuarioId: 'u-1' },
  { id: 't-009', titulo: 'Ver pelicula',   completada: false, premium: false, usuarioId: 'u-3' },
  { id: 't-010', titulo: 'Reservar hotel premium', completada: false, premium: true, usuarioId: 'u-1' },
  { id: 't-011', titulo: 'Correr 5k',      completada: false, premium: false, usuarioId: 'u-1' },
  { id: 't-012', titulo: 'Comprar libros',  completada: false, premium: false, usuarioId: 'u-2' }
];

const etiquetas: Etiqueta[] = [
  { id: 'e-001', nombre: 'urgente',  color: '#dc2626' },
  { id: 'e-002', nombre: 'hogar',    color: '#16a34a' },
  { id: 'e-003', nombre: 'trabajo',  color: '#2563eb' },
  { id: 'e-004', nombre: 'personal', color: '#9333ea' },
  { id: 'e-005', nombre: 'salud',    color: '#facc15' }
];

const shares: Share[] = [
  { id: 's-001', tareaId: 't-001', email: 'ana@example.com', createdAt: '2026-10-31' },
  { id: 's-002', tareaId: 't-002', email: 'luis@example.com', createdAt: '2026-10-30' }
];

export function getTareas(usuarioId?: string): Tarea[] {
  if (!usuarioId) return tareas.slice();
  return tareas.filter((t) => t.usuarioId === usuarioId);
}

export function getTareaById(id: string): Tarea | undefined {
  return tareas.find((t) => t.id === id);
}

export function addTarea(t: Omit<Tarea, 'id'>): Tarea {
  const id = 't-' + String(tareas.length + 1).padStart(3, '0');
  const nueva: Tarea = { id, ...t };
  tareas.push(nueva);
  return nueva;
}

export function removeTarea(id: string): boolean {
  const idx = tareas.findIndex((t) => t.id === id);
  if (idx === -1) return false;
  tareas.splice(idx, 1);
  return true;
}

export function getEtiquetas(): Etiqueta[] {
  return etiquetas.slice();
}

export function getEtiquetaById(id: string): Etiqueta | undefined {
  return etiquetas.find((e) => e.id === id);
}

export function getShares(): Share[] {
  return shares.slice();
}

export function addShare(s: Omit<Share, 'id' | 'createdAt'>): Share {
  const id = 's-' + String(shares.length + 1).padStart(3, '0');
  const nuevo: Share = { id, createdAt: new Date().toISOString().slice(0, 10), ...s };
  shares.push(nuevo);
  return nuevo;
}

// Dead code: solo lo invocan los tests para inflar el array.
export function seedTareasExtra(count: number): void {
  for (let i = 0; i < count; i++) {
    tareas.push({
      id: 'x-' + String(i).padStart(3, '0'),
      titulo: 'Tarea extra ' + i,
      completada: false,
      premium: false,
      usuarioId: 'u-test'
    });
  }
}
