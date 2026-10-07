/* F06y: test_vector_table.c - 3 tests para la tabla de vectores (E01). */
#include "unity.h"
#include "fxemb/vector_table.h"

void setUp(void) {}
void tearDown(void) {}

void test_vector_table_size_is_16(void) {
    TEST_ASSERT_EQUAL_INT(16, FXEMB_VECTOR_TABLE_SIZE);
}

void test_vector_table_initial_sp_is_at_top_of_ram(void) {
    /* El primer slot de la tabla debe ser 0x20020000 (top de RAM STM32F4). */
    uintptr_t sp = (uintptr_t)isr_vector[0];
    TEST_ASSERT_EQUAL_INT(0x20020000, (int)sp);
}

void test_vector_table_reset_handler_is_nonzero(void) {
    /* Reset_Handler debe ser un puntero valido (no NULL). */
    uintptr_t reset = (uintptr_t)isr_vector[1];
    TEST_ASSERT_NOT_NULL((void*)reset);
}

int main(void) {
    UnityBegin("test_vector_table.c");
    RUN_TEST(test_vector_table_size_is_16);
    RUN_TEST(test_vector_table_initial_sp_is_at_top_of_ram);
    RUN_TEST(test_vector_table_reset_handler_is_nonzero);
    return UnityEnd();
}
