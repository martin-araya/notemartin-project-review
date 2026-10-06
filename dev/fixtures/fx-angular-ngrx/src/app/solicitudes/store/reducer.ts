// Module file
// createReducer + createEntityAdapter. La trampa paquete #5 es
// que las entidades con clave distinta de `id` requieren
// clave custom; aqui no se provee.
import { createReducer, on, createFeatureSelector, createSelector } from '@ngrx/store';
import { createEntityAdapter, EntityState } from '@ngrx/entity';
import { SolicitudesActions } from './actions';
import { Item, SOLICITUDES_FEATURE_KEY } from './state';

export interface SolicitudesState extends EntityState<Item> {
  loading: boolean;
  error: string | null;
  filter: { estado?: 'pendiente' | 'aprobado' | 'rechazado' };
}

export const adapter = createEntityAdapter<Item>();

export const initialState: SolicitudesState = adapter.getInitialState({
  loading: false,
  error: null,
  filter: {}
});

export const reducer = createReducer(
  initialState,
  on(SolicitudesActions.load, (state) => ({ ...state, loading: true, error: null })),
  on(SolicitudesActions.loadSuccess, (state, { items }) =>
    adapter.setAll(items, { ...state, loading: false, error: null })
  ),
  on(SolicitudesActions.loadFailure, (state, { error }) => ({ ...state, loading: false, error })),
  on(SolicitudesActions.createSuccess, (state, { item }) => adapter.addOne(item, state)),
  on(SolicitudesActions.createFailure, (state, { error }) => ({ ...state, error })),
  on(SolicitudesActions.updateSuccess, (state, { item }) => adapter.upsertOne(item, state)),
  on(SolicitudesActions.updateFailure, (state, { error }) => ({ ...state, error })),
  on(SolicitudesActions.filter, (state, { estado }) => ({ ...state, filter: { estado } }))
);

export const selectSolicitudesState = createFeatureSelector<SolicitudesState>(SOLICITUDES_FEATURE_KEY);

const { selectAll, selectEntities } = adapter.getSelectors();
export const selectAllItems = createSelector(selectSolicitudesState, selectAll);
export const selectItemEntities = createSelector(selectSolicitudesState, selectEntities);
export const selectLoading = createSelector(selectSolicitudesState, (s) => s.loading);
export const selectError = createSelector(selectSolicitudesState, (s) => s.error);
export const selectFilter = createSelector(selectSolicitudesState, (s) => s.filter);

// Selector computado que filtra por estado. Lo usa ReportesComponent
// para agregar datos.
export const selectFilteredItems = createSelector(
  selectAllItems,
  selectFilter,
  (items, filter) => {
    if (!filter.estado) return items;
    return items.filter((i) => i.estado === filter.estado);
  }
);
