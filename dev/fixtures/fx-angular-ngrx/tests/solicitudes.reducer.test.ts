// tests/solicitudes.reducer.test.ts
// Tests estaticos del reducer + createEntityAdapter. No se
// importa el modulo (que requiere Angular runtime) sino que se
// valida el codigo.
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';

const root = path.join(__dirname, '..');
function read(rel: string): string {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

describe('FEAT-001 reducer (entity adapter)', () => {
  it('inicia con adapter.getInitialState y campos loading/error', () => {
    const r = read('src/app/solicitudes/store/reducer.ts');
    expect(r).toMatch(/createEntityAdapter<Item>/);
    expect(r).toMatch(/getInitialState/);
    expect(r).toMatch(/loading:\s*false/);
    expect(r).toMatch(/error:\s*null/);
  });

  it('declara handlers on(load) y on(loadSuccess)', () => {
    const r = read('src/app/solicitudes/store/reducer.ts');
    expect(r).toMatch(/on\(SolicitudesActions\.load/);
    expect(r).toMatch(/on\(SolicitudesActions\.loadSuccess/);
    expect(r).toMatch(/setAll/);
  });

  it('declara handlers on(createSuccess) y on(updateSuccess)', () => {
    const r = read('src/app/solicitudes/store/reducer.ts');
    expect(r).toMatch(/on\(SolicitudesActions\.createSuccess/);
    expect(r).toMatch(/addOne/);
    expect(r).toMatch(/on\(SolicitudesActions\.updateSuccess/);
    expect(r).toMatch(/upsertOne/);
  });

  it('expone selectores createFeatureSelector + createSelector', () => {
    const r = read('src/app/solicitudes/store/reducer.ts');
    expect(r).toMatch(/createFeatureSelector/);
    expect(r).toMatch(/createSelector/);
    expect(r).toMatch(/selectAllItems/);
    expect(r).toMatch(/selectLoading/);
    expect(r).toMatch(/selectError/);
  });
});
