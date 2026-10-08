TEST_CMD ?= bash tools/run_tests.sh && pytest dev/tests/test_fx_sql_tsql_ground_truth.py -q
IMAGE_TAG ?= npr-fx-sql-tsql

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
	docker run --rm -v $(PWD)/.sqlserver_data:/var/opt/mssql/data $(IMAGE_TAG)

history:
	@bash ./build-history.sh

clean:
	@rm -rf .sqlserver_data 2>/dev/null || true
	@rm -rf Generated/* 2>/dev/null || true