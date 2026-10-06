// Module file
// Formulario reactivo standalone. Dispara la action create.
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { SolicitudesActions } from '../store/actions';

@Component({
  selector: 'fx-nueva-solicitud',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <section>
      <h2>Nueva</h2>
      <form [formGroup]="form" (ngSubmit)="onSubmit()">
        <label>Nombre <input formControlName="nombre" /></label>
        <label>Monto <input formControlName="monto" type="number" /></label>
        <label>Premium <input formControlName="premium" type="checkbox" /></label>
        <button type="submit" [disabled]="form.invalid">Crear</button>
      </form>
    </section>
  `
})
export class NuevaSolicitudComponent {
  private fb = inject(FormBuilder);
  private store = inject(Store);
  private router = inject(Router);

  form: FormGroup = this.fb.group({
    nombre: ['', [Validators.required, Validators.minLength(1)]],
    monto: [0, [Validators.required, Validators.min(0)]],
    premium: [false]
  });

  onSubmit(): void {
    if (this.form.invalid) return;
    const v = this.form.value;
    this.store.dispatch(SolicitudesActions.create({
      payload: {
        nombre: v.nombre,
        monto: Number(v.monto),
        premium: v.premium === true,
        estado: 'pendiente',
        usuarioId: 'u-1'
      }
    }));
    this.router.navigateByUrl('/solicitudes');
  }
}
