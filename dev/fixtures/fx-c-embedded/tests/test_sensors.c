/* F06y: test_sensors.c - 4 tests para feature 1. */
#include "unity.h"
#include "fxemb/sensors.h"
#include "fxemb/hal.h"

#include <string.h>

void setUp(void) {
    /* Llamamos fxemb_sensors_init() por defecto para resetear el ring. */
    fxemb_sensors_init();
}

void tearDown(void) {}

void test_sensors_init_zeros_ring(void) {
    TEST_ASSERT_EQUAL_INT(FXEMB_SENSOR_OK, fxemb_sensors_init());
    uint32_t values[FXEMB_SENSOR_COUNT];
    TEST_ASSERT_EQUAL_INT(FXEMB_SENSOR_OK, fxemb_sensors_read_all(values));
    for (int i = 0; i < FXEMB_SENSOR_COUNT; ++i) {
        TEST_ASSERT_EQUAL_INT(0, (int)values[i]);
    }
}

void test_sensors_read_with_empty_ring_returns_eagain(void) {
    /* Ring vacio -> EAGAIN. */
    uint32_t v = 0;
    TEST_ASSERT_EQUAL_INT(FXEMB_SENSOR_EAGAIN, fxemb_sensors_read(0, &v));
}

void test_sensors_push_then_read_returns_value(void) {
    /* Alimentamos el ring con un valor y leemos. */
    extern void fxemb_sensors_push(uint8_t channel, uint32_t value);
    fxemb_sensors_push(FXEMB_SENSOR_TEMP_CHANNEL, 1234);
    uint32_t v = 0;
    TEST_ASSERT_EQUAL_INT(FXEMB_SENSOR_OK, fxemb_sensors_read(FXEMB_SENSOR_TEMP_CHANNEL, &v));
    TEST_ASSERT_EQUAL_INT(1234, (int)v);
}

void test_sensors_read_invalid_channel_returns_einval(void) {
    uint32_t v = 0;
    TEST_ASSERT_EQUAL_INT(FXEMB_SENSOR_EINVAL, fxemb_sensors_read(99, &v));
    TEST_ASSERT_EQUAL_INT(FXEMB_SENSOR_EINVAL, fxemb_sensors_read(0xFF, &v));
}

int main(void) {
    UnityBegin("test_sensors.c");
    RUN_TEST(test_sensors_init_zeros_ring);
    RUN_TEST(test_sensors_read_with_empty_ring_returns_eagain);
    RUN_TEST(test_sensors_push_then_read_returns_value);
    RUN_TEST(test_sensors_read_invalid_channel_returns_einval);
    return UnityEnd();
}
