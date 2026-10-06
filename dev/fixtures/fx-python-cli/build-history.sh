#!/usr/bin/env bash
# Build a reproducible git history for fx-python-cli.
# Run from inside the fixture directory.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
  echo "git history already initialized; nothing to do." >&2
  exit 0
fi

git init -q -b main
git config user.email "fxnotes@example.com"
git config user.name "fxnotes dev"

git add pyproject.toml README.md .gitignore src/fxnotes/__init__.py
git commit -q -m "feat: scaffold fxnotes CLI"

git add src/fxnotes/__main__.py src/fxnotes/cli.py src/fxnotes/config.py
git commit -q -m "feat: argparse CLI and config with defaults + env"

git add src/fxnotes/db.py src/fxnotes/events.py
git commit -q -m "feat: SQLite wrapper with retry and event bus"

git add src/fxnotes/commands/__init__.py src/fxnotes/commands/add.py src/fxnotes/commands/list_cmd.py
git commit -q -m "feat: add and list commands with plugin dispatch"

git add src/fxnotes/commands/delete.py
git commit -q -m "feat: delete with soft/hard and ask confirmation"

git add src/fxnotes/commands/export.py
git commit -q -m "feat: export to json/csv"

git add src/fxnotes/plugins/loader.py src/fxnotes/legacy_v1.py
git commit -q -m "chore: plugin loader and legacy v1 module"

git add tests/
git commit -q -m "test: 24 pytest cases covering all R-NN"

echo "history built: $(git rev-list --count HEAD) commits"