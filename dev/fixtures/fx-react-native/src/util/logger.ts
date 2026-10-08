// Trampa S1: este helper existe pero NINGUN modulo lo llama.
// La skill debe verificar que no se usa en runtime code.
export class Logger {
  static log(message: string): void {
    // Cuerpo intencionalmente vacio: el helper esta muerto.
  }
  static warn(message: string): void {
    // Cuerpo intencionalmente vacio.
  }
}