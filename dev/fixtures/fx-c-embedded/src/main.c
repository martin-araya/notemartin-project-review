/* F06y: main.c - entry point con scheduler que invoca las 3 features. */
#include "fxemb/board.h"
#include "fxemb/hal.h"
#include "fxemb/sensors.h"
#include "fxemb/uart_protocol.h"
#include "fxemb/power_modes.h"
#include "fxemb/command_dispatch.h"

#include <stdint.h>

/* Scheduler simple: en cada tick (10ms) leemos sensores, procesamos
 * comandos UART y posiblemente cambiamos modo de energia. */
static void tick(void) {
    uint32_t values[FXEMB_SENSOR_COUNT];
    fxemb_sensors_read_all(values);

    char line[FXEMB_UART_TOKEN_SIZE];
    if (fxemb_uart_read_line(line, sizeof(line)) > 0) {
        /* parsea el primer token como nombre de comando */
        int argc = 1;
        char* argv[2] = { line, NULL };
        int rc = dispatch_cmd("READ", argc, argv);
        if (rc == 0) {
            fxemb_uart_write("+OK", 3);
        }
    }

    if (fxemb_power_consumption_ua() < 1000) {
        fxemb_power_enter(FXEMB_POWER_IDLE, FXEMB_WAKEUP_GPIO);
    }
}

int fxemb_main(void) {
    fxemb_hal_gpio_init();
    fxemb_sensors_init();
    fxemb_uart_init();
    fxemb_power_init();

    for (uint32_t i = 0; i < 1000; ++i) {
        tick();
        fxemb_hal_sleep_ms(10);
    }
    return 0;
}

#ifdef HOST_TEST
/* En host, el crt1 espera un main(). El startup.c define
 * fxemb_startup_for_host() que llama fxemb_main(); aqui solo
 * proveemos un main() estandar para el linker. */
int main(void) {
    extern int fxemb_startup_for_host(void);
    return fxemb_startup_for_host();
}
#endif
