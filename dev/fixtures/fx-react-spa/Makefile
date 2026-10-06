TEST_CMD ?= npx vitest run --reporter=verbose

.PHONY: test build lint history clean help

help:
	@echo "Targets: test, build, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building (no-op for fixture; vite build not exercised in tests)"
	@npx vite build

lint:
	@echo "TypeScript typecheck"
	@npx tsc --noEmit

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf dist node_modules .vitest 2>/dev/null || true