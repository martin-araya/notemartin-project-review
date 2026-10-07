TEST_CMD ?= ctest --test-dir build --output-on-failure

.PHONY: test build history clean help

help:
	@echo "Targets: test, build, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Configuring and building with CMake"
	@cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug >/dev/null
	@cmake --build build --parallel
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
	@cmake --build build --parallel

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf build
