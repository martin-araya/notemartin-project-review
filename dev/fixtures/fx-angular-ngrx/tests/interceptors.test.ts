// tests/interceptors.test.ts
// Tests estaticos de los HTTP_INTERCEPTORS. No usan TestBed
// (que requiere jest-preset-angular) sino grep sobre el codigo.
import { describe, it, expect } from 'vitest';
import * as fs from 'node:fs';
import * as path from 'node:path';

const root = path.join(__dirname, '..');
function read(rel: string): string {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

describe('FEAT-001 HTTP_INTERCEPTORS', () => {
  it('CoreModule declara dos providers con multi: true', () => {
    const core = read('src/app/core/core.module.ts');
    const matches = core.match(/multi:\s*true/g) || [];
    expect(matches.length).toBeGreaterThanOrEqual(2);
  });

  it('AuthInterceptor anade Authorization: Bearer', () => {
    const ic = read('src/app/core/interceptors/auth.interceptor.ts');
    expect(ic).toMatch(/Authorization/);
    expect(ic).toMatch(/Bearer/);
  });

  it('LoggingInterceptor loguea cada peticion con tap', () => {
    const ic = read('src/app/core/interceptors/logging.interceptor.ts');
    expect(ic).toMatch(/tap/);
    expect(ic).toMatch(/HttpResponse/);
  });

  it('AuthInterceptor usa window.localStorage (SSR-incompatible)', () => {
    const ic = read('src/app/core/interceptors/auth.interceptor.ts');
    expect(ic).toMatch(/window\.localStorage/);
  });

  it('El orden de declaracion es auth antes que logging', () => {
    const core = read('src/app/core/core.module.ts');
    const authIdx = core.indexOf('AuthInterceptor');
    const logIdx = core.indexOf('LoggingInterceptor');
    expect(authIdx).toBeGreaterThan(-1);
    expect(logIdx).toBeGreaterThan(authIdx);
  });
});
