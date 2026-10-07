TEST_CMD ?= gradle test --console=plain

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building Ktor app"
	@gradle build --console=plain -x test

dev:
	@echo "Starting Ktor dev server (not used by tests)"
	@gradle run --console=plain

lint:
	@echo "No linter configured (Ktor + Vitest fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf build .gradle 2>/dev/null || true
