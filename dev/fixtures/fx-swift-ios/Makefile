TEST_CMD ?= bash tools/run_spm_and_xcode_tests.sh

.PHONY: test build-spm build-xcode history clean help

help:
	@echo "Targets: test, build-spm, build-xcode, history, clean"
	@echo "TEST_CMD=$(TEST_CMD)"
	@echo "Requiere: macOS con Xcode y toolchain Swift 6"

test:
	@echo "Running: $(TEST_CMD)"
	@$(TEST_CMD)

build-spm:
	@swift build

build-xcode:
	@xcodebuild -project Examples/FxSwift.xcodeproj -scheme FxSwiftApp \
	    -destination 'generic/platform=iOS Simulator' -configuration Debug \
	    CODE_SIGNING_ALLOWED=NO build

history:
	@bash build-history.sh

clean:
	@rm -rf .build
