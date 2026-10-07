/* F06y: legacy_helpers.c - S01 trampa superficial.
 *
 * Helper legacy que nadie llama. Compilado y enlazado, pero sin
 * consumidores. La skill debe notar que la funcion existe pero no
 * aparece en el call graph.
 */
#include <stdint.h>

/* trampa S01: dead_helper. */
uint8_t legacy_uart_send_byte(uint8_t byte) {
    (void)byte;
    return 0;
}

uint16_t legacy_crc16(const uint8_t* data, uint32_t len) {
    (void)data; (void)len;
    return 0;
}
