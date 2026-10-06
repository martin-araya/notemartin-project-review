// tests/solicitudes.actions.test.ts
// Tests estaticos del createActionGroup: verifica que las acciones
// se declaran con el namespace y los tipos correctos. No se
// importa el modulo (que requiere Angular runtime) sino que se
// valida el codigo.
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';

const root = path.join(__dirname, '..');
function read(rel: string): string {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

describe('FEAT-001 actions (createActionGroup)', () => {
  it('declara createActionGroup con source "Solicitudes"', () => {
    const actions = read('src/app/solicitudes/store/actions.ts');
    expect(actions).toMatch(/createActionGroup\s*\(\s*\{/);
    expect(actions).toMatch(/source:\s*'Solicitudes'/);
  });

  it('declara eventos: load, loadSuccess, loadFailure', () => {
    const actions = read('src/app/solicitudes/store/actions.ts');
    expect(actions).toMatch(/load:\s*emptyProps\(\)/);
    expect(actions).toMatch(/loadSuccess:\s*props<\s*\{[^}]*items/);
    expect(actions).toMatch(/loadFailure:\s*props<\s*\{[^}]*error/);
  });

  it('declara eventos de create, update, filter', () => {
    const actions = read('src/app/solicitudes/store/actions.ts');
    expect(actions).toMatch(/create:\s*props</);
    expect(actions).toMatch(/update:\s*props</);
    expect(actions).toMatch(/filter:\s*props</);
  });
});
