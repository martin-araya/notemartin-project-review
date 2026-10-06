// shim para tests: provee tipos y contratos sin requerir @angular/core real.
// En un proyecto Angular real este archivo importa de @angular/core y
// configura providers. Aqui documentamos los proveedores que el scanner
// debe descubrir.
//
// Trampa del ecosistema #3:
//   - provideHttpClient(withInterceptors([authInterceptor, loggingInterceptor]))
//   - functional guards e interceptors

import type { Environment } from '../environments/environment.js';

export interface AppConfig {
  providers: ReadonlyArray<unknown>;
}

// El config efectivo se reemplaza en build via environment.ts (trampa #5).
export const appConfig: AppConfig = {
  providers: [
    // provideRouter(routes, withComponentInputBinding()),
    // provideHttpClient(withInterceptors([authInterceptor, loggingInterceptor])),
  ],
};

export type { Environment };
