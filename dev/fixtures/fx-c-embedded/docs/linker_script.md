/* F06y: linker_script.md - documenta las secciones y simbolos del
 * firmware.ld. La trampa E04 vive en este archivo: la skill debe
 * leerlo para entender como se organizan .isr_vector, .text, .data
 * y .bss, y que simbolos exporta (los _estack, _sidata, _sbss, etc.).
 *
 * El linker script (firmware.ld) define:
 *   - MEMORY: FLASH (1M @ 0x08000000) + RAM (128K @ 0x20000000)
 *   - .isr_vector: tabla de vectores al inicio de FLASH (KEEP)
 *   - .text: codigo y read-only
 *   - .data: variables inicializadas (LMA en FLASH, VMA en RAM, copiadas
 *     en startup desde _sidata a _sdata)
 *   - .bss: variables zero-init (NOLOAD, . = 0 por startup)
 *   - _estack: simbolo exportado al final de RAM
 */
