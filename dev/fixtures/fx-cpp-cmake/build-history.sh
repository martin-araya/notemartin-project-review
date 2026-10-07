#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06x.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

# Commit 1: scaffold
cat > .gitignore <<'EOF'
build/
.cache/
compile_commands.json
CMakeUserPresets.json
EOF
echo "CMakeLists.txt minimo" > CMakeLists.txt
git add -A
git commit -q -m "chore: initial scaffold (CMakeLists.txt, .gitignore)"

# Commit 2: config + initializers
mkdir -p cmake include/fxproc/util
echo "" > cmake/config.h.in
echo "" > cmake/CompilerWarnings.cmake
git add -A
git commit -q -m "feat(config): add cmake config.h.in and CompilerWarnings stub (E04)"

# Commit 3: headers
mkdir -p include/fxproc
echo "" > include/fxproc/version.hpp
echo "" > include/fxproc/filter_base.hpp
echo "" > include/fxproc/registry.hpp
echo "" > include/fxproc/x_macros.h
echo "" > include/fxproc/pipeline.hpp
echo "" > include/fxproc/plugin_loader.hpp
echo "" > include/fxproc/result.hpp
echo "" > include/fxproc/filters.hpp
echo "" > include/fxproc/executor.hpp
echo "" > include/fxproc/util/deprecated_helpers.hpp
git add -A
git commit -q -m "feat(headers): add fxproc headers (E01, E02, E03, E05)"

# Commit 4: sources
mkdir -p src
echo "" > src/registry.cpp
echo "" > src/pipeline.cpp
echo "" > src/plugin_loader.cpp
echo "" > src/executor.cpp
echo "" > src/filters.cpp
echo "" > src/result.cpp
echo "" > src/main.cpp
git add -A
git commit -q -m "feat(sources): add fxproc_core sources (E01, E02, E06)"

# Commit 5: plugin
mkdir -p plugins/transform_json
echo "" > plugins/transform_json/CMakeLists.txt
echo "" > plugins/transform_json/transform_json.cpp
git add -A
git commit -q -m "feat(plugin): add transform_json plugin loaded via dlopen (E05)"

# Commit 6: db + apps
mkdir -p apps
echo "" > apps/export_demo.cpp
git add -A
git commit -q -m "feat(apps): add export_demo binary"

# Commit 7: tests
mkdir -p tests
echo "" > tests/test_registry.cpp
echo "" > tests/test_pipeline.cpp
echo "" > tests/test_filters.cpp
echo "" > tests/test_x_macros.cpp
echo "" > tests/test_cmake_generated.cpp
echo "" > tests/test_plugin_loader.cpp
echo "" > tests/test_plugin_integration.cpp
echo "" > tests/test_dispatch.cpp
echo "" > tests/test_export.cpp
echo "" > tests/test_traps.cpp
git add -A
git commit -q -m "test: add GoogleTest suite with feature and trap tests"

# Commit 8: docs + unique tokens
echo "" > docs/plugin_contract.md
echo "" > unique_tokens.txt
git add -A
git commit -q -m "chore: finalize fixture with plugin contract doc and unique tokens"

echo "Historia creada con 8 commits:"
git log --oneline
