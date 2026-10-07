/* F06y: board_stm32f4.c - Reset_Handler para STM32F4 Discovery. */
#include "fxemb/vector_table.h"

#include <stdint.h>

extern int main(void);

__attribute__((noreturn)) void Reset_Handler(void) {
    /* En bare-metal real: copia .data, limpia .bss, llama a main.
     * En este fixture simplificado solo delegamos. */
    (void)main();
    for (;;) { /* spin */ }
}
