/* F06y: board_host.c - implementacion de Reset_Handler para tests.
 *
 * E02: este archivo define Reset_Handler con linkage fuerte, lo que
 * hace que el linker prefiera este simbolo sobre el weak del
 * startup.c. El handler llama a fxemb_startup_for_host() que
 * inicializa y corre fxemb_main().
 */
#include "fxemb/vector_table.h"
#include "fxemb/board.h"

#include <stdint.h>

/* E02: sobreescribe el Reset_Handler weak. */
__attribute__((noreturn)) void Reset_Handler(void) {
    /* En bare-metal, copiamos .data desde FLASH a RAM, limpiamos
     * .bss, configuramos SP y llamamos a main. En host, el runtime
     * de C ya hizo todo eso; solo delegamos a fxemb_main(). */
    extern int fxemb_startup_for_host(void);
    (void)fxemb_startup_for_host();
    /* En host, fxemb_main retorna; en bare-metal, no deberia. */
    for (;;) { /* spin */ }
}

/* Board-specific: en host, exponemos una variable con el nombre
 * de la placa para que el ground truth la pueda leer. */
const char* fxemb_board_name_host = FXEMB_BOARD_NAME;
