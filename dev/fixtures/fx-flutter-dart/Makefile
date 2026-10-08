TEST_CMD ?= flutter test --no-pub --reporter=expanded
IMAGE_TAG ?= npr-fx-flutter-dart

.PHONY: test docker-build docker-run docker-test history clean help

help:
	@echo "Targets: test, docker-build, docker-test, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"
	@echo "IMAGE_TAG=$(IMAGE_TAG)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

docker-build:
	docker build -f Dockerfile.test -t $(IMAGE_TAG) .

docker-test: docker-build
	docker run --rm -v $(PWD)/.dart-tool:/app/.dart_tool $(IMAGE_TAG)

history:
	@bash ./build-history.sh

clean:
	@rm -rf .dart_tool build .dart_tool-cache 2>/dev/null || true
	@rm -rf lib/**/*.g.dart lib/**/*.freezed.dart 2>/dev/null || true