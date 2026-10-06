// src/app/core/pipes/monto.pipe.ts
// Pipe personalizado que formatea numeros como moneda. Trampa
// paquete #4: sin `pure: true` se redefine en cada ciclo de
// deteccion de cambios. La skill debe notar la anotacion.
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'monto' })
export class MontoPipe implements PipeTransform {
  // Sin `pure: true` (default true en Angular 17; la trampa es
  // que la implementacion lee una variable global mutable).
  private _currency = 'EUR';

  transform(value: number | null | undefined, prefix: string = this._currency): string {
    if (value == null) return '';
    return prefix + ' ' + value.toFixed(2);
  }
}
