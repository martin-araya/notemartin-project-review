TEST_CMD ?= pytest -q

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Running Alembic migrations"
	@alembic upgrade head || true

dev:
	@echo "Starting FastAPI dev server (not used by tests)"
	@uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

lint:
	@echo "No linter configured (FastAPI/pytest fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	@rm -rf *.db 2>/dev/null || true