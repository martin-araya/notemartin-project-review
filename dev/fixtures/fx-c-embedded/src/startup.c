/* F06y: startup.c - vector table initialization + handlers debiles.
 *
 * E01: tabla de vectores en .isr_vector (ver vector_table.h).
 * E02: handlers por defecto son __attribute__((weak)).
 */
#include "fxemb/vector_table.h"
#include "fxemb/weak_handlers.h"
#include "fxemb/board.h"
#include "fxemb/version.h"

#include <stdint.h>

/* E01: tabla de vectores. Ubicada en .isr_vector via atributo
 * del section. El primer elemento es el initial SP (lo llena el
 * linker con _estack). */
__attribute__((section(".isr_vector")))
const vector_t isr_vector[FXEMB_VECTOR_TABLE_SIZE] = {
    (vector_t)(0x20020000UL),  /* 0: Initial SP (top de RAM, tipico). */
    Reset_Handler,             /* 1: Reset. */
    NMI_Handler,               /* 2: NMI. */
    HardFault_Handler,         /* 3: Hard fault. */
    Default_Handler,           /* 4: MemManage. */
    Default_Handler,           /* 5: BusFault. */
    Default_Handler,           /* 6: UsageFault. */
    0, 0, 0, 0,               /* 7-10: Reservados. */
    Default_Handler,           /* 11: SVCall. */
    Default_Handler,           /* 12: Debug Monitor. */
    0,                          /* 13: Reservado. */
    Default_Handler,           /* 14: PendSV. */
    Default_Handler,           /* 15: SysTick. */
};

/* E02: definiciones debiles por defecto. Si board_*.c define
 * Reset_Handler, el linker descarta estas. */
__attribute__((weak)) void Reset_Handler(void) { while (1) { } }
__attribute__((weak)) void NMI_Handler(void)     { while (1) { } }
__attribute__((weak)) void HardFault_Handler(void) { while (1) { } }
__attribute__((weak)) void Default_Handler(void)   { while (1) { } }

/* En host (HOST_TEST), el startup es llamado desde main; en
 * bare-metal, es el punto de entrada tras reset. */
#ifdef HOST_TEST
extern int fxemb_main(void);
/* Stub debil para que los tests que no incluyen main.c no fallen
 * al linkear. Si main.c esta presente, su fxemb_main() fuerte
 * sobreescribe este. */
__attribute__((weak)) int fxemb_main(void) { return 0; }
int fxemb_startup_for_host(void) {
    /* En host, no copiamos .data desde FLASH; los globales ya estan
     * en RAM. Tampoco limpiamos .bss; el startup lo hace el runtime de C. */
    return fxemb_main();
}
#endif
