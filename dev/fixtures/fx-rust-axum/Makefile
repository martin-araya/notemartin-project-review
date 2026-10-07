TEST_CMD ?= cargo test --workspace

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building Rust workspace"
	@cargo build --workspace

dev:
	@echo "Starting dev server (not used by tests)"
	@DATABASE_URL=sqlite::memory: HTTP_PORT=8082 cargo run --bin server

lint:
	@echo "No linter configured (Rust/cargo fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@cargo clean 2>/dev/null || true