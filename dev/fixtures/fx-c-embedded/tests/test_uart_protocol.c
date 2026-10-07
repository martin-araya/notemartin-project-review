/* F06y: test_uart_protocol.c - 4 tests para feature 2. */
#include "unity.h"
#include "fxemb/uart_protocol.h"

#include <string.h>

void setUp(void) { fxemb_uart_init(); }
void tearDown(void) {}

void test_uart_init_resets_buffer(void) {
    /* Despues de init no hay bytes en buffer. */
    const uint8_t* data = NULL;
    size_t len = 999;
    fxemb_uart_rx_buffered(&data, &len);
    TEST_ASSERT_EQUAL_INT(0, (int)len);
}

void test_uart_rx_byte_appends_to_buffer(void) {
    fxemb_uart_rx_byte('A');
    fxemb_uart_rx_byte('T');
    const uint8_t* data = NULL;
    size_t len = 0;
    fxemb_uart_rx_buffered(&data, &len);
    TEST_ASSERT_EQUAL_INT(2, (int)len);
    TEST_ASSERT_NOT_NULL(data);
    TEST_ASSERT_EQUAL_INT('A', (int)data[0]);
    TEST_ASSERT_EQUAL_INT('T', (int)data[1]);
}

void test_uart_read_line_terminates_on_crlf(void) {
    /* Alimentamos "AT+READ?<CR><LF>" */
    const char* line = "AT+READ?";
    for (size_t i = 0; i < strlen(line); ++i) {
        fxemb_uart_rx_byte((uint8_t)line[i]);
    }
    fxemb_uart_rx_byte('\r');
    fxemb_uart_rx_byte('\n');

    char out[FXEMB_UART_TOKEN_SIZE];
    int n = fxemb_uart_read_line(out, sizeof(out));
    TEST_ASSERT_GREATER_OR_EQUAL_INT(8, n);
    TEST_ASSERT_EQUAL_STRING("AT+READ?", out);
}

void test_uart_read_line_returns_zero_when_no_line(void) {
    /* Sin CR/LF en buffer, no devolvemos linea. */
    fxemb_uart_rx_byte('A');
    fxemb_uart_rx_byte('T');
    char out[FXEMB_UART_TOKEN_SIZE];
    int n = fxemb_uart_read_line(out, sizeof(out));
    TEST_ASSERT_EQUAL_INT(0, n);
}

int main(void) {
    UnityBegin("test_uart_protocol.c");
    RUN_TEST(test_uart_init_resets_buffer);
    RUN_TEST(test_uart_rx_byte_appends_to_buffer);
    RUN_TEST(test_uart_read_line_terminates_on_crlf);
    RUN_TEST(test_uart_read_line_returns_zero_when_no_line);
    return UnityEnd();
}
