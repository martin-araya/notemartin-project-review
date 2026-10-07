/* F06y: test_board_selection.c - 3 tests para la seleccion de placa (E05). */
#include "unity.h"
#include "fxemb/board.h"

#include <stdio.h>
#include <string.h>

void setUp(void) {}
void tearDown(void) {}

void test_board_header_defines_a_board_name(void) {
    /* BOARD_HOST o HOST_TEST debe estar definido en este test. */
    TEST_ASSERT_NOT_NULL(FXEMB_BOARD_NAME);
    TEST_ASSERT_GREATER_OR_EQUAL_INT(1, (int)strlen(FXEMB_BOARD_NAME));
}

void test_board_header_explicit_error_for_no_board(void) {
    /* El header debe tener un #error en la rama por defecto. */
    char buf[4096];
    FILE* f = fopen("include/fxemb/board.h", "r");
    TEST_ASSERT_NOT_NULL(f);
    size_t n = fread(buf, 1, sizeof(buf) - 1, f);
    buf[n] = '\0';
    fclose(f);
    TEST_ASSERT_NOT_NULL(strstr(buf, "#error"));
}

void test_board_host_name_is_host(void) {
    /* En HOST_TEST, FXEMB_BOARD_NAME debe ser "host". */
    TEST_ASSERT_EQUAL_STRING("host", FXEMB_BOARD_NAME);
}

int main(void) {
    UnityBegin("test_board_selection.c");
    RUN_TEST(test_board_header_defines_a_board_name);
    RUN_TEST(test_board_header_explicit_error_for_no_board);
    RUN_TEST(test_board_host_name_is_host);
    return UnityEnd();
}
