TEST_CMD ?= vendor/bin/phpunit --testdox

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Installing PHP dependencies via composer"
	@composer install --no-interaction --prefer-dist

dev:
	@echo "Starting Laravel dev server (not used by tests)"
	@php artisan serve --host=0.0.0.0 --port=8083

lint:
	@echo "No linter configured (Laravel + PHPUnit fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf vendor composer.lock 2>/dev/null || true
	@rm -rf storage/logs/*.log 2>/dev/null || true
