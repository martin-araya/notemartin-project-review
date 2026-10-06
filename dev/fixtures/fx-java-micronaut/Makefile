TEST_CMD ?= gradle test --no-daemon --console=plain

.PHONY: test build lint history clean help

help:
	@echo "Targets: test, build, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building with Gradle"
	@gradle build --no-daemon --console=plain

lint:
	@echo "Type-checking Java sources (compileJava)"
	@gradle compileJava --no-daemon --console=plain

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@gradle clean --no-daemon --console=plain 2>/dev/null || true
	@rm -rf .gradle build .idea 2>/dev/null || true
