TEST_CMD ?= bash tests/all-tests.sh

.PHONY: test build lint history clean help

help:
	@echo "Targets: test, build, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building (no-op for fixture; next build no se ejecuta en tests)"
	@npx next build

lint:
	@echo "TypeScript typecheck"
	@npx tsc --noEmit

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf .next node_modules e2e-results 2>/dev/null || true