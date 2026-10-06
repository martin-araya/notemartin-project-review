// src/app/core/interceptors/logging.interceptor.ts
// HTTP_INTERCEPTORS con multi: true. Loguea cada peticion y
// respuesta. El orden de declaracion (auth primero, logging
// despues) importa: si se invierte, logging ve el header
// Authorization sin el Bearer ya agregado por auth.
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const started = Date.now();
    return next.handle(req).pipe(
      tap((event) => {
        if (event instanceof HttpResponse) {
          // eslint-disable-next-line no-console
          console.log('[fx-http]', req.method, req.url, '->', event.status, 'in', Date.now() - started, 'ms');
        }
      })
    );
  }
}
