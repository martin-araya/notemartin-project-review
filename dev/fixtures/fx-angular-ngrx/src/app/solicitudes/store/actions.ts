// Module file
// createActionGroup: las acciones se generan automaticamente
// bajo el namespace `SolicitudesActions`. La skill debe notar
// que los nombres de las acciones (load, loadSuccess, etc.)
// vienen del objeto events.
import { createActionGroup, emptyProps, props } from '@ngrx/store';
import { Item } from './state';

export const SolicitudesActions = createActionGroup({
  source: 'Solicitudes',
  events: {
    load: emptyProps(),
    loadSuccess: props<{ items: Item[] }>(),
    loadFailure: props<{ error: string }>(),
    create: props<{ payload: Omit<Item, 'id'> }>(),
    createSuccess: props<{ item: Item }>(),
    createFailure: props<{ error: string }>(),
    update: props<{ id: string; changes: Partial<Item> }>(),
    updateSuccess: props<{ item: Item }>(),
    updateFailure: props<{ error: string }>(),
    filter: props<{ estado?: 'pendiente' | 'aprobado' | 'rechazado' }>()
  }
});
