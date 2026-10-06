// Rutas con lazy loadComponent (trampa del ecosistema #3).
// En un proyecto Angular real: import { Routes } from '@angular/router'.
// Aqui usamos un shim de tipos.

export interface Route {
  path?: string;
  redirectTo?: string;
  pathMatch?: 'full' | 'prefix';
  loadComponent?: () => Promise<unknown>;
  canActivate?: ReadonlyArray<unknown>;
}

export const routes: ReadonlyArray<Route> = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  {
    path: 'login',
    loadComponent: () => import('./features/login/login.page.js').then((m) => m.LoginPage),
    canActivate: [/* guestOnlyGuard */],
  },
  {
    path: 'listings',
    loadComponent: () => import('./features/listings/listings.page.js').then((m) => m.ListingsPage),
    canActivate: [/* authGuard */],
  },
  { path: '**', redirectTo: 'login' },
];
