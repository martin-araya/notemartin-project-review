// Module file
// Componente standalone. Filtra items pendientes del store
// principal via selectFilteredItems y permite aprobar/rechazar.
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { Item } from '@app/solicitudes/store/state';
import { SolicitudesActions } from '@app/solicitudes/store/actions';
import { selectAllItems } from '@app/solicitudes/store/reducer';
import { AprobacionesActions } from '../store/actions';

@Component({
  selector: 'fx-cola-aprobaciones',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <section>
      <h2>Cola de aprobaciones</h2>
      <ul class="fx-list">
        <li *ngFor="let item of pendientes">
          <strong>{{ item.id }}</strong> - {{ item.nombre }}
          <input [(ngModel)]="comentario[item.id]" placeholder="Comentario (rechazo)" />
          <button (click)="approve(item)">Aprobar</button>
          <button (click)="reject(item)">Rechazar</button>
        </li>
      </ul>
    </section>
  `
})
export class ColaAprobacionesComponent implements OnInit {
  private store = inject(Store);
  private router = inject(Router);
  pendientes: Item[] = [];
  comentario: Record<string, string> = {};

  ngOnInit(): void {
    this.store.select(selectAllItems).subscribe((items) => {
      this.pendientes = items.filter((i) => i.estado === 'pendiente');
    });
    this.store.dispatch(SolicitudesActions.load());
  }

  approve(item: Item): void {
    this.store.dispatch(AprobacionesActions.approve({
      itemId: item.id, usuarioId: 'u-1', comentario: this.comentario[item.id]
    }));
  }

  reject(item: Item): void {
    this.store.dispatch(AprobacionesActions.reject({
      itemId: item.id, usuarioId: 'u-1', comentario: this.comentario[item.id] || ''
    }));
  }
}
