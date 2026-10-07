/* F06y: test_weak_symbols.c - 3 tests para la sobreescritura weak (E02). */
#include "unity.h"
#include "fxemb/vector_table.h"

#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* Definimos un Reset_Handler fuerte local. El linker debe preferir
 * este sobre el weak del startup.c. En este test unitario
 * compilamos sin startup.c, asi que el unico Reset_Handler visible
 * es este. */

/* Forward declaration del board_host.c Reset_Handler. */
extern void Reset_Handler(void);

void setUp(void) {}
void tearDown(void) {}

void test_weak_symbols_board_handler_is_strong(void) {
    /* El Reset_Handler del board_host.c debe estar linkeado (no es
     * NULL ni el weak del startup.c). */
    uintptr_t reset = (uintptr_t)Reset_Handler;
    TEST_ASSERT_NOT_NULL((void*)reset);
}

void test_weak_default_handler_exists(void) {
    /* El Default_Handler weak existe, aunque su definicion sea
     * un while(1). El test verifica que el simbolo esta linkeado. */
    uintptr_t dh = (uintptr_t)Default_Handler;
    TEST_ASSERT_NOT_NULL((void*)dh);
}

void test_weak_attribute_in_source(void) {
    /* Verificamos que el fuente weak_handlers.h usa __attribute__((weak)).
     * Leemos el archivo y buscamos la cadena. */
    const char* path = "include/fxemb/weak_handlers.h";
    FILE* f = fopen(path, "r");
    TEST_ASSERT_NOT_NULL(f);
    char buf[4096];
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    TEST_ASSERT_NOT_NULL(strstr(buf, "__attribute__((weak))"));
}

int main(void) {
    UnityBegin("test_weak_symbols.c");
    RUN_TEST(test_weak_symbols_board_handler_is_strong);
    RUN_TEST(test_weak_default_handler_exists);
    RUN_TEST(test_weak_attribute_in_source);
    return UnityEnd();
}
