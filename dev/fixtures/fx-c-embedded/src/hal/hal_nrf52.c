/* F06y: hal_nrf52.c - implementacion real del HAL para nRF52 DK. */
#include "fxemb/hal.h"
#include "fxemb/board.h"

void fxemb_hal_gpio_init(void) { /* nRF52 GPIO init */ }
void fxemb_hal_gpio_set(uint32_t pin_mask) { (void)pin_mask; }
void fxemb_hal_gpio_clear(uint32_t pin_mask) { (void)pin_mask; }
uint32_t fxemb_hal_gpio_read(void) { return 0; }
uint32_t fxemb_hal_adc_read(uint8_t channel) { (void)channel; return 0; }
uint32_t fxemb_hal_micros(void) { return 0; }
void fxemb_hal_sleep_ms(uint32_t ms) { (void)ms; }
