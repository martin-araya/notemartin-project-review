// tests/tasks.test.ts
// Tests del feature principal: store + load + actions.
import { describe, it, expect } from 'vitest';
import {
  getTareas,
  getTareaById,
  addTarea,
  removeTarea
} from '../src/lib/server/db';

describe('FEAT-001 tareas (store y load)', () => {
  it('R-01 el store devuelve 12 items en el seed', () => {
    const all = getTareas();
    expect(all.length).toBe(12);
  });

  it('R-01 el filtro por usuarioId reduce el listado', () => {
    const u1 = getTareas('u-1');
    expect(u1.length).toBeGreaterThan(0);
    expect(u1.every((t) => t.usuarioId === 'u-1')).toBe(true);
  });

  it('R-02 addTarea agrega con id incremental', () => {
    const before = getTareas().length;
    const nueva = addTarea({ titulo: 'Test', completada: false, premium: false, usuarioId: 'u-1' });
    expect(nueva.id).toMatch(/^t-\d+$/);
    expect(getTareas().length).toBe(before + 1);
  });

  it('R-03 removeTarea devuelve true cuando existe, false cuando no', () => {
    const nueva = addTarea({ titulo: 'Borrable', completada: false, premium: false, usuarioId: 'u-1' });
    expect(removeTarea(nueva.id)).toBe(true);
    expect(removeTarea('no-existe')).toBe(false);
  });

  it('R-07 getTareaById devuelve tareas premium y no premium', () => {
    const t = getTareaById('t-004');
    expect(t).toBeDefined();
    expect(t!.premium).toBe(true);
    const t2 = getTareaById('t-001');
    expect(t2!.premium).toBe(false);
  });
});
