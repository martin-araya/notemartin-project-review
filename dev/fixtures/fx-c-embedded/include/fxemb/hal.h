/* F06y: hal.h - macros de acceso a registros MMIO (trampa E06 del
 * ecosistema).
 *
 * Cada macro apunta a una direccion fija que el linker script
 * (firmware.ld) reserva. Los punteros se declaran volatile para
 * que el compilador no reordene accesos a registros con efectos
 * secundarios (la trampa paquete P01 race_lectura_sensores se
 * manifiesta cuando los volatile estan mal aplicados).
 *
 * La trampa conceptual: si una macro se escribe con un cast que
 * elimina volatile (p.ej. (uint32_t*)0x40020014 sin volatile), el
 * compilador puede cachear el valor en un registro y los efectos
 * sobre el hardware real no se ven. Aqui todas las macros son
 * correctas; lo que se planta es la *apariencia* de complejidad
 * para que la skill verifique que la palabra volatile esta.
 */
#ifndef FXEMB_HAL_H
#define FXEMB_HAL_H

#include <stdint.h>

/* Direcciones tipicas para STM32F4 Discovery. */
#define FXEMB_GPIOA_BASE     0x40020000UL
#define FXEMB_GPIOA_ODR_OFFSET  0x14UL
#define FXEMB_GPIOA_IDR_OFFSET  0x10UL

#define FXEMB_RCC_BASE        0x40023800UL
#define FXEMB_RCC_AHB1ENR_OFFSET  0x30UL

/* Macros MMIO. volatile uint32_t* garantiza que cada lectura/escritura
 * toca la direccion real, sin optimizaciones del compilador. */
#define FXEMB_GPIOA_ODR (*(volatile uint32_t*)(FXEMB_GPIOA_BASE + FXEMB_GPIOA_ODR_OFFSET))
#define FXEMB_GPIOA_IDR (*(volatile uint32_t*)(FXEMB_GPIOA_BASE + FXEMB_GPIOA_IDR_OFFSET))
#define FXEMB_RCC_AHB1ENR (*(volatile uint32_t*)(FXEMB_RCC_BASE + FXEMB_RCC_AHB1ENR_OFFSET))

/* Bits de RCC_AHB1ENR para habilitar GPIOs. */
#define FXEMB_RCC_AHB1ENR_GPIOAEN  (1U << 0)

/* API de alto nivel. El usuario llama fxemb_hal_gpio_set() sin saber
 * la direccion exacta. */
void fxemb_hal_gpio_init(void);
void fxemb_hal_gpio_set(uint32_t pin_mask);
void fxemb_hal_gpio_clear(uint32_t pin_mask);
uint32_t fxemb_hal_gpio_read(void);

/* Lectura simulada de sensor (trampa P03 stub). */
uint32_t fxemb_hal_adc_read(uint8_t channel);

/* Microsegundos desde el reset (lo usa el scheduler). */
uint32_t fxemb_hal_micros(void);

/* Sleep de baja potencia (lo usa power_modes.c). */
void fxemb_hal_sleep_ms(uint32_t ms);

#endif
