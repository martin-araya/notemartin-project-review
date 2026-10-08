// Trampa S1: helper Logger con print que nunca se invoca desde el codigo
// de runtime. La skill debe notar que no hay `Logger.print(...)` en lib/.
class Logger {
  static void print(String message) {
    // La trampa intencional es que este helper existe pero no se usa.
    // debugPrint iria aqui si fuera necesario; intencionalmente vacio.
  }
}