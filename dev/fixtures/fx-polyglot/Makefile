TEST_CMD ?= bash tests/all-tests.sh

.PHONY: test build lint history clean help

help:
	@echo "Targets: test, build, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@cd src/ingesta && go build -o ../../artifacts/ingesta .
	@cd src/transformacion && cargo build --release --features v1
	@cp src/transformacion/target/release/transformacion artifacts/transformacion-linux
	@cd src/transformacion && cargo build --release --no-default-features --features v2,strict --bin transformacion_v2
	@cp src/transformacion/target/release/transformacion_v2 artifacts/transformacion-linux-v2

lint:
	@cd src/ingesta && go vet ./...
	@cd src/transformacion && cargo clippy --all-features -- -D warnings

history:
	@bash ./build-history.sh

clean:
	@rm -rf artifacts/* src/ingesta/ingesta src/transformacion/target