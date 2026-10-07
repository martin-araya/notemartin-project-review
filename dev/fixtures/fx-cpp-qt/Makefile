TEST_CMD ?= tests/test_runner.py

.PHONY: test build clean help

help:
	@echo "Targets: test, build, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Configurando y compilando con CMake"
	@cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug >/dev/null
	@cmake --build build --parallel
	@echo "Ejecutando: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
	@cmake --build build --parallel

clean:
	@rm -rf build
