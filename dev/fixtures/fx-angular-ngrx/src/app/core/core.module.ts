// src/app/core/core.module.ts
// NgModule con forRoot: provee HTTP_INTERCEPTORS (auth + logging)
// con multi: true. El orden de declaracion determina el orden
// de ejecucion.
import { NgModule, Optional, SkipSelf, ModuleWithProviders } from '@angular/core';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { LoggingInterceptor } from './interceptors/logging.interceptor';

@NgModule({
  imports: [HttpClientModule],
  exports: [HttpClientModule]
})
export class CoreModule {
  // Trampa paquete #4: si CoreModule.forRoot() se importa dos veces
  // (e.g. via lazy load que olvida skipSelf), los interceptors
  // se duplican y cada peticion se procesa 2 veces.
  constructor(@Optional() @SkipSelf() parent?: CoreModule) {
    if (parent) {
      throw new Error('CoreModule ya fue cargado; usa forRoot solo una vez en AppModule.');
    }
  }

  static forRoot(): ModuleWithProviders<CoreModule> {
    return {
      ngModule: CoreModule,
      providers: [
        { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
        { provide: HTTP_INTERCEPTORS, useClass: LoggingInterceptor, multi: true }
      ]
    };
  }
}
