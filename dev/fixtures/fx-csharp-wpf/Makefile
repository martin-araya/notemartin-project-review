TEST_CMD ?= dotnet test --logger "console;verbosity=normal"
IMAGE_TAG ?= npr-fx-csharp-wpf

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
	docker run --rm -v $(PWD)/.nuget-cache:$(HOME)/.nuget/packages $(IMAGE_TAG)

history:
	@bash ./build-history.sh

clean:
	@rm -rf bin obj .vs .nuget-cache 2>/dev/null || true
	@rm -rf Generated/* 2>/dev/null || true