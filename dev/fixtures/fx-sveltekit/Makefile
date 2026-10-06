TEST_CMD ?= npm test -- --run

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building SvelteKit app"
	@npx vite build

dev:
	@echo "Starting SvelteKit dev server (not used by tests)"
	@npx vite dev

lint:
	@echo "No linter configured (Svelte + Vitest fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf node_modules .svelte-kit build .vitest 2>/dev/null || true
