// tests/traps_ecosystem.test.ts
// Verifica la presencia literal de las 6 trampas del ecosistema
// plantadas en el codigo del fixture.
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';

const root = path.join(__dirname, '..');

function read(rel: string): string {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

describe('Trampas del ecosistema (CC-06)', () => {
  it('TRAP-E01: flujo action -> effect -> service -> action', () => {
    const effects = read('src/app/solicitudes/store/effects.ts');
    expect(effects).toMatch(/createEffect/);
    expect(effects).toMatch(/ofType\(SolicitudesActions\./);
    expect(effects).toMatch(/this\.api\.listAll/);
    expect(effects).toMatch(/SolicitudesActions\.loadSuccess/);
  });

  it('TRAP-E02: createActionGroup genera namespace Solicitudes', () => {
    const actions = read('src/app/solicitudes/store/actions.ts');
    expect(actions).toMatch(/createActionGroup/);
    expect(actions).toMatch(/source:\s*'Solicitudes'/);
  });

  it('TRAP-E03: efectos usan switchMap, exhaustMap, mergeMap segun semantica', () => {
    const effects = read('src/app/solicitudes/store/effects.ts');
    expect(effects).toMatch(/switchMap/);
    expect(effects).toMatch(/exhaustMapSafe/);
    expect(effects).toMatch(/mergeMap/);
  });

  it('TRAP-E04: CoreModule.forRoot + StoreModule.forFeature (forChild)', () => {
    const core = read('src/app/core/core.module.ts');
    const solicitudes = read('src/app/solicitudes/solicitudes.module.ts');
    expect(core).toMatch(/static forRoot/);
    expect(core).toMatch(/multi: true/);
    expect(solicitudes).toMatch(/StoreModule\.forFeature/);
  });

  it('TRAP-E05: HTTP_INTERCEPTORS con multi: true', () => {
    const core = read('src/app/core/core.module.ts');
    expect(core).toMatch(/HTTP_INTERCEPTORS/);
    const count = (core.match(/HTTP_INTERCEPTORS/g) || []).length;
    expect(count).toBeGreaterThanOrEqual(2);
  });

  it('TRAP-E06: pipes y directivas personalizados', () => {
    const pipe = read('src/app/core/pipes/monto.pipe.ts');
    const dir = read('src/app/core/directives/contador.directive.ts');
    expect(pipe).toMatch(/Pipe\s*\(\s*\{\s*name:\s*'monto'/);
    expect(dir).toMatch(/Directive\s*\(/);
    expect(dir).toMatch(/setInterval/);
  });
});
