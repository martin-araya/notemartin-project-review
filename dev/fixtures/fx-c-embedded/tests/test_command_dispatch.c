/* F06y: test_command_dispatch.c - 4 tests para la tabla de dispatch (E03). */
#include "unity.h"
#include "fxemb/command_dispatch.h"
#include <errno.h>
#include <string.h>

void setUp(void) {}
void tearDown(void) {}

void test_dispatch_table_has_at_least_4_entries(void) {
    TEST_ASSERT_TRUE(cmd_table_size >= 4);
    TEST_ASSERT_NOT_NULL(cmd_table);
}

void test_dispatch_read_succeeds(void) {
    char arg0[] = "READ";
    char* argv[] = { arg0, NULL };
    int argc = 1;
    TEST_ASSERT_EQUAL_INT(0, dispatch_cmd("READ", argc, argv));
}

void test_dispatch_unknown_returns_einval(void) {
    char arg0[] = "FOOBAR";
    char* argv[] = { arg0, NULL };
    TEST_ASSERT_EQUAL_INT(-EINVAL, dispatch_cmd("FOOBAR", 1, argv));
}

void test_dispatch_table_contains_reset(void) {
    int found = 0;
    for (int i = 0; i < cmd_table_size; ++i) {
        if (strcmp(cmd_table[i].cmd_name, "RESET") == 0) {
            found = 1;
            break;
        }
    }
    TEST_ASSERT_EQUAL_INT(1, found);
}

int main(void) {
    UnityBegin("test_command_dispatch.c");
    RUN_TEST(test_dispatch_table_has_at_least_4_entries);
    RUN_TEST(test_dispatch_read_succeeds);
    RUN_TEST(test_dispatch_unknown_returns_einval);
    RUN_TEST(test_dispatch_table_contains_reset);
    return UnityEnd();
}
