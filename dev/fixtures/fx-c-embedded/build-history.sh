#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06y.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

# Commit 1: scaffold
cat > .gitignore <<'EOF'
build/
.cache/
*.o
*.elf
EOF
echo "# fx-c-embedded" > README.md
git add -A
git commit -q -m "chore: initial scaffold (README, .gitignore)"

# Commit 2: linker script
git add firmware.ld
git commit -q -m "feat(linker): add firmware.ld with .isr_vector and section layout (E04)"

# Commit 3: headers
mkdir -p include/fxemb include/tests
echo "" > include/fxemb/version.h
echo "" > include/fxemb/vector_table.h
echo "" > include/fxemb/weak_handlers.h
echo "" > include/fxemb/command_dispatch.h
echo "" > include/fxemb/hal.h
echo "" > include/fxemb/board.h
echo "" > include/fxemb/sensors.h
echo "" > include/fxemb/uart_protocol.h
echo "" > include/fxemb/power_modes.h
echo "" > include/fxemb/deprecated_macros.h
echo "" > include/tests/unity.h
git add -A
git commit -q -m "feat(headers): add fxemb headers (E01, E02, E03, E05, E06) and Unity stubs"

# Commit 4: sources
mkdir -p src/hal src/board
echo "" > src/startup.c
echo "" > src/main.c
echo "" > src/sensors.c
echo "" > src/uart_protocol.c
echo "" > src/power_modes.c
echo "" > src/command_dispatch.c
echo "" > src/legacy_helpers.c
echo "" > src/hal/hal_host.c
echo "" > src/hal/hal_stm32f4.c
echo "" > src/hal/hal_nrf52.c
echo "" > src/board/board_host.c
echo "" > src/board/board_stm32f4.c
echo "" > src/board/board_nrf52.c
git add -A
git commit -q -m "feat(sources): add firmware sources, HAL variants and board stubs"

# Commit 5: tests
mkdir -p tests
echo "" > tests/unity_internals.c
echo "" > tests/test_sensors.c
echo "" > tests/test_uart_protocol.c
echo "" > tests/test_power_modes.c
echo "" > tests/test_command_dispatch.c
echo "" > tests/test_vector_table.c
echo "" > tests/test_weak_symbols.c
echo "" > tests/test_linker_script.c
echo "" > tests/test_board_selection.c
echo "" > tests/test_hal_volatile.c
echo "" > tests/test_traps.c
echo "" > tests/test_runner.py
git add -A
git commit -q -m "test: add Unity test suite with 46 tests and Python runner"

# Commit 6: Makefile + Dockerfile
echo "" > Makefile
echo "" > Dockerfile.test
git add -A
git commit -q -m "build: add Makefile and Dockerfile.test for gcc:13-bookworm"

# Commit 7: docs + unique tokens
mkdir -p docs
echo "" > docs/linker_script.md
echo "" > unique_tokens.txt
git add -A
git commit -q -m "docs: add linker_script.md and unique_tokens.txt"

# Commit 8: manifest
git add manifest.yml
git commit -q -m "chore: finalize fixture with manifest.yml"

echo "Historia creada con 8 commits:"
git log --oneline
