TEST_CMD ?= npm test -- --colors=false --runInBand

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Compiling TypeScript"
	@npm run build

dev:
	@echo "Starting NestJS dev server (not used by tests)"
	@npm run start:dev

lint:
	@echo "No linter configured (NestJS/Jest fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf node_modules dist coverage 2>/dev/null || true