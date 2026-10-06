// Module file
// Rutas lazy del feature. Se cargan via loadComponent en app.routes.
import { Routes } from '@angular/router';

export const SOLICITUDES_ROUTES: Routes = [
  { path: '', redirectTo: 'lista', pathMatch: 'full' },
  {
    path: 'lista',
    loadComponent: () => import('./pages/lista-solicitudes.component').then((m) => m.ListaSolicitudesComponent)
  },
  {
    path: 'nueva',
    loadComponent: () => import('./pages/nueva-solicitud.component').then((m) => m.NuevaSolicitudComponent)
  },
  {
    path: ':id',
    loadComponent: () => import('./pages/detalle-solicitud.component').then((m) => m.DetalleSolicitudComponent)
  }
];
