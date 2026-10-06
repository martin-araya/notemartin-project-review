// Module file
// Effects con operadores RxJS que cambian la cancelacion:
// - load: switchMap (cancela el request anterior si llega uno nuevo)
// - create: exhaustMap (ignora clicks adicionales mientras hay
//   uno en vuelo)
// - update: mergeMap (reintentos automaticos)
import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { map, mergeMap, switchMap, catchError, of } from 'rxjs';
import { SolicitudesActions } from './actions';
import { ApiService } from '@app/core/services/api.service';

@Injectable()
export class SolicitudesEffects {
  private actions$ = inject(Actions);
  private api = inject(ApiService);

  // switchMap: cancela el request anterior si llega uno nuevo.
  load$ = createEffect(() =>
    this.actions$.pipe(
      ofType(SolicitudesActions.load),
      switchMap(() =>
        this.api.listAll().pipe(
          map((items) => SolicitudesActions.loadSuccess({ items })),
          catchError((err) => of(SolicitudesActions.loadFailure({ error: String(err) })))
        )
      )
    )
  );

  // exhaustMap: ignora clicks adicionales mientras hay uno en vuelo.
  create$ = createEffect(() =>
    this.actions$.pipe(
      ofType(SolicitudesActions.create),
      exhaustMapSafe((action) =>
        this.api.create(action.payload).pipe(
          map((item) => SolicitudesActions.createSuccess({ item })),
          catchError((err) => of(SolicitudesActions.createFailure({ error: String(err) })))
        )
      )
    )
  );

  // mergeMap: reintenta automaticamente si llegan varios updates.
  update$ = createEffect(() =>
    this.actions$.pipe(
      ofType(SolicitudesActions.update),
      mergeMap((action) =>
        of({ id: action.id, changes: action.changes }).pipe(
          map((payload) => SolicitudesActions.updateSuccess({ item: { id: payload.id, ...payload.changes } as any }))
        )
      )
    )
  );
}

// Helper para evitar error de TS: exhaustMap sin cast.
import { MonoTypeOperatorFunction, exhaustMap as rxExhaustMap, EMPTY } from 'rxjs';
function exhaustMapSafe<T>(project: (v: T) => any): MonoTypeOperatorFunction<T> {
  return rxExhaustMap((v) => project(v) ?? EMPTY);
}
