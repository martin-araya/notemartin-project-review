TEST_CMD ?= npx vitest run

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Preparing Nuxt (no real build needed for tests)"
	@npx nuxt prepare

dev:
	@echo "Starting Nuxt dev server (not used by tests)"
	@npx nuxt dev

lint:
	@echo "No linter configured (Nuxt + Vitest fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf node_modules .nuxt .output .vitest 2>/dev/null || true
