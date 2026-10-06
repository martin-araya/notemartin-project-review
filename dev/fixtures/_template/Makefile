TEST_CMD ?= python -m pytest -q

.PHONY: test lint history clean help

help:
	@echo "Targets: test, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

lint:
	@echo "No linter configured for this template"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	@rm -rf dist build .pytest_cache 2>/dev/null || true
