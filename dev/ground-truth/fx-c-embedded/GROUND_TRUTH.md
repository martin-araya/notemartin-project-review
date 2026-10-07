# GROUND_TRUTH — fx-c-embedded

## Vision general

Fixture C99 testeable en host para microcontrolador (estilo ARM Cortex-M): tabla de vectores en `.isr_vector`, simbolos `__attribute__((weak))` para handlers sobreescribibles, dispatch de comandos por tabla de punteros a funcion, secciones del linker script con LMA/VMA distintas, seleccion de placa via `#ifdef`, registros MMIO `volatile` para acceso a hardware. Cubre la primera fase del bloque "Nativo y sistemas" (F06x-F06z) — el caso del firmware embebido de verdad (no solo C++ de alto nivel).

## Stack

- C99 con `-std=c99 -pedantic`
- GCC 13.x en `gcc:13-bookworm` para host
- Unity (fork minimo en `include/tests/unity.h`) + runner Python en `tests/test_runner.py`
- `arm-none-eabi-gcc` opcional para cross-compile (target `make cross-arm`)
- QEMU opcional para ejecutar el firmware (target `make qemu`)

## Features y R-NN

| Feature | R-NN | Cubre |
|---|---|---|
| `lectura-de-sensores` | 7 | lectura exitosa, EAGAIN en ring vacio, EINVAL en canal invalido, ENODEV, race condition, valor cacheado, ring overflow |
| `protocolo-de-comandos-uart` | 7 | AT+READ?<CR><LF>, buffer overflow, comando desconocido, +OK/+ERR, handler failure, soft reset, ring vacio |
| `modo-bajo-consumo` | 7 | RUN->IDLE, wake-up GPIO, wake-up RTC, EBUSY en SLEEP activo, EINVAL en DEEPSLEEP sin wake-up, consumo stub, watchdog reset |

## Trampas plantadas (CC-04..CC-06)

### Ecosistema (6/6)
1. **E01** `isr_vector[16]` en `src/startup.c` con `__attribute__((section(".isr_vector")))` — primer slot es initial SP, los siguientes 15 son punteros a handlers.
2. **E02** `__attribute__((weak))` en `include/fxemb/weak_handlers.h` para Reset/NMI/HardFault/Default; sobreescritos en `src/board/board_*.c`.
3. **E03** `cmd_table[]` en `src/command_dispatch.c` con `cmd_handler_t` typedef en `include/fxemb/command_dispatch.h`; dispatch O(n) lineal con strcmp.
4. **E04** `firmware.ld` con `.isr_vector` + `.text` + `.data` (LMA en FLASH, VMA en RAM) + `.bss` NOLOAD; simbolos exportados `_estack`, `_sidata`, `_sdata`, `_sbss`, `_ebss`.
5. **E05** `#ifdef STM32F4_DISCOVERY / #elif NRF52_DK / #elif BOARD_HOST / #else #error` en `include/fxemb/board.h`; activa distintos `board_*.c`.
6. **E06** Macros MMIO `volatile uint32_t*` en `include/fxemb/hal.h` (FXEMB_GPIOA_ODR, FXEMB_GPIOA_IDR, FXEMB_RCC_AHB1ENR); stub en `hal_host.c` para tests.

### Paquete (6/6)
1. **P01** `race_lectura_sensores` en `src/sensors.c` — `g_sensor_head++` no atomico.
2. **P02** `uart_handler_race` en `src/uart_protocol.c` — `g_rx_head++` no atomico en rx_byte.
3. **P03** `consumo_stub_irreal` en `src/power_modes.c` — `fxemb_power_consumption_ua()` retorna 0 siempre.
4. **P04** `sleep_lock_olvidado` en `src/power_modes.c` — `fxemb_power_enter` no toma mutex.
5. **P05** `sensor_no_inicializado` en `src/sensors.c` — `read` no devuelve -ENODEV; cae en basura.
6. **P06** `weak_handler_loop_infinito` en `src/startup.c` — `Default_Handler` queda en `while(1)` sin bkpt.

### Superficiales (3/3)
1. **S01** `dead_legacy_helper` en `src/legacy_helpers.c` — `legacy_uart_send_byte` y `legacy_crc16` sin consumidores.
2. **S02** `unused_macro` en `include/fxemb/deprecated_macros.h` — LEGACY_DELAY/NOP/BARRIER sin marca de deprecation.
3. **S03** `commented_out_code` en `src/sensors.c` — 4 lineas comentadas con TODO DMA en `fxemb_sensors_get_count_via_dma`.

## Salida de la suite

46 tests Unity passing en `gcc:13-bookworm` con `make test`:

- 4 tests de `sensors` (feature 1)
- 4 tests de `uart_protocol` (feature 2)
- 4 tests de `power_modes` (feature 3)
- 4 tests de `command_dispatch` (tabla E03)
- 3 tests de `vector_table` (E01)
- 3 tests de `weak_symbols` (E02)
- 3 tests de `linker_script` (E04)
- 3 tests de `board_selection` (E05)
- 3 tests de `hal_volatile` (E06)
- 6 tests de trampas del ecosistema
- 6 tests de trampas del paquete
- 3 tests de trampas superficiales

## Comandos para reproducir

```bash
docker build -f dev/fixtures/fx-c-embedded/Dockerfile.test -t npr-fx-c-embedded dev/fixtures/fx-c-embedded
docker run --rm npr-fx-c-embedded

# o via run_fixture_tests.py:
python dev/tools/run_fixture_tests.py --fixture fx-c-embedded --container
```

Targets Makefile:
- `make test` — corre los 46 tests Unity
- `make build` — compila el firmware en host (`gcc -DHOST_TEST=1`)
- `make cross-arm` — cross-compile para STM32F4 (`arm-none-eabi-gcc`, opcional)
- `make qemu` — ejecuta el firmware en QEMU (`qemu-system-arm`, opcional)
- `make clean` — borra `build/`

## Comandos para regenerar la historia git

```bash
cd dev/fixtures/fx-c-embedded
bash build-history.sh
```

Crea 8 commits incrementales.

## Notas de portabilidad

- El fixture corre nativamente en linux/macos via Docker (`gcc:13-bookworm`).
- `arm-none-eabi-gcc` y `qemu-system-arm` son opcionales; no se requieren en CI pero los targets `make cross-arm` y `make qemu` estan documentados para quienes quieran verificar el cross-compile o la ejecucion bare-metal.
- `dlopen` no se usa (no aplica en bare-metal); POSIX no es relevante.
- La trampa E02 (weak symbols) requiere GCC o clang; MSVC no soporta `__attribute__((weak))` aunque el fixture compila en linux/macos.
