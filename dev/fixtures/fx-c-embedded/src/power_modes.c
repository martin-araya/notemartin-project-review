/* F06y: power_modes.c - feature 3: maquina de estados de energia. */
#include "fxemb/power_modes.h"
#include "fxemb/hal.h"

#include <errno.h>

#include <stdint.h>

static fxemb_power_mode_t g_current_mode = FXEMB_POWER_RUN;
static fxemb_wakeup_source_t g_wakeup_source = FXEMB_WAKEUP_NONE;
static int g_wakeup_pending = 0;
static int g_power_initialized = 0;
static int g_active_peripherals = 0xFF;  /* bitmask */

int fxemb_power_init(void) {
    g_current_mode = FXEMB_POWER_RUN;
    g_wakeup_source = FXEMB_WAKEUP_NONE;
    g_wakeup_pending = 0;
    g_active_peripherals = 0xFF;
    g_power_initialized = 1;
    return 0;
}

int fxemb_power_enter(fxemb_power_mode_t mode, fxemb_wakeup_source_t wakeup) {
    if (!g_power_initialized) return -ENODEV;
    if (mode == FXEMB_POWER_DEEPSLEEP && wakeup == FXEMB_WAKEUP_NONE) {
        return -EINVAL;  /* R-05: no se puede deepsleep sin wakeup source */
    }
    /* trampa paquete P04 (sleep_lock_olvidado): no tomamos un mutex
     * antes de cambiar de modo, asi una IRQ puede entrar a un estado
     * inconsistente. */
    if (mode == FXEMB_POWER_SLEEP && (g_active_peripherals & 0x01)) {
        return -EBUSY;  /* R-04: periferico activo bloquea */
    }
    g_current_mode = mode;
    g_wakeup_source = wakeup;
    return 0;
}

int fxemb_power_current_mode(void) { return (int)g_current_mode; }

int fxemb_power_wakeup_pending(void) { return g_wakeup_pending; }

int fxemb_power_clear_wakeup(void) { g_wakeup_pending = 0; return 0; }

int fxemb_power_consumption_ua(void) {
    if (!g_power_initialized) return 0;
    /* trampa paquete P03 (consumo_stub_irreal): siempre devolvemos 0
     * en lugar de un valor realista. La skill debe notar que la HAL
     * no mide corriente en absoluto. */
    return 0;
}

/* API para que las IRQs marquen wakeup pending. */
void fxemb_power_set_wakeup_pending(fxemb_wakeup_source_t src) {
    (void)src;
    g_wakeup_pending = 1;
}
