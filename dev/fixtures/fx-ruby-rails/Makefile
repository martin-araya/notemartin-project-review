TEST_CMD ?= bundle exec rspec --format documentation

.PHONY: test build history clean help

help:
	@echo "Targets: test, build, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Installing Ruby dependencies via bundler"
	@bundle config set --local without 'production'
	@bundle install --jobs=4 --quiet

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf vendor .bundle log/*.log tmp 2>/dev/null || true
