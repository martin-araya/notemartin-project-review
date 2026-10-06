TEST_CMD ?= pnpm test

.PHONY: test build lint history clean help

help:
	@echo "Targets: test, build, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building with turbo"
	@pnpm build

lint:
	@echo "Type-checking with tsc"
	@pnpm lint

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf node_modules .turbo .pnpm-store dist .angular coverage 2>/dev/null || true
