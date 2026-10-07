TEST_CMD ?= pytest -q --ds=fxdjango.settings.dev

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Migrating DB schema"
	@python manage.py migrate --no-input

dev:
	@echo "Starting Django dev server (not used by tests)"
	@python manage.py runserver 0.0.0.0:8080

lint:
	@echo "No linter configured (Django/pytest fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@rm -rf *.sqlite3 db.sqlite3 2>/dev/null || true