/**
 * Trampa S1: helper declarado pero NO invocado en runtime.
 * La skill debe verificar que no se usa en codigo de runtime.
 */
export class LegacyLogger {
  static info(message: string): void {
    // Cuerpo intencionalmente vacio: el helper esta muerto.
  }
  static warn(message: string): void {
    // Cuerpo intencionalmente vacio.
  }
  static error(message: string): void {
    // Cuerpo intencionalmente vacio.
  }
}