// Module file
import { Routes } from '@angular/router';

export const APROBACIONES_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/cola-aprobaciones.component').then((m) => m.ColaAprobacionesComponent)
  }
];
