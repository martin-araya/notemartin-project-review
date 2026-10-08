#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06ag.
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
git add .gitignore README.md manifest.yml Makefile Dockerfile.test \
        unique_tokens.txt
git commit -q -m "chore: initial scaffold (README, manifest, runner)"

# Commit 2: solution + csproj + build props
git add FxWpf.sln Directory.Build.props
git commit -q -m "build: solution + Directory.Build.props + 3 csproj"

# Commit 3: Core (Models + Interfaces)
git add src/FxWpf.Core/
git commit -q -m "feat(core): Models + Interfaces for clientes/cotizaciones/producto"

# Commit 4: ViewModels (E2 + P1, P2, P5)
git add src/FxWpf.ViewModels/
git commit -q -m "feat(viewmodels): CommunityToolkit.Mvvm with ObservableProperty + RelayCommand"

# Commit 5: Converters (E4 + P3)
git add src/FxWpf.App/Converters/
git commit -q -m "feat(converters): BoolToVisibility + NullToBool + CurrencyConverter"

# Commit 6: Themes (E6) + Styles (E5 + P4)
git add src/FxWpf.App/Themes/ src/FxWpf.App/Styles/
git commit -q -m "feat(themes+styles): merged dictionaries + Style/trigger declarations"

# Commit 7: Views + Templates (E1 + E3 + P6) + App.xaml (E6)
git add src/FxWpf.App/Views/ src/FxWpf.App/App.xaml src/FxWpf.App/App.xaml.cs \
        src/FxWpf.App/AssemblyInfo.cs src/FxWpf.App/FxWpf.App.csproj
git commit -q -m "feat(views): MainWindow + ClientesView + CotizacionesView + PrintPreview + DataTemplates + App.xaml"

# Commit 8: tests + tools + Generated
git add tests/ tools Generated
git commit -q -m "test: xUnit suite for ViewModels + traps + tools + Generated placeholder"

echo "Historia creada con 8 commits:"
git log --oneline