TEST_CMD ?= pg_prove -h localhost -U postgres -d fxpg_test db/test/*.sql && pytest dev/tests/test_fx_sql_postgres_ground_truth.py -q
IMAGE_TAG ?= npr-fx-sql-postgres

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
	docker run --rm -v $(PWD)/.pg_data:/var/lib/postgresql/data $(IMAGE_TAG)

history:
	@bash ./build-history.sh

clean:
	@rm -rf .pg_data 2>/dev/null || true
	@rm -rf Generated/* 2>/dev/null || true