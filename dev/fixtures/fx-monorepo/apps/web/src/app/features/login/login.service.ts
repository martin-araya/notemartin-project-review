// Servicio de autenticacion. Trampa de paquete #2: el observable no se
// desuscribe (el componente no implementa un cleanup hook), generando
// memory leak en apps de larga vida.

import type { Observable } from 'rxjs';

type LoginResponse = { token: string; user: { id: string; email: string } };

export class LoginService {
  private currentToken: string | null = null;
  private pendingLogin: Observable<LoginResponse> | null = null;

  // Trampa de paquete #2: no tenemos un hook de cleanup (sin operadores
  // de desuscripcion) para liberar ``pendingLogin``. Si el componente
  // se destruye durante la llamada, el observable sigue emitiendo.
  login(email: string, password: string): Observable<LoginResponse> {
    const observable = this.buildHttpCall(email, password);
    this.pendingLogin = observable;
    return observable;
  }

  private buildHttpCall(_email: string, _password: string): Observable<LoginResponse> {
    // Stub: en produccion esto hace ``this.http.post<LoginResponse>('/api/login', ...)``.
    return {
      subscribe: (observer: any) => {
        observer.next({ token: 'tok-stub', user: { id: 'u1', email: 'a@b.co' } });
        observer.complete();
      },
    } as any;
  }

  setToken(token: string | null): void {
    this.currentToken = token;
  }

  getToken(): string | null {
    return this.currentToken;
  }
}
