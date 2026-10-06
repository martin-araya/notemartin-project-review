#!/usr/bin/env bash
# Build a reproducible git history for fx-ts-agent-extension.
# Run from inside the fixture directory.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
  echo "git history already initialized; nothing to do." >&2
  exit 0
fi

git init -q -b main
git config user.email "fxagent@example.com"
git config user.name "fxagent dev"

# Commit 1: scaffold
mkdir -p src/host/vscode-shim src/host/providers src/host/mcp src/webview/ui locales tests
git add package.json tsconfig.json vitest.config.ts esbuild.config.mjs manifest.yml README.md .gitignore
git commit -q -m "chore: scaffold package.json, tsconfig, esbuild + vitest configs"

# Commit 2: vscode-shim
git add src/host/vscode-shim/
git commit -q -m "feat: vscode-shim with window, commands, webview"

# Commit 3: modes
git add src/host/modes.ts
git commit -q -m "feat: 3 modes (plan, code, ask) with prompts and tool groups"

# Commit 4: tools
git add src/host/tools.ts
git commit -q -m "feat: 6 tools with approval flow (read_file, list_dir, search_code, run_terminal_cmd, ask_user, propose_plan)"

# Commit 5: skills
git add src/host/skills.ts locales/
git commit -q -m "feat: skill loader with 2 paths and frontmatter merge"

# Commit 6: providers + mcp + context + i18n
git add src/host/providers/ src/host/mcp/ src/host/context.ts src/host/i18n.ts
git commit -q -m "feat: provider factory with dynamic import, mcp client, context condensation, i18n"

# Commit 7: messages
git add src/host/messages.ts
git commit -q -m "feat: 12 message types dispatcher (>5000 lines)"

# Commit 8: extension + tests
git add src/host/extension.ts src/webview/ tests/
git commit -q -m "feat: extension entry point + vitest suite (162 tests)"

echo "history built: $(git rev-list --count HEAD) commits"
