// Directiva estructural con setInterval. Trampa paquete #6:
// el setInterval nunca se limpia al destruir el componente
// (memory leak). La skill debe notar la falta del cleanup hook.
import { Directive, ElementRef, Input, OnInit } from '@angular/core';

@Directive({
  selector: '[fxContador]'
})
export class ContadorDirective implements OnInit {
  @Input() fxContador = 0;
  private intervalId: any = null;

  ngOnInit(): void {
    this.intervalId = setInterval(() => {
      this.fxContador += 1;
      if (this.host?.nativeElement) {
        this.host.nativeElement.setAttribute('data-count', String(this.fxContador));
      }
    }, 5000);
  }

  constructor(private host: ElementRef<HTMLElement>) {}
}
