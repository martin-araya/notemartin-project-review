/* F06y: command_dispatch.h - dispatch de comandos por tabla de
 * punteros a funcion (trampa E03 del ecosistema).
 *
 * Cada comando UART (AT+READ?, AT+RESET, etc.) tiene un handler
 * asociado. La tabla indexa por nombre de comando.
 *
 * Esto NO es un string-dispatch: se indexa por el campo cmd_name
 * (char*). Si la skill busca el handler por nombre, debe iterar
 * la tabla. Eso es la trampa: parece una lookup O(1) pero es O(n)
 * lineal porque el campo cmd_name se compara con strcmp.
 */
#ifndef FXEMB_COMMAND_DISPATCH_H
#define FXEMB_COMMAND_DISPATCH_H

#include <stdint.h>

/* Firma del handler: recibe argc/argv al estilo main, retorna
 * un codigo (0 = ok, negativo = -errno). */
typedef int (*cmd_handler_t)(int argc, char** argv);

/* Entrada de la tabla: nombre, handler, descripcion para ayuda. */
typedef struct {
    const char*  cmd_name;
    cmd_handler_t handler;
    const char*  description;
} cmd_dispatch_t;

/* Tabla exportada. Se define en src/command_dispatch.c. */
extern const cmd_dispatch_t cmd_table[];
extern const int cmd_table_size;

/* API: dispatch_cmd busca el handler por nombre. */
int dispatch_cmd(const char* name, int argc, char** argv);

#endif
