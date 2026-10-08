TEST_CMD ?= bash entrypoint.sh
IMAGE_TAG ?= npr-fx-python-ml

.PHONY: test docker-build docker-run docker-test history clean help
help:
	@echo "Targets: test, docker-build, docker-test, history, clean"
test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)
docker-build:
	docker build -f Dockerfile.test -t $(IMAGE_TAG) .
docker-test: docker-build
	docker run --rm -v $(PWD)/.mlruns:/fixture/mlruns $(IMAGE_TAG)
history:
	@bash ./build-history.sh
clean:
	@rm -rf .dvc mlruns mlartifacts .pytest_cache __pycache__ Generated 2>/dev/null || true