// Module file
// Cross-feature effect: al aprobar, dispara un update sobre el
// store del modulo principal para reflejar el cambio de estado.
import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { map, mergeMap, withLatestFrom, filter, tap } from 'rxjs/operators';
import { of } from 'rxjs';
import { AprobacionesActions } from './actions';
import { SolicitudesActions } from '@app/solicitudes/store/actions';
import { selectAllItems } from '@app/solicitudes/store/reducer';
import { Store } from '@ngrx/store';

@Injectable()
export class AprobacionesEffects {
  private actions$ = inject(Actions);
  private store = inject(Store);

  // Cross-feature: al aprobar, dispara SolicitudesActions.update
  // con el nuevo estado. Trampa paquete #6: si el effect ya esta
  // escuchando SolicitudesActions.filter en su modulo, hay un
  // bucle. Aqui solo escuchamos approve, pero el diseno propaga
  // y rompe en produccion.
  approveAndPropagate$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AprobacionesActions.approve),
      withLatestFrom(this.store.select(selectAllItems)),
      mergeMap(([action, items]) => {
        const item = items.find((i) => i.id === action.itemId);
        if (!item || item.estado !== 'pendiente') {
          return of(AprobacionesActions.failure({
            error: item ? 'already_decided' : 'not_found'
          }));
        }
        const aprobacion = {
          id: 'ap-' + Date.now(),
          itemId: action.itemId,
          usuarioId: action.usuarioId,
          decision: 'aprobado' as const,
          comentario: action.comentario,
          fecha: new Date().toISOString().slice(0, 10)
        };
        // Dispara update sobre el modulo principal.
        this.store.dispatch(SolicitudesActions.update({
          id: action.itemId,
          changes: { estado: 'aprobado' }
        }));
        return of(AprobacionesActions.approveSuccess({ aprobacion }));
      })
    )
  );

  rejectAndPropagate$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AprobacionesActions.reject),
      withLatestFrom(this.store.select(selectAllItems)),
      mergeMap(([action, items]) => {
        const item = items.find((i) => i.id === action.itemId);
        if (!item) {
          return of(AprobacionesActions.failure({ error: 'not_found' }));
        }
        if (!action.comentario || action.comentario.length < 3) {
          return of(AprobacionesActions.failure({ error: 'comentario_required' }));
        }
        const aprobacion = {
          id: 'ap-' + Date.now(),
          itemId: action.itemId,
          usuarioId: action.usuarioId,
          decision: 'rechazado' as const,
          comentario: action.comentario,
          fecha: new Date().toISOString().slice(0, 10)
        };
        this.store.dispatch(SolicitudesActions.update({
          id: action.itemId,
          changes: { estado: 'rechazado' }
        }));
        return of(AprobacionesActions.rejectSuccess({ aprobacion }));
      })
    )
  );
}
