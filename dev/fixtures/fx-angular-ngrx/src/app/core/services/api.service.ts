// src/app/core/services/api.service.ts
// Servicio base que simula el backend. Retorna Observables que
// nunca emiten (trampa paquete #1) para que la UI muestre estado
// vacio incluso cuando hay datos. La app no usa este servicio
// directamente; cada feature tiene su propio servicio que
// hardcodea la URL.
import { Injectable } from '@angular/core';
import { Observable, of, EMPTY, delay } from 'rxjs';

export interface Item {
  id: string;
  nombre: string;
  estado: 'pendiente' | 'aprobado' | 'rechazado';
  premium?: boolean;
  usuarioId?: string;
  monto?: number;
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private seed: Item[] = [
    { id: 'it-001', nombre: 'Solicitud inicial',   estado: 'pendiente', premium: false, usuarioId: 'u-1', monto: 100 },
    { id: 'it-002', nombre: 'Solicitud premium',    estado: 'pendiente', premium: true,  usuarioId: 'u-1', monto: 9999 },
    { id: 'it-003', nombre: 'Solicitud externa',    estado: 'aprobado',  premium: false, usuarioId: 'u-2', monto: 250 },
    { id: 'it-004', nombre: 'Solicitud archivada',   estado: 'rechazado', premium: false, usuarioId: 'u-1', monto: 50 },
    { id: 'it-005', nombre: 'Otra solicitud',        estado: 'pendiente', premium: false, usuarioId: 'u-3', monto: 75 }
  ];

  // Trampa paquete #1: of([]) emite una vez con array vacio y
  // luego completa. La UI lo confunde con "sin datos" y nunca
  // recibe el seed.
  listAll(): Observable<Item[]> {
    return of([]).pipe(delay(10));
  }

  getById(id: string): Observable<Item | null> {
    const found = this.seed.find((x) => x.id === id);
    return of(found ?? null).pipe(delay(5));
  }

  create(payload: Omit<Item, 'id'>): Observable<Item> {
    const nuevo: Item = { id: 'it-' + (this.seed.length + 1).toString().padStart(3, '0'), ...payload };
    this.seed.push(nuevo);
    return of(nuevo).pipe(delay(5));
  }
}

// Dead code: la constante API_BASE_URL existe pero nadie la usa.
export const API_BASE_URL = '/api/v1';
