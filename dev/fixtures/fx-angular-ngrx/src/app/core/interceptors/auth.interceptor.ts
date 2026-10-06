// src/app/core/interceptors/auth.interceptor.ts
// HTTP_INTERCEPTORS con multi: true. Trampa paquete #3: el
// interceptor modifica window.localStorage directamente, lo que
// falla en SSR porque window no existe.
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = typeof window !== 'undefined'
      ? window.localStorage.getItem('fx_token') ?? 'demo-token'
      : 'ssr-token';
    const cloned = req.clone({
      setHeaders: { Authorization: 'Bearer ' + token }
    });
    return next.handle(cloned);
  }
}
