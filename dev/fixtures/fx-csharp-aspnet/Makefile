TEST_CMD ?= dotnet test tests/FxAspNet.Tests/FxAspNet.Tests.csproj --nologo

.PHONY: test build dev lint history clean help

help:
	@echo "Targets: test, build, dev, lint, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build:
	@echo "Building ASP.NET Core app"
	@dotnet build --nologo

dev:
	@echo "Starting dev server (not used by tests)"
	@ASPNETCORE_URLS=http://localhost:5080 dotnet run --project FxAspNet.csproj

lint:
	@echo "No linter configured (xUnit fixture)"

history:
	@echo "Generating scripted git history"
	@bash ./build-history.sh

clean:
	@rm -rf bin obj 2>/dev/null || true