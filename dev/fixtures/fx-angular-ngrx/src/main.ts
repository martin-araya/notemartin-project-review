// src/main.ts
// Bootstrap standalone con importProvidersFrom para los modulos
// legacy (CoreModule, SolicitudesModule, etc).
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
