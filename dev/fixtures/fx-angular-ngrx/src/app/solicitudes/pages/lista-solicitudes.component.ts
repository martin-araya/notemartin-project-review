// Module file
// Componente standalone. Carga items via Store y los renderiza
// con el pipe MontoPipe y la directiva fxContador.
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { Item } from '../store/state';
import { SolicitudesActions } from '../store/actions';
import { selectAllItems, selectLoading, selectError } from '../store/reducer';
import { MontoPipe } from '@app/core/pipes/monto.pipe';
import { ContadorDirective } from '@app/core/directives/contador.directive';

@Component({
  selector: 'fx-lista-solicitudes',
  standalone: true,
  imports: [CommonModule, MontoPipe, ContadorDirective],
  template: `
    <section>
      <h2>Listado</h2>
      <p *ngIf="loading$ | async">Cargando...</p>
      <p *ngIf="error$ | async as err" class="error">{{ err }}</p>
      <ul class="fx-list" [fxContador]="0">
        <li *ngFor="let item of items$ | async" [class.premium-hide]="item.premium">
          <strong>{{ item.id }}</strong> - {{ item.nombre }} - {{ item.monto | monto }}
          <button (click)="goToDetail(item.id)">Detalle</button>
        </li>
      </ul>
    </section>
  `
})
export class ListaSolicitudesComponent implements OnInit {
  private store = inject(Store);
  items$: Observable<Item[]> = this.store.select(selectAllItems);
  loading$ = this.store.select(selectLoading);
  error$: Observable<string | null> = this.store.select(selectError);

  ngOnInit(): void {
    this.store.dispatch(SolicitudesActions.load());
  }

  goToDetail(id: string): void {
    window.location.href = '/solicitudes/' + id;
  }
}
