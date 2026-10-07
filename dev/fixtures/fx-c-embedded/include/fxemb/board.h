/* F06y: board.h - seleccion de placa via #ifdef (trampa E05 del
 * ecosistema).
 *
 * El usuario compila con -DSTM32F4_DISCOVERY=1, -DNRF52_DK=1, o
 * -DBOARD_HOST=1 (default para tests). El header activa el resto
 * de includes y el startup.c incluye el board_<name>.c apropiado.
 *
 * Si no se define ninguna placa, se emite un #error para que el
 * build falle explicito (mejor que linkear con codigo vacio).
 */
#ifndef FXEMB_BOARD_H
#define FXEMB_BOARD_H

#include "version.h"

#if defined(STM32F4_DISCOVERY)
  #define FXEMB_BOARD_NAME "stm32f4_discovery"
  #define FXEMB_BOARD_HAS_UART1   1
  #define FXEMB_BOARD_HAS_ADC1    1
  #define FXEMB_BOARD_HAS_SLEEP   1
  #define FXEMB_BOARD_CLOCK_HZ    168000000UL
#elif defined(NRF52_DK)
  #define FXEMB_BOARD_NAME "nrf52_dk"
  #define FXEMB_BOARD_HAS_UART0   1
  #define FXEMB_BOARD_HAS_SAADC   1
  #define FXEMB_BOARD_HAS_SLEEP   1
  #define FXEMB_BOARD_CLOCK_HZ    64000000UL
#elif defined(BOARD_HOST) || defined(HOST_TEST)
  #define FXEMB_BOARD_NAME "host"
  #define FXEMB_BOARD_HAS_UART0   1
  #define FXEMB_BOARD_HAS_ADC0    1
  #define FXEMB_BOARD_HAS_SLEEP   0   /* host: no dormimos de verdad */
  #define FXEMB_BOARD_CLOCK_HZ    0
#else
  #error "FXEMB: ninguna placa seleccionada. Define -DSTM32F4_DISCOVERY=1, -DNRF52_DK=1, o -DBOARD_HOST=1."
#endif

#endif
