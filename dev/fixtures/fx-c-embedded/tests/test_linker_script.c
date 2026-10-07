/* F06y: test_linker_script.c - 3 tests para el linker script (E04). */
#include "unity.h"
#include "fxemb/vector_table.h"

#include <stdio.h>
#include <string.h>

void setUp(void) {}
void tearDown(void) {}

void test_linker_script_exists(void) {
    FILE* f = fopen("firmware.ld", "r");
    TEST_ASSERT_NOT_NULL(f);
    fclose(f);
}

void test_linker_script_contains_isr_vector_section(void) {
    char buf[8192];
    FILE* f = fopen("firmware.ld", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    TEST_ASSERT_NOT_NULL(strstr(buf, ".isr_vector"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "KEEP(*(.isr_vector))"));
}

void test_linker_script_exports_estack(void) {
    char buf[8192];
    FILE* f = fopen("firmware.ld", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    TEST_ASSERT_NOT_NULL(strstr(buf, "_estack"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "_sidata"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "_sbss"));
    TEST_ASSERT_NOT_NULL(strstr(buf, "_ebss"));
}

int main(void) {
    UnityBegin("test_linker_script.c");
    RUN_TEST(test_linker_script_exists);
    RUN_TEST(test_linker_script_contains_isr_vector_section);
    RUN_TEST(test_linker_script_exports_estack);
    return UnityEnd();
}
