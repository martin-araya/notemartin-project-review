TEST_CMD ?= bash build/all-tests.sh

.PHONY: test build lint history clean help

help:
	@echo "Targets: test, build, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building all 5 artifacts"
	@bash build/build-all.sh

lint:
	@echo "Type-checking TypeScript"
	@npx tsc --noEmit

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf artifacts/* node_modules .vite 2>/dev/null || true
