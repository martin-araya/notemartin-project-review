// Module file
import { Routes } from '@angular/router';

export const REPORTES_ROUTES: Routes = [
  { path: '', component: (() => import('./pages/reportes.component').then((m) => m.ReportesComponent)) as any }
];
