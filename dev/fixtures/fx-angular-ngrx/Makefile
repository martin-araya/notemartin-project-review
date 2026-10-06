TEST_CMD ?= npx jest --runInBand

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building Angular app (no real build needed for tests)"
	@npx ng build --configuration=development 2>/dev/null || true

dev:
	@echo "Starting Angular dev server (not used by tests)"
	@npx ng serve 2>/dev/null || true

lint:
	@echo "No linter configured (Angular + Jest fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf node_modules dist .angular coverage .jest 2>/dev/null || true
