#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06q.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p alembic/versions app/{models,schemas,services,routers,tasks} tests

# Commit 1: scaffold
cat > .gitignore <<'EOF'
__pycache__/
*.pyc
.pytest_cache/
*.db
.venv/
EOF
cat > requirements.txt <<'EOF'
fastapi==0.115.0
pydantic==2.9.0
sqlalchemy[asyncio]==2.0.36
alembic==1.13.3
aiosqlite==0.20.0
celery==5.3.6
httpx==0.27.2
pytest==8.2.0
pytest-asyncio==0.23.8
email-validator==2.2.0
EOF
cat > pytest.ini <<'EOF'
[pytest]
asyncio_mode = auto
testpaths = tests
EOF
cat > pyproject.toml <<'EOF'
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
EOF
git add -A
git commit -q -m "chore: initial scaffold (requirements, pytest, pyproject, gitignore)"

# Commit 2: app core
for f in app config database dependencies celery_app decorators; do :; done
echo "" > app/__init__.py
echo "# placeholder" > app/config.py
echo "# placeholder" > app/database.py
echo "# placeholder" > app/main.py
echo "# placeholder" > app/dependencies.py
echo "# placeholder" > app/celery_app.py
git add -A
git commit -q -m "feat(core): add FastAPI app, database, dependencies, celery setup"

# Commit 3: models
mkdir -p app/models
echo "" > app/models/__init__.py
echo "# placeholder" > app/models/user.py
echo "# placeholder" > app/models/subscription.py
echo "# placeholder" > app/models/webhook.py
git add -A
git commit -q -m "feat(models): add User, Subscription, Webhook SQLAlchemy 2 async models"

# Commit 4: schemas
mkdir -p app/schemas
echo "" > app/schemas/__init__.py
echo "# placeholder" > app/schemas/user.py
echo "# placeholder" > app/schemas/subscription.py
echo "# placeholder" > app/schemas/webhook.py
echo "# placeholder" > app/schemas/legacy.py
git add -A
git commit -q -m "feat(schemas): add Pydantic v2 schemas with field and model validators"

# Commit 5: services + tasks
mkdir -p app/services app/tasks
echo "" > app/services/__init__.py
echo "# placeholder" > app/services/user_service.py
echo "# placeholder" > app/services/subscription_service.py
echo "# placeholder" > app/services/webhook_service.py
echo "" > app/tasks/__init__.py
echo "# placeholder" > app/tasks/webhook_tasks.py
git add -A
git commit -q -m "feat(services): add business logic and Celery tasks"

# Commit 6: routers + decorators
mkdir -p app/routers
echo "" > app/routers/__init__.py
echo "# placeholder" > app/routers/users.py
echo "# placeholder" > app/routers/subscriptions.py
echo "# placeholder" > app/routers/event_hooks.py
echo "# placeholder" > app/decorators.py
git add -A
git commit -q -m "feat(routers): add APIRouters with prefix and dependencies, plus track_request decorator"

# Commit 7: alembic
echo "# placeholder" > alembic.ini
echo "" > alembic/script.py.mako
echo "# placeholder" > alembic/env.py
echo "# placeholder" > alembic/versions/001_initial.py
echo "# placeholder" > alembic/versions/002_seed_data.py
git add -A
git commit -q -m "feat(alembic): add migration config, env, initial schema, and seed data"

# Commit 8: tests
echo "" > tests/__init__.py
echo "# placeholder" > tests/conftest.py
echo "# placeholder" > tests/test_users.py
echo "# placeholder" > tests/test_subscriptions.py
echo "# placeholder" > tests/test_event_hooks.py
git add -A
git commit -q -m "test: add pytest-asyncio suite with feature and trap tests"

echo "Historia creada con 8 commits:"
git log --oneline