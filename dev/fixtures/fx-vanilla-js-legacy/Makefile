TEST_CMD ?= npm test -- --runInBand --verbose

.PHONY: test build lint history clean help

help:
	@echo "Targets: test, build, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building CSS from SCSS (no Gulp required for CI)"
	@if [ -x node_modules/.bin/sass ]; then node_modules/.bin/sass public/scss/main.scss public/css/main.css --no-source-map; else echo "sass not installed; CSS must be committed manually"; fi

lint:
	@echo "No linter configured (ES5 + jQuery fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf dist node_modules .jest 2>/dev/null || true
