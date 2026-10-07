/* F06y: test_power_modes.c - 4 tests para feature 3. */
#include "unity.h"
#include "fxemb/power_modes.h"
#include <errno.h>

void setUp(void) { fxemb_power_init(); }
void tearDown(void) {}

void test_power_init_starts_in_run_mode(void) {
    TEST_ASSERT_EQUAL_INT(FXEMB_POWER_RUN, fxemb_power_current_mode());
    TEST_ASSERT_EQUAL_INT(0, fxemb_power_wakeup_pending());
}

void test_power_enter_idle_succeeds(void) {
    TEST_ASSERT_EQUAL_INT(0, fxemb_power_enter(FXEMB_POWER_IDLE, FXEMB_WAKEUP_GPIO));
    TEST_ASSERT_EQUAL_INT(FXEMB_POWER_IDLE, fxemb_power_current_mode());
}

void test_power_deepsleep_without_wakeup_returns_einval(void) {
    /* trampa paquete R-05: deepsleep sin wakeup source -> -EINVAL. */
    TEST_ASSERT_EQUAL_INT(-EINVAL, fxemb_power_enter(FXEMB_POWER_DEEPSLEEP, FXEMB_WAKEUP_NONE));
}

void test_power_consumption_returns_zero_stub(void) {
    /* trampa paquete P03: el stub devuelve 0, no mA realistas. */
    TEST_ASSERT_EQUAL_INT(0, fxemb_power_consumption_ua());
}

int main(void) {
    UnityBegin("test_power_modes.c");
    RUN_TEST(test_power_init_starts_in_run_mode);
    RUN_TEST(test_power_enter_idle_succeeds);
    RUN_TEST(test_power_deepsleep_without_wakeup_returns_einval);
    RUN_TEST(test_power_consumption_returns_zero_stub);
    return UnityEnd();
}
