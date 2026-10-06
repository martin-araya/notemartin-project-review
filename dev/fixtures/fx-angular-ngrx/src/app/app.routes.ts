// src/app/app.routes.ts
import { Routes } from '@angular/router';

export const APP_ROUTES: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'solicitudes' },
  {
    path: 'solicitudes',
    loadChildren: () => import('./solicitudes/solicitudes.routes').then((m) => m.SOLICITUDES_ROUTES)
  },
  {
    path: 'aprobaciones',
    loadChildren: () => import('./aprobaciones/aprobaciones.routes').then((m) => m.APROBACIONES_ROUTES)
  },
  {
    path: 'reportes',
    loadChildren: () => import('./reportes/reportes.routes').then((m) => m.REPORTES_ROUTES)
  }
];
