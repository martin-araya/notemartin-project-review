/* F06y: board_nrf52.c - Reset_Handler para nRF52 DK. */
#include "fxemb/vector_table.h"

extern int main(void);

__attribute__((noreturn)) void Reset_Handler(void) {
    (void)main();
    for (;;) { /* spin */ }
}
