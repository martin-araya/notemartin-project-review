/* F06y: test_hal_volatile.c - 3 tests para las macros MMIO volatile (E06). */
#include "unity.h"
#include "fxemb/hal.h"

#include <stdio.h>
#include <string.h>

void setUp(void) {
    fxemb_hal_gpio_init();
}

void tearDown(void) {}

void test_hal_gpio_set_changes_output(void) {
    /* Set bit 0 -> 1, lectura debe ser 1. */
    fxemb_hal_gpio_set(0x01);
    TEST_ASSERT_EQUAL_INT(0x01, (int)fxemb_hal_gpio_read());
}

void test_hal_gpio_clear_clears_output(void) {
    fxemb_hal_gpio_set(0x01);
    fxemb_hal_gpio_set(0x02);
    fxemb_hal_gpio_clear(0x01);
    /* El bit 0 debe estar en 0, el bit 1 en 1. */
    TEST_ASSERT_EQUAL_INT(0x02, (int)fxemb_hal_gpio_read());
}

void test_hal_header_uses_volatile_qualifier(void) {
    /* Verificamos que hal.h usa volatile en sus macros MMIO. */
    char buf[4096];
    FILE* f = fopen("include/fxemb/hal.h", "r");
    if (!f) {
        TEST_FAIL_MESSAGE("include/fxemb/hal.h not found");
    }
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    /* Debe haber al menos 3 ocurrencias de volatile. */
    int count = 0;
    char* p = buf;
    while ((p = strstr(p, "volatile")) != NULL) {
        count++;
        p++;
    }
    TEST_ASSERT_GREATER_OR_EQUAL_INT(3, count);
}

int main(void) {
    UnityBegin("test_hal_volatile.c");
    RUN_TEST(test_hal_gpio_set_changes_output);
    RUN_TEST(test_hal_gpio_clear_clears_output);
    RUN_TEST(test_hal_header_uses_volatile_qualifier);
    return UnityEnd();
}
