// tests/share.test.ts
// Tests del feature de publicacion + cross-store.
import { describe, it, expect } from 'vitest';
import { addShare, getShares, getTareas } from '../src/lib/server/db';

describe('FEAT-003 publicacion (shares)', () => {
  it('R-01 el seed tiene 2 shares', () => {
    const all = getShares();
    expect(all.length).toBe(2);
  });

  it('R-01 addShare agrega con id incremental y createdAt', () => {
    const before = getShares().length;
    const nuevo = addShare({ tareaId: 't-001', email: 'nuevo@example.com' });
    expect(nuevo.id).toMatch(/^s-\d+$/);
    expect(nuevo.createdAt).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    expect(getShares().length).toBe(before + 1);
  });

  it('R-05 addShare con tareaId inexistente se permite en server pero falla en cross-store', () => {
    // El addShare del server no valida el target; lo hace el caller.
    // La trampa es que el cross-store borra el item aunque el id
    // no exista en el modulo principal.
    const all = getTareas();
    const before = all.length;
    addShare({ tareaId: 'no-existe', email: 'x@y.z' });
    const after = getTareas();
    expect(after.length).toBe(before);
  });

  it('R-03 el share no muta la lista de tareas (responsabilidad del cross-store)', () => {
    const before = getTareas().length;
    addShare({ tareaId: 't-002', email: 'a@b.c' });
    const after = getTareas().length;
    expect(after).toBe(before);
  });
});
