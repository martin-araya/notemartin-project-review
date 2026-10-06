TEST_CMD ?= mvn -B -q test -Dtest='TrapsEcosystemTest,TrapsPackageTest,TrapsSuperficialTest'

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"
	@echo ""
	@echo "Por defecto corre los tests estaticos de trampas (Traps*Test)."
	@echo "Para correr todos los tests (incluye runtime con @SpringBootTest,"
	@echo "@WebMvcTest, Testcontainers):"
	@echo "  TEST_CMD='mvn -B -q test' make test"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building Spring Boot app"
	@mvn -B -q package -DskipTests

dev:
	@echo "Starting Spring Boot dev server (not used by tests)"
	@mvn -B -q spring-boot:run

lint:
	@echo "No linter configured (Spring + JUnit fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf target 2>/dev/null || true
