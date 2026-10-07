/* F06y: weak_handlers.h - handlers debiles por defecto (trampa E02).
 *
 * El atributo __attribute__((weak)) permite que cualquier otro
 * archivo de la app (tipicamente board_*.c) sobreescriba el simbolo
 * con una definicion fuerte. En el linker, el simbolo fuerte gana.
 *
 * El default de Reset_Handler y de los demas handlers es un bucle
 * infinito, que es la convencion habitual en firmware embebido
 * para "el sistema se cuelga si llega aqui". La trampa paquete
 * P06 (weak_handler_loop_infinito) documenta este patron.
 */
#ifndef FXEMB_WEAK_HANDLERS_H
#define FXEMB_WEAK_HANDLERS_H

#include "vector_table.h"

/* Reset_Handler: punto de entrada tras reset. Llamado por el
 * hardware. Por defecto es weak; board_*.c lo sobreescribe. */
__attribute__((weak)) void Reset_Handler(void);

/* Handlers de excepcion del sistema. Por defecto, todos
 * caen en Default_Handler. */
__attribute__((weak)) void NMI_Handler(void);
__attribute__((weak)) void HardFault_Handler(void);

/* Default_Handler: cuando no se define un handler especifico
 * para una interrupcion. Queda en bucle infinito (trampa P06). */
__attribute__((weak)) void Default_Handler(void);

#endif
