TEST_CMD ?= ./gradlew test --no-daemon
IMAGE_TAG ?= npr-fx-kotlin-android

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
	docker run --rm -v $(PWD)/.gradle-cache:/app/.gradle $(IMAGE_TAG)

history:
	@bash ./build-history.sh

clean:
	@rm -rf .gradle .gradle-cache build app/build */build 2>/dev/null || true
	@rm -rf app/src/main/res/drawable-*/ app/src/main/res/mipmap-*/ 2>/dev/null || true