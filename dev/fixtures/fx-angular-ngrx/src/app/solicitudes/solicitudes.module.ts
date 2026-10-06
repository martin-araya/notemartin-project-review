// Module file
// NgModule con forChild: provee el feature state y los effects.
// Se importa en app.config.ts via importProvidersFrom.
import { NgModule } from '@angular/core';
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { SOLICITUDES_FEATURE_KEY, SolicitudesState } from './store/state';
import { reducer } from './store/reducer';
import { SolicitudesEffects } from './store/effects';

@NgModule({
  imports: [
    StoreModule.forFeature<SolicitudesState>(SOLICITUDES_FEATURE_KEY, reducer),
    EffectsModule.forFeature([SolicitudesEffects])
  ]
})
export class SolicitudesModule {}
