// Componente con signals. Trampa del ecosistema #4: usa ``effect()`` que
// dispara una llamada HTTP cuando cambia el signal ``token``.
//
// Trampa de paquete #2: el effect nunca se limpia (sin ``DestroyRef``).

export class LoginPage {
  static readonly name = 'LoginPage';

  // signals: username, password, token
  username = '';
  password = '';
  token: string | null = null;
  loading = false;
  error: string | null = null;

  // effect() se ejecuta cuando cambia token. Dispara un GET a /api/login/me.
  // En el fixture, el effect solo emite un log; en produccion haria HTTP.
  effectRef: (() => void) | null = null;

  attachEffect(): void {
    // Trampa del ecosistema #4: el effect() depende de ``token``. Trampa
    // de paquete #2: nunca se desuscribe (no hay DestroyRef).
    this.effectRef = () => {
      if (this.token) {
        // En produccion: ``this.http.get('/api/login/me', { headers: ... })``
        // eslint-disable-next-line no-console
        console.log('[effect] token changed, would GET /api/login/me');
      }
    };
    this.effectRef();
  }

  submit(): void {
    if (!this.username || !this.password) {
      this.error = 'missing_credentials';
      return;
    }
    this.loading = true;
    // Stub: en produccion, ``this.loginService.login(...)``.
    this.token = 'tok-' + this.username;
    this.attachEffect();
    this.loading = false;
  }
}
