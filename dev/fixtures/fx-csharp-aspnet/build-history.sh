#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06o.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p src/Domain/{Pedidos,Facturacion,Reintentos} src/Infrastructure/{Persistence/Configurations,Mediator,Background} src/Features/{Pedidos/{Commands,Queries},Facturacion/{Commands,Queries},Reintentos} src/Web/{Endpoints,Middleware} tests/FxAspNet.Tests/{Fixtures,Features,Trampas}

# Commit 1: scaffold
cat > .gitignore <<'EOF'
bin/
obj/
*.user
.vs/
EOF
git add -A
git commit -q -m "chore: initial scaffold"

# Commit 2: csproj
cat > FxAspNet.csproj <<'EOF'
<Project Sdk="Microsoft.NET.Sdk.Web">
</Project>
EOF
git add -A
git commit -q -m "chore: add web project file"

# Commit 3: domain entities
echo "// domain placeholder" > src/Domain/Pedidos/.gitkeep
echo "// domain placeholder" > src/Domain/Facturacion/.gitkeep
echo "// domain placeholder" > src/Domain/Reintentos/.gitkeep
git add -A
git commit -q -m "feat(domain): add entity classes"

# Commit 4: EF Core
echo "// persistence placeholder" > src/Infrastructure/Persistence/.gitkeep
git add -A
git commit -q -m "feat(persistence): add EF Core DbContext and configurations"

# Commit 5: Mediator + Background
echo "// mediator placeholder" > src/Infrastructure/Mediator/.gitkeep
echo "// background placeholder" > src/Infrastructure/Background/.gitkeep
git add -A
git commit -q -m "feat(infrastructure): add mediator registration and background service"

# Commit 6: features
echo "// features placeholder" > src/Features/Pedidos/Commands/.gitkeep
echo "// features placeholder" > src/Features/Pedidos/Queries/.gitkeep
echo "// features placeholder" > src/Features/Facturacion/Commands/.gitkeep
echo "// features placeholder" > src/Features/Facturacion/Queries/.gitkeep
echo "// features placeholder" > src/Features/Reintentos/.gitkeep
git add -A
git commit -q -m "feat(features): add CQRS commands, queries and handlers"

# Commit 7: web + Program
echo "// web placeholder" > src/Web/Endpoints/.gitkeep
echo "// web placeholder" > src/Web/Middleware/.gitkeep
git add -A
git commit -q -m "feat(web): add minimal API endpoints and middleware"

# Commit 8: tests
echo "// tests placeholder" > tests/FxAspNet.Tests/.gitkeep
git add -A
git commit -q -m "test: add xunit suite with WebApplicationFactory"

echo "Historia creada con 8 commits:"
git log --oneline