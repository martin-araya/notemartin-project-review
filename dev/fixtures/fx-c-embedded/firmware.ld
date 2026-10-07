/* F06y: firmware.ld - linker script para el firmware embebido.
 *
 * E04: este archivo es parte de la trampa del ecosistema. La skill debe
 * notar que:
 *   - .isr_vector se ubica al inicio de FLASH (antes de .text)
 *   - KEEP(*(.isr_vector)) impide que el linker descarte la tabla
 *   - .data tiene LMA en FLASH y VMA en RAM (copiada en startup)
 *   - .bss es zero-initialized en RAM
 *   - _estack se exporta para que startup.c coloque el vector 0
 *
 * El script se usa con:
 *   arm-none-eabi-gcc -T firmware.ld ...
 *
 * Para tests en host, el firmware NO se enlaza con este script; usa
 * gcc normal con hal_host.c. Esto esta documentado en el Makefile
 * y en docs/linker_script.md.
 */

/* Memoria: STM32F4 Discovery (valores tipicos). */
MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 1M
    RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}

/* Top del stack = fin de RAM. El vector 0 (initial SP) apunta aqui. */
_estack = ORIGIN(RAM) + LENGTH(RAM);

/* Tamano minimo de stack (en bytes) - usado por startup.c. */
_Min_Stack_Size = 0x400;

SECTIONS
{
    /* E04: .isr_vector al inicio absoluto de FLASH. El KEEP() evita que
     * el linker elimine la tabla aunque no haya referencias explicitas
     * desde el codigo C. */
    .isr_vector :
    {
        . = ALIGN(4);
        KEEP(*(.isr_vector))
        . = ALIGN(4);
    } >FLASH

    /* Codigo y datos read-only. */
    .text :
    {
        . = ALIGN(4);
        *(.text)
        *(.text*)
        *(.rodata)
        *(.rodata*)
        . = ALIGN(4);
        _etext = .;
    } >FLASH

    /* E04: .data con LMA en FLASH y VMA en RAM. El startup copia
     * de _sidata a _sdata durante el Reset_Handler. */
    .data :
    {
        . = ALIGN(4);
        _sdata = .;
        *(.data)
        *(.data*)
        . = ALIGN(4);
        _edata = .;
    } >RAM AT> FLASH
    /* _sidata = LMA de .data (donde esta en FLASH). */
    _sidata = LOADADDR(.data);

    /* E04: .bss zero-initialized en RAM. El startup limpia este bloque. */
    .bss (NOLOAD) :
    {
        . = ALIGN(4);
        _sbss = .;
        __bss_start__ = _sbss;
        *(.bss)
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        _ebss = .;
        __bss_end__ = _ebss;
    } >RAM

    /* _estack ya esta definida arriba. La exportamos de nuevo para
     * que el startup pueda referenciarla. */
    ._user_heap_stack (NOLOAD) :
    {
        . = ALIGN(8);
        PROVIDE ( end = . );
        . = . + _Min_Stack_Size;
        . = ALIGN(8);
    } >RAM
}
