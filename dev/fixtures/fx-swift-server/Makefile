TEST_CMD ?= swift test --parallel
IMAGE_TAG ?= npr-fx-swift-server

.PHONY: test build docker-build docker-run docker-test history clean help

help:
	@echo "Targets: test, docker-build, docker-test, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"
	@echo "IMAGE_TAG=$(IMAGE_TAG)"

# Tests locales (requiere Swift 6.0+ instalado)
test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

# Build de la imagen Docker
docker-build:
	docker build -f Dockerfile.test -t $(IMAGE_TAG) .

# Ejecuta los tests dentro del contenedor
docker-test: docker-build
	docker run --rm -v $(PWD)/.build-cache:/app/.build $(IMAGE_TAG)

# Genera historia git reproducible de 8 commits
history:
	@bash ./build-history.sh

clean:
	@rm -rf .build .swiftpm .build-cache DerivedData 2>/dev/null || true
	@rm -rf Tests/.build 2>/dev/null || true