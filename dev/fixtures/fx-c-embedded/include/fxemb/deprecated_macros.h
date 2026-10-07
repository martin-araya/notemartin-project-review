/* F06y: deprecated_macros.h - S02 trampa superficial.
 *
 * Tres macros obsoletas sin marca de deprecation. C99 no soporta
 * el atributo de C++ ni la forma textual usada en C++; en C la
 * convencion es usar la extension de GCC/clang. Este header no
 * usa esa extension a proposito.
 */
#ifndef FXEMB_DEPRECATED_MACROS_H
#define FXEMB_DEPRECATED_MACROS_H

/* Macros obsoletas. La trampa S02 es que no llevan la marca estandar
 * de deprecation de C y el codigo de la app puede seguirlas usando
 * sin warning. */

/* LEGACY_DELAY: bucle de espera activa. */
#define LEGACY_DELAY(ticks)  do { volatile int _i = 0; while (_i++ < (ticks)) {} } while (0)

/* LEGACY_NOP: no-op. */
#define LEGACY_NOP()         do { int _x = 0; (void)_x; } while (0)

/* LEGACY_BARRIER: memory barrier. */
#define LEGACY_BARRIER()     __asm__ __volatile__("" ::: "memory")

#endif
