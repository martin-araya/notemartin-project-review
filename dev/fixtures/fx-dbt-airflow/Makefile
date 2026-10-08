TEST_CMD ?= bash tools/run_dbt.sh && bash tools/run_airflow_tests.sh && pytest dev/tests/test_fx_dbt_airflow_ground_truth.py -q
IMAGE_TAG ?= npr-fx-dbt-airflow

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
	docker run --rm -v $(PWD)/.duckdb:/fixture/.duckdb $(IMAGE_TAG)

history:
	@bash ./build-history.sh

clean:
	@rm -rf .duckdb .airflow Generated 2>/dev/null || true
	@rm -rf dbt/dbt_packages dbt/target dbt/logs 2>/dev/null || true