// Module file
import { NgModule } from '@angular/core';
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { APROBACIONES_FEATURE_KEY, AprobacionesState } from './store/state';
import { reducer } from './store/reducer';
import { AprobacionesEffects } from './store/effects';

@NgModule({
  imports: [
    StoreModule.forFeature<AprobacionesState>(APROBACIONES_FEATURE_KEY, reducer),
    EffectsModule.forFeature([AprobacionesEffects])
  ]
})
export class AprobacionesModule {}
