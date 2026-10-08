TEST_CMD ?= xvfb-run -a yarn vitest --run
IMAGE_TAG ?= npr-fx-electron

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
	docker run --rm -v $(PWD)/.yarn-cache:$(HOME)/.cache $(IMAGE_TAG)

history:
	@bash ./build-history.sh

clean:
	@rm -rf node_modules .yarn-cache dist release 2>/dev/null || true
	@rm -rf Generated/* 2>/dev/null || true