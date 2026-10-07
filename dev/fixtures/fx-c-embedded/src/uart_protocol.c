/* F06y: uart_protocol.c - feature 2: parser de lineas AT-like. */
#include "fxemb/uart_protocol.h"

#include <stdint.h>
#include <stddef.h>

/* Ring buffer de recepcion. La trampa paquete P02 (uart_handler_race)
 * se manifiesta cuando la ISR escribe y el main lee sin sincronizar. */
static uint8_t  g_rx_buf[FXEMB_UART_BUF_SIZE];
static size_t   g_rx_head = 0;
static size_t   g_rx_tail = 0;
static int      g_uart_initialized = 0;

static size_t ring_used(void) {
    return (g_rx_head + FXEMB_UART_BUF_SIZE - g_rx_tail) % FXEMB_UART_BUF_SIZE;
}

int fxemb_uart_init(void) {
    g_rx_head = 0;
    g_rx_tail = 0;
    g_uart_initialized = 1;
    return 0;
}

void fxemb_uart_reset(void) {
    g_rx_head = 0;
    g_rx_tail = 0;
}

void fxemb_uart_rx_byte(uint8_t byte) {
    /* Sin lock. La trampa P02 vive aqui: si la ISR llama a esta funcion
     * mientras el main loop hace fxemb_uart_read_line, el head puede
     * ser actualizado a mitad de operacion. */
    size_t next = (g_rx_head + 1) % FXEMB_UART_BUF_SIZE;
    if (next == g_rx_tail) {
        /* Ring lleno: descartamos el byte. */
        return;
    }
    g_rx_buf[g_rx_head] = byte;
    g_rx_head = next;
}

int fxemb_uart_rx_buffered(const uint8_t** out_data, size_t* out_len) {
    if (out_data) *out_data = g_rx_buf;
    if (out_len)  *out_len = ring_used();
    return 0;
}

/* Busca el primer CR o LF en el buffer y devuelve la linea terminada
 * en NUL. Retorna 0 si no hay linea completa. */
int fxemb_uart_read_line(char* out, size_t out_size) {
    if (!g_uart_initialized || out_size == 0) return 0;
    size_t i = g_rx_tail;
    size_t line_end = (size_t)-1;
    while (i != g_rx_head) {
        if (g_rx_buf[i] == '\r' || g_rx_buf[i] == '\n') {
            line_end = i;
            break;
        }
        i = (i + 1) % FXEMB_UART_BUF_SIZE;
    }
    if (line_end == (size_t)-1) return 0;

    /* Copia la linea al output. */
    size_t n = 0;
    i = g_rx_tail;
    while (i != line_end && n + 1 < out_size) {
        out[n++] = (char)g_rx_buf[i];
        i = (i + 1) % FXEMB_UART_BUF_SIZE;
    }
    out[n] = '\0';

    /* Avanza el tail saltando CR LF opcionales. */
    g_rx_tail = (line_end + 1) % FXEMB_UART_BUF_SIZE;
    if (g_rx_tail != g_rx_head && (g_rx_buf[g_rx_tail] == '\n' || g_rx_buf[g_rx_tail] == '\r')) {
        g_rx_tail = (g_rx_tail + 1) % FXEMB_UART_BUF_SIZE;
    }
    return (int)n;
}

int fxemb_uart_write(const char* data, size_t len) {
    (void)data;
    (void)len;
    /* En host, simplemente lo descartamos. En bare-metal, HAL UART TX. */
    return 0;
}
