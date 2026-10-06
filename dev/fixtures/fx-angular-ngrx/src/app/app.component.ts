// src/app/app.component.ts
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'fx-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `
    <div>
      <header class="fx-top">
        <a routerLink="/">Inicio</a>
        <a routerLink="/solicitudes">Solicitudes</a>
        <a routerLink="/aprobaciones">Aprobaciones</a>
        <a routerLink="/reportes">Reportes</a>
      </header>
      <main>
        <router-outlet></router-outlet>
      </main>
    </div>
  `
})
export class AppComponent {}
