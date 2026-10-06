// src/app/app.config.ts
// Providers raiz: store global con feature state duplicado
// (trampa paquete #6). El provideStore duplica el state del
// modulo principal que luego tambien se registra via
// SolicitudesModule.forChild, produciendo selectores que
// retornan datos inconsistentes.
import { ApplicationConfig, importProvidersFrom, isDevMode } from '@angular/core';
import { provideRouter, withHashLocation } from '@angular/router';
import { provideStore } from '@ngrx/store';
import { provideEffects } from '@ngrx/effects';
import { provideStoreDevtools } from '@ngrx/store-devtools';
import { provideHttpClient, withInterceptorsFromDi, HTTP_INTERCEPTORS } from '@angular/common/http';

import { CoreModule } from './core/core.module';
import { SolicitudesModule } from './solicitudes/solicitudes.module';
import { SolicitudesEffects } from './solicitudes/store/effects';
import { reducer as solicitudesReducer, SOLICITUDES_FEATURE_KEY } from './solicitudes/store/reducer';
import { AuthInterceptor } from './core/interceptors/auth.interceptor';

import { APP_ROUTES } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(APP_ROUTES, withHashLocation()),
    // Trampa paquete #6: provideStore global + SolicitudesModule
    // via importProvidersFrom registran el mismo state dos veces.
    provideStore({ [SOLICITUDES_FEATURE_KEY]: solicitudesReducer }),
    provideEffects([SolicitudesEffects]),
    provideHttpClient(withInterceptorsFromDi()),
    provideStoreDevtools({ maxAge: 25, logOnly: !isDevMode() }),
    importProvidersFrom(CoreModule.forRoot(), SolicitudesModule),
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ]
};
