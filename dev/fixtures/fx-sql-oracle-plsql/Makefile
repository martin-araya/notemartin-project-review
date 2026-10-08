TEST_CMD ?= sqlcl /nolog @db/test/01-accounts-test.sql && sqlcl /nolog @db/test/02-interest-test.sql && sqlcl /nolog @db/test/03-monthly-close-test.sql && pytest dev/tests/test_fx_sql_oracle_plsql_ground_truth.py -q
IMAGE_TAG ?= npr-fx-sql-oracle-plsql

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
	docker run --rm -v $(PWD)/.oracle_data:/opt/oracle/oradata $(IMAGE_TAG)

history:
	@bash ./build-history.sh

clean:
	@rm -rf .oracle_data 2>/dev/null || true
	@rm -rf Generated/* 2>/dev/null || true