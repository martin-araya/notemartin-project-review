// Module file
import { NgModule } from '@angular/core';
import { ReportesComponent } from './pages/reportes.component';
import { REPORTES_ROUTES } from './reportes.routes';
import { RouterModule } from '@angular/router';

@NgModule({
  imports: [RouterModule.forChild(REPORTES_ROUTES), ReportesComponent],
  exports: [RouterModule]
})
export class ReportesModule {}
