// Module file
// Detalle por route param. Usa *ngIf directo (trampa CC-06:
// la skill debe notar que este componente renderiza sin
// verificar si el item existe en el store, mostrando `null`).
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { Store } from '@ngrx/store';
import { map, Observable } from 'rxjs';
import { Item } from '../store/state';
import { selectItemEntities, SolicitudesActions } from '../store/reducer';
import { Actions, ofType } from '@ngrx/effects';

@Component({
  selector: 'fx-detalle-solicitud',
  standalone: true,
  imports: [CommonModule],
  template: `
    <section *ngIf="item$ | async as item; else missing">
      <h2>Detalle {{ item.id }}</h2>
      <p>Nombre: {{ item.nombre }}</p>
      <p>Monto: {{ item.monto }}</p>
      <p>Estado: {{ item.estado }}</p>
      <p *ngIf="item.premium" class="info">Premium</p>
    </section>
    <ng-template #missing>
      <p>No encontrado</p>
    </ng-template>
  `
})
export class DetalleSolicitudComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private store = inject(Store);

  item$: Observable<Item | undefined> = this.store.select(selectItemEntities).pipe(
    map((entities) => entities[this.route.snapshot.paramMap.get('id') || ''])
  );

  ngOnInit(): void {
    this.store.dispatch(SolicitudesActions.load());
  }
}
