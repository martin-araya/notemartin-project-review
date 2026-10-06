// src/app.d.ts
// Tipos globales para SvelteKit. App.Locals se usa en hooks.server.ts.
declare global {
  namespace App {
    interface Locals {
      user?: { id: string; role: 'user' | 'premium' } | null;
    }
    interface PageData {
      user?: { id: string; role: 'user' | 'premium' } | null;
    }
  }
}

export {};
