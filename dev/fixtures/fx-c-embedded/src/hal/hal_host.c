/* F06y: hal_host.c - implementacion del HAL para tests en host.
 *
 * Reemplaza el acceso a registros MMIO con memoria global. Esto
 * permite que el codigo que usa las macros FXEMB_GPIOA_ODR, etc.
 * corra en x86 sin hardware.
 */
#include "fxemb/hal.h"
#include "fxemb/board.h"

#include <stdint.h>

/* Registros simulados como memoria global. La trampa paquete P03
 * (consumo_stub_irreal) vive aqui: reportamos 0 mA siempre. */
static uint32_t g_gpioa_odr = 0;
static uint32_t g_gpioa_idr = 0;
static uint32_t g_rcc_ahb1enr = 0;
static uint32_t g_micros_counter = 0;
static uint8_t  g_adc_channels[8] = { 25, 50, 75, 100, 125, 150, 175, 200 };

/* Definiciones de los registros: el archivo compila contra las macros
 * que vimos antes; pero como estamos en host, redefinimos los punteros
 * para apuntar a la memoria global. */
#ifdef HOST_TEST
/* Truco: en host, las macros MMIO se reemplazan por accesos a las
 * variables globales de este archivo. */
#undef FXEMB_GPIOA_ODR
#undef FXEMB_GPIOA_IDR
#undef FXEMB_RCC_AHB1ENR
volatile uint32_t FXEMB_GPIOA_ODR = 0;
volatile uint32_t FXEMB_GPIOA_IDR = 0;
volatile uint32_t FXEMB_RCC_AHB1ENR = 0;
#endif

void fxemb_hal_gpio_init(void) {
    /* Habilita el clock del GPIOA. */
    FXEMB_RCC_AHB1ENR |= FXEMB_RCC_AHB1ENR_GPIOAEN;
}

void fxemb_hal_gpio_set(uint32_t pin_mask) {
    FXEMB_GPIOA_ODR |= pin_mask;
}

void fxemb_hal_gpio_clear(uint32_t pin_mask) {
    FXEMB_GPIOA_ODR &= ~pin_mask;
}

uint32_t fxemb_hal_gpio_read(void) {
    /* En el stub de host, leemos el ODR (output) directamente; en
     * hardware real, IDR y ODR son registros distintos y depende
     * del modo (input vs output) del pin. La trampa paquete P01
     * (race_lectura_sensores) se manifestaria si ODR se leyera
     * desde un thread mientras otro escribe via fxemb_hal_gpio_set. */
    return FXEMB_GPIOA_ODR;
}

uint32_t fxemb_hal_adc_read(uint8_t channel) {
    if (channel >= 8) return 0xFFFFFFFFu;
    return (uint32_t)g_adc_channels[channel] * 10u;
}

uint32_t fxemb_hal_micros(void) {
    return g_micros_counter;
}

void fxemb_hal_sleep_ms(uint32_t ms) {
    /* En host, simulamos el tiempo incrementando el contador.
     * trampa paquete P03: este stub no duerme nada, solo avanza el
     * reloj simulado. */
    g_micros_counter += ms * 1000u;
}
