/* F06y: vector_table.h - tabla de vectores de interrupcion estilo
 * ARM Cortex-M (trampa E01 del ecosistema).
 *
 * La tabla reside en la seccion .isr_vector (ver firmware.ld). El
 * primer elemento es el initial stack pointer; los siguientes son
 * punteros a funciones handler que el hardware invoca al ocurrir
 * una interrupcion.
 *
 * Para tests en host, el array se compila como datos ordinarios y
 * los tests verifican que los punteros apunten a las funciones
 * correctas. Para bare-metal, la seccion es la primera de FLASH y
 * el hardware la lee en reset.
 */
#ifndef FXEMB_VECTOR_TABLE_H
#define FXEMB_VECTOR_TABLE_H

#include <stdint.h>

/* Tipo de cada entrada de la tabla: un puntero a funcion que el
 * hardware llama sin argumentos y sin retorno. */
typedef void (*vector_t)(void);

/* Numero de entradas de la tabla. En un Cortex-M4 tipico son 16
 * IRQs del sistema + N IRQs externas; usamos 16 para mantener
 * el fixture simple. */
#define FXEMB_VECTOR_TABLE_SIZE 16

/* Tabla de vectores exportada. Se ubica en .isr_vector via la
 * declaracion __attribute__((section(".isr_vector"))) en
 * src/startup.c. */
extern const vector_t isr_vector[FXEMB_VECTOR_TABLE_SIZE];

/* Handlers debiles (trampa E02): el usuario puede sobreescribirlos
 * en board_*.c. Si ninguno los define, queda el default de
 * weak_handlers.h que es un while(1). */
extern void Reset_Handler(void);
extern void NMI_Handler(void);
extern void HardFault_Handler(void);
extern void Default_Handler(void);

#endif
