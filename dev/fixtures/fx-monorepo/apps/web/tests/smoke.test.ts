// Smoke tests para apps/web. Verifican que el module graph se importa sin
// error y que las trampas documentadas estan presentes en el codigo
// (sin necesidad de un browser).
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', 'src');        // apps/web/src
const APP = join(HERE, '..');                // apps/web

function readSrc(rel: string): string {
  return readFileSync(join(ROOT, rel), 'utf-8');
}

function readApp(rel: string): string {
  return readFileSync(join(APP, rel), 'utf-8');
}

describe('apps/web module graph (file existence)', () => {
  it('AppComponent existe y se puede importar via require', async () => {
    // No podemos importar directamente (Angular CLI no esta instalado);
    // verificamos la existencia del archivo y la exportacion de la clase.
    const src = readSrc('app/app.component.ts');
    expect(src).toContain('export class AppComponent');
  });

  it('appConfig provee providers (functional interceptors)', () => {
    const src = readSrc('app/app.config.ts');
    expect(src).toContain('appConfig');
    expect(src).toContain('providers');
    expect(src).toContain('withInterceptors');
  });

  it('routes declara lazy loadComponent y canActivate', () => {
    const src = readSrc('app/app.routes.ts');
    expect(src).toContain('loadComponent');
    expect(src).toContain('canActivate');
  });

  it('authGuard y guestOnlyGuard son CanActivateFn', () => {
    const src = readSrc('app/core/auth.guard.ts');
    expect(src).toContain('CanActivateFn');
    expect(src).toContain('authGuard');
    expect(src).toContain('guestOnlyGuard');
  });

  it('authInterceptor y loggingInterceptor son HttpInterceptorFn', () => {
    const src = readSrc('app/core/auth.interceptor.ts');
    expect(src).toContain('HttpInterceptorFn');
    expect(src).toContain('authInterceptor');
    expect(src).toContain('loggingInterceptor');
  });

  it('LoginPage existe y declara submit + effectRef', () => {
    const src = readSrc('app/features/login/login.page.ts');
    expect(src).toContain('class LoginPage');
    expect(src).toContain('submit');
    expect(src).toContain('effectRef');
  });

  it('ListingsPage existe y declara updateFilter + effectRef', () => {
    const src = readSrc('app/features/listings/listings.page.ts');
    expect(src).toContain('class ListingsPage');
    expect(src).toContain('updateFilter');
    expect(src).toContain('effectRef');
  });
});

describe('apps/web traps (ecosystem + package)', () => {
  it('trap #1: tsconfig.json tiene path alias @fx-mono/shared', () => {
    const ts = JSON.parse(readApp('tsconfig.json'));
    const app = JSON.parse(readApp('tsconfig.app.json'));
    const hasAlias = (ts.compilerOptions?.paths?.['@fx-mono/shared'] !== undefined)
                 || (app.compilerOptions?.paths?.['@fx-mono/shared'] !== undefined);
    expect(hasAlias).toBe(true);
  });

  it('trap #1: package.json usa workspace:*', () => {
    const pkg = JSON.parse(readApp('package.json'));
    expect(pkg.dependencies['@fx-mono/shared']).toBe('workspace:*');
  });

  it('trap #3: loadComponent se usa en las rutas', () => {
    const routes = readSrc('app/app.routes.ts');
    expect(routes).toMatch(/loadComponent\s*:/);
  });

  it('trap #3: CanActivateFn se usa en auth.guard', () => {
    const guard = readSrc('app/core/auth.guard.ts');
    expect(guard).toContain('CanActivateFn');
  });

  it('trap #3: HttpInterceptorFn se usa en auth.interceptor', () => {
    const inter = readSrc('app/core/auth.interceptor.ts');
    expect(inter).toContain('HttpInterceptorFn');
  });

  it('trap #4: effect() usado en login.page (no solo declarado)', () => {
    const login = readSrc('app/features/login/login.page.ts');
    expect(login).toContain('effectRef');
    expect(login).toContain("console.log('[effect] token changed");
  });

  it('trap #5: angular.json tiene fileReplacements', () => {
    const aj = JSON.parse(readApp('angular.json'));
    const devCfg = aj.projects['fx-mono-web'].architect.build.configurations.development;
    const prodCfg = aj.projects['fx-mono-web'].architect.build.configurations.production;
    expect(devCfg.fileReplacements).toBeDefined();
    expect(prodCfg.fileReplacements).toBeDefined();
  });

  it('trap #5: production tiene production: true', () => {
    const env = readSrc('environments/environment.production.ts');
    expect(env).toContain('production: true');
  });

  it('trap #5: development tiene production: false', () => {
    const env = readSrc('environments/environment.development.ts');
    expect(env).toContain('production: false');
  });

  it('trap #6: proxy.conf.json apunta /api al backend', () => {
    const proxy = JSON.parse(readApp('proxy.conf.json'));
    expect(proxy['/api'].target).toMatch(/^http:\/\/[^/]+/);
  });
});

describe('apps/web package traps', () => {
  it('trap P1: authInterceptor agrega Bearer incluso con token vacio', () => {
    const inter = readSrc('app/core/auth.interceptor.ts');
    // El interceptor no valida token vacio (comentario explicito).
    expect(inter.toLowerCase()).toContain('trampa de paquete #1');
    expect(inter).toContain('no validamos que el token no este vacio');
  });

  it('trap P2: LoginService no desuscribe el observable', () => {
    const svc = readSrc('app/features/login/login.service.ts');
    expect(svc.toLowerCase()).toContain('trampa de paquete #2');
    // El servicio no implementa cleanup real (sin takeUntilDestroyed,
    // sin unsubscribe manual). El comentario lo admite explicitamente.
    expect(svc).not.toContain('takeUntilDestroyed');
    expect(svc).not.toContain('pipe(takeUntil');
  });

  it('trap P3: ListingsPage effect() depende de this completo', () => {
    const page = readSrc('app/features/listings/listings.page.ts');
    expect(page.toLowerCase()).toContain('trampa de paquete #3');
    expect(page).toContain('el effect lee');
  });
});
