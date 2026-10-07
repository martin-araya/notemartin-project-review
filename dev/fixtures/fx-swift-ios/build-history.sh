#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06aa.
# El fixture se construye con los archivos reales ya en su sitio; este
# script crea commits incrementales declarando paths especificos.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

# Commit 1: scaffold + manifest + .gitignore + README
cat > .gitignore <<'EOF'
build/
/.build/
/.swiftpm/
/DerivedData/
xcuserdata/
*.xcuserstate
*.xcuserdatad/
EOF
echo "# fx-swift-ios" > README.md
git add .gitignore README.md manifest.yml Dockerfile.test Makefile \
        tools/run_spm_and_xcode_tests.sh tools/generate_pbxproj.py
git commit -q -m "chore: initial scaffold (README, .gitignore, manifest, runner)"

# Commit 2: Package.swift
git add Package.swift
git commit -q -m "build: add Swift Package manifest for FxSwiftCore"

# Commit 3: Models
git add Sources/FxSwiftCore/Models
git commit -q -m "feat(models): add Codable Expense + ExpenseCategory + OnboardingState + SyncStatus"

# Commit 4: PropertyWrappers + Protocols
git add Sources/FxSwiftCore/PropertyWrappers Sources/FxSwiftCore/Protocols
git commit -q -m "feat(property-wrappers+protocols): Debounced, UserDefaultsBacked, Describable, Syncable"

# Commit 5: AppGroup + Persistence
git add Sources/FxSwiftCore/AppGroup Sources/FxSwiftCore/Persistence
git commit -q -m "feat(appgroup+persistence): AppGroupPaths, AppGroupStore, ExpensesRepository, ExpensesStore"

# Commit 6: Sync
git add Sources/FxSwiftCore/Sync
git commit -q -m "feat(sync): add CloudKitSyncEngine actor and SyncCoordinator"

# Commit 7: Widget + BuildFlags
git add Sources/FxSwiftCore/Widget Sources/FxSwiftCore/BuildFlags
git commit -q -m "feat(widget+build-flags): WidgetSummary, WidgetSummaryProvider, BuildFlags"

# Commit 8: UI + ObjCBridge + Tests + Examples Xcode project
git add Sources/FxSwiftCore/UI Sources/FxSwiftCore/ObjCBridge \
        Sources/FxSwiftCore/FxSwiftCore.swift \
        Sources/FxSwiftCoreTests \
        Examples
git commit -q -m "feat(ui+objc+tests+xcode): UI views, ObjC bridge, Swift Testing suite and Xcode project"

echo "Historia creada con 8 commits:"
git log --oneline
