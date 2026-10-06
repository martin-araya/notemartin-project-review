// Module file
import { createReducer, on, createFeatureSelector, createSelector } from '@ngrx/store';
import { AprobacionesActions } from './actions';
import { AprobacionesState, APROBACIONES_FEATURE_KEY } from './state';

export const initialState: AprobacionesState = {
  items: [],
  loading: false
};

export const reducer = createReducer(
  initialState,
  on(AprobacionesActions.load, (state) => ({ ...state, loading: true })),
  on(AprobacionesActions.loadSuccess, (state, { items }) => ({ ...state, loading: false, items })),
  on(AprobacionesActions.approveSuccess, (state, { aprobacion }) => ({
    ...state,
    items: [...state.items, aprobacion]
  })),
  on(AprobacionesActions.rejectSuccess, (state, { aprobacion }) => ({
    ...state,
    items: [...state.items, aprobacion]
  }))
);

export const selectAprobacionesState = createFeatureSelector<AprobacionesState>(APROBACIONES_FEATURE_KEY);
export const selectAllAprobaciones = createSelector(selectAprobacionesState, (s) => s.items);
export const selectAprobacionesLoading = createSelector(selectAprobacionesState, (s) => s.loading);
