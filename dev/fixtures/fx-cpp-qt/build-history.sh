#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06z.
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
*.o
*.so
*.a
*.exe
moc_*.cpp
moc_*.h
qrc_*.cpp
ui_*.h
.qmake.stash
EOF
echo "# fx-cpp-qt" > README.md
git add -A
git commit -q -m "chore: initial scaffold (README, .gitignore)"

# Commit 2: cmake
mkdir -p cmake
cat > cmake/QtCompilerWarnings.cmake <<'EOF'
function(qtapp_set_warnings target)
    target_compile_options(\${target} PRIVATE
        -Wall -Wextra -Wpedantic -Wshadow -Wnon-virtual-dtor
        -Wno-unused-parameter
    )
endfunction()
EOF
echo "CMakeLists.txt stub" > CMakeLists.txt
git add -A
git commit -q -m "build: add cmake config (QtCompilerWarnings) and root CMakeLists"

# Commit 3: headers
mkdir -p include/qtapp/util
cat > include/qtapp/version.h <<'EOF'
#pragma once
#define QTAPP_VERSION_MAJOR 0
#define QTAPP_VERSION_MINOR 1
#define QTAPP_VERSION_PATCH 0
#define QTAPP_VERSION_STRING "0.1.0"
EOF
echo "" > include/qtapp/editor.h
echo "" > include/qtapp/preferences.h
echo "" > include/qtapp/exporter.h
echo "" > include/qtapp/main_window.h
echo "" > include/qtapp/preferences_proxy.h
git add -A
git commit -q -m "feat(headers): add QObject headers (Editor, Preferences, Exporter, MainWindow, Proxy)"

# Commit 4: sources
mkdir -p src
echo "" > src/main.cpp
echo "" > src/editor.cpp
echo "" > src/preferences.cpp
echo "" > src/exporter.cpp
echo "" > src/main_window.cpp
echo "" > src/preferences_proxy.cpp
echo "" > src/legacy_helpers.cpp
git add -A
git commit -q -m "feat(sources): add Qt 6 source files with Q_OBJECT implementations"

# Commit 5: ui + qml
mkdir -p ui qml
echo "" > ui/main_window.ui
echo "" > ui/preferences_form.ui
echo "" > qml/PreferencesPage.qml
echo "" > qml/ThemeSwitcher.qml
git add -A
git commit -q -m "feat(ui): add Qt Designer .ui files and QML files"

# Commit 6: resources
mkdir -p resources/icons resources/styles
echo "" > resources/icons/save.svg
echo "" > resources/icons/open.svg
echo "" > resources/icons/export.svg
echo "" > resources/styles/app.qss
git add -A
git commit -q -m "feat(resources): add icons and styles registered via AUTORCC"

# Commit 7: tests
mkdir -p tests
echo "" > tests/test_main.cpp
echo "" > tests/CMakeLists.txt
echo "" > tests/test_runner.py
git add -A
git commit -q -m "test: add Qt Test suite with 29 tests and Python runner"

# Commit 8: docs + manifest
mkdir -p docs
echo "" > docs/qt_build.md
echo "" > docs/signal_slot_cheatsheet.md
git add -A
git commit -q -m "chore: finalize fixture with docs and manifest"

echo "Historia creada con 8 commits:"
git log --oneline
