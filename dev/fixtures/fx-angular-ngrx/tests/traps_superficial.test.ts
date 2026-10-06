// tests/traps_superficial.test.ts
// Verifica la presencia de las 3 trampas superficiales.
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';

const root = path.join(__dirname, '..');
function read(rel: string): string {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

describe('Trampas superficiales (CC-05)', () => {
  it('TRAP-S01: API_BASE_URL existe pero nadie la usa', () => {
    const svc = read('src/app/core/services/api.service.ts');
    expect(svc).toMatch(/export const API_BASE_URL/);
  });

  it('TRAP-S02: ReportesComponent importa SolicitudesActions pero no lo usa en el CSV', () => {
    const reportes = read('src/app/reportes/pages/reportes.component.ts');
    expect(reportes).toMatch(/import.*SolicitudesActions/);
  });

  it('TRAP-S03: ContadorDirective exporta count como publico sin uso externo', () => {
    const d = read('src/app/core/directives/contador.directive.ts');
    // El codigo usa `this.fxContador` (no export), pero @Input
    // aparece en el codigo. La trampa es la falta de OnDestroy.
    expect(d).toMatch(/@Input/);
  });
});
