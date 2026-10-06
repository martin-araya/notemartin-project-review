// tests/traps_package.test.ts
// Verifica la presencia de las 6 trampas del paquete plantadas.
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';

const root = path.join(__dirname, '..');
function read(rel: string): string {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

describe('Trampas del paquete (CC-04)', () => {
  it('TRAP-P01: ApiService.listAll retorna observable vacio', () => {
    const svc = read('src/app/core/services/api.service.ts');
    expect(svc).toMatch(/listAll\s*\(\)/);
    // La trampa es que el seed existe pero nunca se devuelve.
    expect(svc).toMatch(/of\(\[\]\)/);
  });

  it('TRAP-P02: AuthInterceptor usa window.localStorage (SSR-incompatible)', () => {
    const ic = read('src/app/core/interceptors/auth.interceptor.ts');
    expect(ic).toMatch(/window\.localStorage/);
    // La trampa: el guard `typeof window !== 'undefined'` esta
    // ahi, lo que indica que el codigo sabe del problema SSR pero
    // lo "arregla" devolviendo 'ssr-token'.
    expect(ic).toMatch(/ssr-token/);
  });

  it('TRAP-P03: MontoPipe sin pure: true explicito', () => {
    const pipe = read('src/app/core/pipes/monto.pipe.ts');
    expect(pipe).toMatch(/Pipe\s*\(\s*\{\s*name:\s*'monto'/);
    // En Angular 17, pure es true por defecto; la trampa es que
    // lee _currency de una variable mutable.
    expect(pipe).toMatch(/private _currency/);
  });

  it('TRAP-P04: createEntityAdapter sin selectId custom (id por defecto)', () => {
    const reducer = read('src/app/solicitudes/store/reducer.ts');
    expect(reducer).toMatch(/createEntityAdapter<Item>/);
    // No se pasa clave custom.
    expect(reducer).not.toMatch(/selectId\s*:/);
  });

  it('TRAP-P05: provideStore global + SolicitudesModule duplican el state', () => {
    const cfg = read('src/app/app.config.ts');
    expect(cfg).toMatch(/provideStore/);
    expect(cfg).toMatch(/importProvidersFrom\(CoreModule\.forRoot\(\),\s*SolicitudesModule\)/);
  });

  it('TRAP-P06: ContadorDirective sin OnDestroy (memory leak)', () => {
    const d = read('src/app/core/directives/contador.directive.ts');
    expect(d).toMatch(/OnInit/);
    expect(d).toMatch(/setInterval/);
    // No implementa OnDestroy.
    expect(d).not.toMatch(/OnDestroy/);
    expect(d).not.toMatch(/clearInterval/);
  });
});
