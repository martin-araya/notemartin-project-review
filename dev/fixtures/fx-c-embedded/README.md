# fx-c-embedded

Firmware C99 testeable en host para microcontrolador (estilo ARM Cortex-M):
tabla de vectores, simbolos `weak`, dispatch por tablas de punteros a funcion,
secciones por linker script, `#ifdef` por placa y registros MMIO `volatile`.

## Stack

- C99 con `-std=c99 -pedantic`
- GCC 13.x en `gcc:13-bookworm`
- Unity (ThrowTheSwitch) + runner Python para tests en host
- `arm-none-eabi-gcc` opcional para cross-compile (no requerido en CI)
- QEMU opcional para ejecutar el firmware (no requerido en CI)

## Features

- `lectura-de-sensores`: lectura periodica de temperatura, presion y acelerometro.
- `protocolo-de-comandos-uart`: comandos AT-like con framing, checksum y estado.
- `modo-bajo-consumo`: transiciones RUN/IDLE/SLEEP/DEEPSLEEP con wake-up sources.

## Comandos

```bash
make test         # corre tests Unity en host via Python runner
make build        # compila firmware_host con gcc -DHOST_TEST=1
make cross-arm    # cross-compile para STM32F4 (requiere arm-none-eabi-gcc)
make qemu         # ejecuta firmware en qemu-system-arm
make clean        # borra build/
```

## Contenedor

```bash
python dev/tools/run_fixture_tests.py --fixture fx-c-embedded --container
```

Imagen: `gcc:13-bookworm` con `make`, `binutils`, `python3`.
