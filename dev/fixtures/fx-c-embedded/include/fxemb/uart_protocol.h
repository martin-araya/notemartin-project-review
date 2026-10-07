/* F06y: uart_protocol.h - feature 2: protocolo de comandos AT-like
 * sobre UART.
 *
 * Formato:
 *   AT+<CMD>?<CR><LF>     -> consulta
 *   AT+<CMD>=<VAL><CR><LF> -> set
 *   +OK <payload><CR><LF>  -> respuesta correcta
 *   +ERR -<errno><CR><LF> -> respuesta de error
 *
 * La trampa paquete P02 (uart_handler_race) se manifiesta cuando
 * la ISR completa el buffer mientras el main loop lo lee.
 */
#ifndef FXEMB_UART_PROTOCOL_H
#define FXEMB_UART_PROTOCOL_H

#include <stdint.h>
#include <stddef.h>

#define FXEMB_UART_BUF_SIZE 64
#define FXEMB_UART_TOKEN_SIZE 32

/* Inicializa el driver. */
int  fxemb_uart_init(void);

/* Alimenta bytes al parser (llamado por la ISR o por el test). */
void fxemb_uart_rx_byte(uint8_t byte);
int  fxemb_uart_rx_buffered(const uint8_t** out_data, size_t* out_len);

/* Lee una linea terminada en CR/LF. */
int  fxemb_uart_read_line(char* out, size_t out_size);

/* Escribe una respuesta (anade CR/LF). */
int  fxemb_uart_write(const char* data, size_t len);

/* Reset del parser. */
void fxemb_uart_reset(void);

#endif
