// Module file
import { createActionGroup, emptyProps, props } from '@ngrx/store';
import { Aprobacion } from './state';

export const AprobacionesActions = createActionGroup({
  source: 'Aprobaciones',
  events: {
    load: emptyProps(),
    loadSuccess: props<{ items: Aprobacion[] }>(),
    approve: props<{ itemId: string; usuarioId: string; comentario?: string }>(),
    approveSuccess: props<{ aprobacion: Aprobacion }>(),
    reject: props<{ itemId: string; usuarioId: string; comentario: string }>(),
    rejectSuccess: props<{ aprobacion: Aprobacion }>(),
    failure: props<{ error: string }>()
  }
});
