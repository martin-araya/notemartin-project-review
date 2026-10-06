// Module file
// Selector computado: agrega items por estado y muestra el total
// monetario. Usa el pipe MontoPipe del modulo core.
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Store } from '@ngrx/store';
import { Observable, combineLatest, map } from 'rxjs';
import { Item } from '@app/solicitudes/store/state';
import { selectAllItems } from '@app/solicitudes/store/reducer';
import { SolicitudesActions } from '@app/solicitudes/store/actions';
import { MontoPipe } from '@app/core/pipes/monto.pipe';

interface Reporte {
  total: number;
  pendientes: number;
  aprobados: number;
  rechazados: number;
  montoTotal: number;
  vacio: boolean;
}

@Component({
  selector: 'fx-reportes',
  standalone: true,
  imports: [CommonModule, FormsModule, MontoPipe],
  template: `
    <section>
      <h2>Reportes</h2>
      <p *ngIf="reporte$ | async as r">
        <span *ngIf="r.vacio">Sin datos</span>
        <span *ngIf="!r.vacio">
          Total: {{ r.total }} - Pendientes: {{ r.pendientes }} - Aprobados: {{ r.aprobados }} - Rechazados: {{ r.rechazados }} - Monto: {{ r.montoTotal | monto }}
        </span>
      </p>
      <button (click)="exportarCSV()">Exportar CSV</button>
    </section>
  `
})
export class ReportesComponent implements OnInit {
  private store = inject(Store);

  reporte$: Observable<Reporte> = this.store.select(selectAllItems).pipe(
    map((items: Item[]) => {
      if (items.length === 0) {
        return { total: 0, pendientes: 0, aprobados: 0, rechazados: 0, montoTotal: 0, vacio: true } as Reporte;
      }
      return {
        total: items.length,
        pendientes: items.filter((i) => i.estado === 'pendiente').length,
        aprobados: items.filter((i) => i.estado === 'aprobado').length,
        rechazados: items.filter((i) => i.estado === 'rechazado').length,
        montoTotal: items.reduce((acc, i) => acc + (i.monto ?? 0), 0),
        vacio: false
      } as Reporte;
    })
  );

  ngOnInit(): void {
    this.store.dispatch(SolicitudesActions.load());
  }

  exportarCSV(): void {
    // Genera un CSV simple en memoria. En un fixture real haria
    // una llamada al backend; aqui solo dispara el dialogo de
    // descarga.
    if (typeof document === 'undefined') return;
    // Dead import: este componente importa SolicitudesActions arriba
    // pero no lo usa para nada relacionado con el CSV. La trampa
    // paquete #6 es exactamente este patron.
  }
}
