// tests/tags.test.ts
// Tests del feature de catalogo.
import { describe, it, expect } from 'vitest';
import { getEtiquetas, getEtiquetaById, getTareas } from '../src/lib/server/db';

describe('FEAT-002 catalogo (etiquetas)', () => {
  it('R-01 getEtiquetas devuelve 5 items del seed', () => {
    const all = getEtiquetas();
    expect(all.length).toBe(5);
    expect(all.map((e) => e.nombre)).toContain('urgente');
  });

  it('R-04 getEtiquetaById devuelve undefined para id inexistente', () => {
    expect(getEtiquetaById('no-existe')).toBeUndefined();
  });

  it('R-04 getEtiquetaById devuelve el item correcto', () => {
    const e = getEtiquetaById('e-001');
    expect(e).toBeDefined();
    expect(e!.nombre).toBe('urgente');
    expect(e!.color).toMatch(/^#/);
  });

  it('R-02 el filtro por usuarioId devuelve items consistentes', () => {
    const u1 = getTareas('u-1');
    const u2 = getTareas('u-2');
    expect(u1.length).toBeGreaterThan(0);
    expect(u2.length).toBeGreaterThan(0);
    expect(u1.every((t) => t.usuarioId === 'u-1')).toBe(true);
  });
});
