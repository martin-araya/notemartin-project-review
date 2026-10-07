TEST_CMD ?= go test ./... -race -count=1

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building Go binary"
	@go build -o bin/server ./cmd/server
	@go build -o bin/legacy ./cmd/legacy

dev:
	@echo "Starting dev server (not used by tests)"
	@DATABASE_URL=:memory: HTTP_PORT=8081 WORKER_COUNT=2 go run ./cmd/server

lint:
	@echo "No linter configured (Go/race fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf bin coverage 2>/dev/null || true