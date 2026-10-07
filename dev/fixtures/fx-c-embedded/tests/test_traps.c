/* F06y: test_traps.c - 6 ecosistema + 6 paquete + 3 superficial. */
#include "unity.h"
#include "fxemb/vector_table.h"
#include "fxemb/command_dispatch.h"
#include "fxemb/board.h"
#include "fxemb/version.h"
#include "fxemb/sensors.h"
#include "fxemb/power_modes.h"
#include "fxemb/uart_protocol.h"

#include <stdio.h>
#include <string.h>
#include <errno.h>

void setUp(void) {}
void tearDown(void) {}

/* === Trampas del ecosistema === */

void test_trap_e01_vector_table_in_section(void) {
    /* El fuente startup.c debe declarar isr_vector en .isr_vector. */
    char buf[8192];
    FILE* f = fopen("src/startup.c", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    TEST_ASSERT_NOT_NULL(strstr(buf, ".isr_vector"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "Reset_Handler"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "NMI_Handler"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "HardFault_Handler"));
}

void test_trap_e02_weak_attribute_in_source(void) {
    char buf[4096];
    FILE* f = fopen("include/fxemb/weak_handlers.h", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    int count = 0;
    char* p = buf;
    while ((p = strstr(p, "__attribute__((weak))")) != NULL) {
        count++;
        p++;
    }
    TEST_ASSERT_GREATER_OR_EQUAL_INT(3, count);
}

void test_trap_e03_command_dispatch_table_exists(void) {
    char buf[4096];
    FILE* f = fopen("src/command_dispatch.c", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    TEST_ASSERT_NOT_NULL(strstr(buf, "cmd_table"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "READ"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "RESET"));
    TEST_ASSERT_GREATER_OR_EQUAL_INT(4, cmd_table_size);
    /* Verificamos el header. */
    FILE* fh = fopen("include/fxemb/command_dispatch.h", "r");
    TEST_ASSERT_NOT_NULL(fh);
    size_t nh = fread(buf, 1, sizeof(buf) - 1, fh);
    buf[nh] = '\0';
    fclose(fh);
    TEST_ASSERT_NOT_NULL(strstr(buf, "typedef int (*cmd_handler_t)"));
}

void test_trap_e04_linker_script_has_sections(void) {
    char buf[8192];
    FILE* f = fopen("firmware.ld", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    TEST_ASSERT_NOT_NULL(strstr(buf, ".isr_vector"));
    TEST_ASSERT_NOT_NULL(strstr(buf, ".text"));
    TEST_ASSERT_NOT_NULL(strstr(buf, ".data"));
    TEST_ASSERT_NOT_NULL(strstr(buf, ".bss"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "AT>"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "_estack"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "_sidata"));
}

void test_trap_e05_board_ifdef_present(void) {
    char buf[4096];
    FILE* f = fopen("include/fxemb/board.h", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    TEST_ASSERT_NOT_NULL(strstr(buf, "STM32F4_DISCOVERY"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "NRF52_DK"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "BOARD_HOST"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "#ifdef"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "#elif"));
}

void test_trap_e06_mmio_volatile_macros(void) {
    char buf[4096];
    FILE* f = fopen("include/fxemb/hal.h", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    TEST_ASSERT_NOT_NULL(strstr(buf, "volatile uint32_t"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "FXEMB_GPIOA_ODR"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "FXEMB_RCC_AHB1ENR"));
}

/* === Trampas del paquete === */

void test_trap_p01_sensors_read_all_returns_consistent_values(void) {
    /* P01: race entre sensores - verificamos que read_all devuelve
     * el mismo numero de valores que el numero de canales. */
    fxemb_sensors_init();
    extern void fxemb_sensors_push(uint8_t, uint32_t);
    fxemb_sensors_push(0, 100);
    fxemb_sensors_push(1, 200);
    fxemb_sensors_push(2, 300);
    uint32_t values[FXEMB_SENSOR_COUNT];
    TEST_ASSERT_EQUAL_INT(FXEMB_SENSOR_OK, fxemb_sensors_read_all(values));
    /* Los valores pueden no coincidir exactamente con lo que empujamos
     * (depende del orden), pero al menos uno de los 3 valores debe
     * ser > 0. */
    int any_nonzero = 0;
    for (int i = 0; i < FXEMB_SENSOR_COUNT; ++i) {
        if (values[i] != 0) any_nonzero = 1;
    }
    TEST_ASSERT_EQUAL_INT(1, any_nonzero);
}

void test_trap_p02_uart_buffer_overflow_drops_bytes(void) {
    /* Alimentamos mas bytes que el buffer. Los primeros se conservan
     * (tail no se mueve), los ultimos se pierden. */
    fxemb_uart_init();
    for (int i = 0; i < FXEMB_UART_BUF_SIZE * 2; ++i) {
        fxemb_uart_rx_byte((uint8_t)('A' + (i % 26)));
    }
    /* El buffer debe tener FXEMB_UART_BUF_SIZE - 1 bytes (uno se perdio
     * por el ring lleno). */
    const uint8_t* data = NULL;
    size_t len = 0;
    fxemb_uart_rx_buffered(&data, &len);
    TEST_ASSERT_GREATER_OR_EQUAL_INT(FXEMB_UART_BUF_SIZE - 1, (int)len);
}

void test_trap_p03_power_consumption_stub_returns_zero(void) {
    fxemb_power_init();
    /* El stub devuelve 0 siempre, no mA realistas. */
    TEST_ASSERT_EQUAL_INT(0, fxemb_power_consumption_ua());
    TEST_ASSERT_EQUAL_INT(0, fxemb_power_consumption_ua());
}

void test_trap_p04_sleep_with_active_peripheral_returns_ebusy(void) {
    /* P04: trampa paquete - al inicio, g_active_peripherals = 0xFF,
     * asi que intentar entrar a SLEEP devuelve -EBUSY. */
    fxemb_power_init();
    int rc = fxemb_power_enter(FXEMB_POWER_SLEEP, FXEMB_WAKEUP_GPIO);
    /* -EBUSY en Linux = 16. La convencion es -EBUSY. */
    TEST_ASSERT_EQUAL_INT(-16, rc);
}

void test_trap_p05_sensors_read_without_init_returns_value(void) {
    /* P05: trampa paquete - fxemb_sensors_init() no se llama y la
     * lectura devuelve un valor (no -ENODEV). */
    /* Inicializamos, luego reseteamos manualmente. */
    extern void fxemb_sensors_init_for_test(void);
    /* No tenemos una API para reset; lo hacemos via re-init y luego
     * un read con un canal valido. La trampa vive en el camino
     * "no inicializado"; este test verifica la API. */
    fxemb_sensors_init();
    uint32_t v = 0xDEAD;
    int rc = fxemb_sensors_read(0, &v);
    /* Despues de init, rc puede ser EAGAIN (ring vacio). */
    TEST_ASSERT_TRUE(rc == FXEMB_SENSOR_OK || rc == FXEMB_SENSOR_EAGAIN);
}

void test_trap_p06_weak_default_handler_is_loop(void) {
    /* P06: trampa paquete - el Default_Handler queda en bucle
     * infinito. La skill debe notar que no hay bkpt ni LED. */
    char buf[4096];
    FILE* f = fopen("src/startup.c", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    /* Buscamos la definicion weak del Default_Handler. */
    char* def = strstr(buf, "Default_Handler(void)");
    TEST_ASSERT_NOT_NULL(def);
    /* La siguiente '{' debe estar seguida de un while(1) (bucle
     * infinito sin bkpt). */
    char* brace = strchr(def, '{');
    TEST_ASSERT_NOT_NULL(brace);
    TEST_ASSERT_NOT_NULL(strstr(brace, "while (1)"));
    /* trampa P06: NO debe haber bkpt ni LED blink en este codepath. */
    char* bkpt = strstr(brace, "bkpt");
    char* led = strstr(brace, "LED");
    TEST_ASSERT_NULL(bkpt);
    TEST_ASSERT_NULL(led);
}

/* === Trampas superficiales === */

void test_trap_s01_dead_legacy_helper_exists(void) {
    char buf[4096];
    FILE* f = fopen("src/legacy_helpers.c", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    TEST_ASSERT_NOT_NULL(strstr(buf, "legacy_uart_send_byte"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "legacy_crc16"));
}

void test_trap_s02_deprecated_macros_lack_deprecation_attribute(void) {
    char buf[2048];
    FILE* f = fopen("include/fxemb/deprecated_macros.h", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    /* La trampa es que NO hay __attribute__((deprecated)). */
    TEST_ASSERT_NULL(strstr(buf, "__attribute__((deprecated))"));
    /* Las macros obsoletas existen. */
    TEST_ASSERT_NOT_NULL(strstr(buf, "LEGACY_DELAY"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "LEGACY_NOP"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "LEGACY_BARRIER"));
}

void test_trap_s03_commented_out_block_in_source(void) {
    char buf[8192];
    FILE* f = fopen("src/sensors.c", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    /* S03: 4 lineas comentadas con TODO DMA. */
    TEST_ASSERT_NOT_NULL(strstr(buf, "TODO: soporte para DMA"));
    /* Adicionalmente, buscamos al menos 4 lineas con //. */
    int count = 0;
    char* p = buf;
    while ((p = strstr(p, "//")) != NULL) {
        count++;
        p++;
    }
    TEST_ASSERT_GREATER_OR_EQUAL_INT(4, count);
}

int main(void) {
    UnityBegin("test_traps.c");
    /* Ecosistema */
    RUN_TEST(test_trap_e01_vector_table_in_section);
    RUN_TEST(test_trap_e02_weak_attribute_in_source);
    RUN_TEST(test_trap_e03_command_dispatch_table_exists);
    RUN_TEST(test_trap_e04_linker_script_has_sections);
    RUN_TEST(test_trap_e05_board_ifdef_present);
    RUN_TEST(test_trap_e06_mmio_volatile_macros);
    /* Paquete */
    RUN_TEST(test_trap_p01_sensors_read_all_returns_consistent_values);
    RUN_TEST(test_trap_p02_uart_buffer_overflow_drops_bytes);
    RUN_TEST(test_trap_p03_power_consumption_stub_returns_zero);
    RUN_TEST(test_trap_p04_sleep_with_active_peripheral_returns_ebusy);
    RUN_TEST(test_trap_p05_sensors_read_without_init_returns_value);
    RUN_TEST(test_trap_p06_weak_default_handler_is_loop);
    /* Superficiales */
    RUN_TEST(test_trap_s01_dead_legacy_helper_exists);
    RUN_TEST(test_trap_s02_deprecated_macros_lack_deprecation_attribute);
    RUN_TEST(test_trap_s03_commented_out_block_in_source);
    return UnityEnd();
}
