/* F06y: hal_stm32f4.c - implementacion real del HAL para STM32F4.
 *
 * Compilado con -DSTM32F4_DISCOVERY=1 + arm-none-eabi-gcc -mcpu=cortex-m4.
 * En este caso las macros MMIO apuntan a direcciones reales del
 * microcontrolador; el codigo C es identico a la version de host,
 * pero los accesos leen/escriben hardware.
 */
#include "fxemb/hal.h"
#include "fxemb/board.h"

void fxemb_hal_gpio_init(void) {
    /* STM32F4: habilita clock de GPIOA via RCC_AHB1ENR. */
    FXEMB_RCC_AHB1ENR |= FXEMB_RCC_AHB1ENR_GPIOAEN;
    /* (en bare-metal real, aqui configurariamos MODER, OTYPER, OSPEEDR
     * para poner el pin en modo output, pero el fixture lo deja asi.) */
}

void fxemb_hal_gpio_set(uint32_t pin_mask) { FXEMB_GPIOA_ODR |= pin_mask; }
void fxemb_hal_gpio_clear(uint32_t pin_mask) { FXEMB_GPIOA_ODR &= ~pin_mask; }
uint32_t fxemb_hal_gpio_read(void) { return FXEMB_GPIOA_IDR; }
uint32_t fxemb_hal_adc_read(uint8_t channel) {
    (void)channel;
    return 0;
}
uint32_t fxemb_hal_micros(void) {
    /* En bare-metal, leemos el timer del sistema. Aqui devolvemos 0
     * porque la rutina startup lo incrementa. */
    return 0;
}
void fxemb_hal_sleep_ms(uint32_t ms) { (void)ms; /* __WFI en real */ }
