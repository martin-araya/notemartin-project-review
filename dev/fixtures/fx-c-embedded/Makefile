TEST_CMD ?= tests/test_runner.py

.PHONY: test build cross-arm qemu clean help

help:
	@echo "Targets: test, build, cross-arm, qemu, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Compilando firmware con gcc -DHOST_TEST=1 (host-emulation)"
	@mkdir -p build
	@gcc -std=c99 -DHOST_TEST=1 -I include -I src/hal -I src/board \
	    -c src/startup.c -o build/startup.o
	@gcc -std=c99 -DHOST_TEST=1 -I include -I src/hal -I src/board \
	    -c src/main.c -o build/main.o
	@gcc -std=c99 -DHOST_TEST=1 -I include -I src/hal -I src/board \
	    -c src/sensors.c -o build/sensors.o
	@gcc -std=c99 -DHOST_TEST=1 -I include -I src/hal -I src/board \
	    -c src/uart_protocol.c -o build/uart_protocol.o
	@gcc -std=c99 -DHOST_TEST=1 -I include -I src/hal -I src/board \
	    -c src/power_modes.c -o build/power_modes.o
	@gcc -std=c99 -DHOST_TEST=1 -I include -I src/hal -I src/board \
	    -c src/command_dispatch.c -o build/command_dispatch.o
	@gcc -std=c99 -DHOST_TEST=1 -I include -I src/hal -I src/board \
	    -c src/hal/hal_host.c -o build/hal_host.o
	@gcc -std=c99 -DHOST_TEST=1 -I include -I src/hal -I src/board \
	    -c src/board/board_host.c -o build/board_host.o
	@gcc -std=c99 -DHOST_TEST=1 -I include -I src/hal -I src/board \
	    -c src/legacy_helpers.c -o build/legacy_helpers.o
	@gcc build/*.o -o build/firmware_host
	@echo "OK: build/firmware_host"

cross-arm:
	@echo "Cross-compile para ARM Cortex-M con arm-none-eabi-gcc (no requerido en CI)"
	@arm-none-eabi-gcc -std=c99 -mcpu=cortex-m4 -mthumb -nostdlib \
	    -T firmware.ld -I include \
	    -DSTM32F4_DISCOVERY=1 \
	    src/startup.c src/main.c src/sensors.c src/uart_protocol.c \
	    src/power_modes.c src/command_dispatch.c \
	    src/hal/hal_stm32f4.c src/board/board_stm32f4.c \
	    -o build/firmware_stm32f4.elf
	@echo "OK: build/firmware_stm32f4.elf"

qemu:
	@echo "Ejecutando firmware en qemu-system-arm (requiere QEMU instalado)"
	@qemu-system-arm -cpu cortex-m3 -machine lm3s6965evb -nographic \
	    -kernel build/firmware_stm32f4.elf

clean:
	@rm -rf build
