#!/usr/bin/env bash
# Genera una historia git reproducible de 8 commits para el fixture F06p.
set -euo pipefail

cd "$(dirname "$0")"

if [ -d .git ]; then
    echo "ERROR: ya existe un repositorio git aqui; no se sobreescribe." >&2
    exit 1
fi

git init -q -b main
git config user.name "Fixture Builder"
git config user.email "fixture@local"

mkdir -p fxdjango/settings apps/{enrollments,payments,certificates,audit}/{migrations,templatetags} tests

# Commit 1: scaffold
cat > .gitignore <<'EOF'
__pycache__/
*.pyc
*.sqlite3
.pytest_cache/
.coverage
db.sqlite3
EOF
cat > requirements.txt <<'EOF'
Django==5.0.6
djangorestframework==3.15.1
celery==5.3.6
pytest==8.2.0
pytest-django==4.8.0
EOF
cat > pytest.ini <<'EOF'
[pytest]
DJANGO_SETTINGS_MODULE = fxdjango.settings.dev
python_files = test_*.py
EOF
git add -A
git commit -q -m "chore: initial scaffold (requirements, pytest config, gitignore)"

# Commit 2: settings + urls + celery
mkdir -p fxdjango/settings
for f in base settings dev prod; do
    if [ "$f" = "base" ] || [ "$f" = "settings" ]; then continue; fi
done
echo "" > fxdjango/__init__.py
echo "" > fxdjango/settings/__init__.py
echo "# placeholder" > fxdjango/settings/base.py
echo "# placeholder" > fxdjango/settings/dev.py
echo "# placeholder" > fxdjango/settings/prod.py
echo "# placeholder" > fxdjango/urls.py
echo "# placeholder" > fxdjango/celery.py
echo "# placeholder" > fxdjango/wsgi.py
echo "# placeholder" > fxdjango/asgi.py
echo "# placeholder" > manage.py
git add -A
git commit -q -m "feat(project): add Django settings split and root urls"

# Commit 3: enrollments app
echo "" > apps/__init__.py
echo "" > apps/enrollments/__init__.py
echo "# placeholder" > apps/enrollments/apps.py
echo "# placeholder" > apps/enrollments/models.py
echo "# placeholder" > apps/enrollments/managers.py
echo "# placeholder" > apps/enrollments/signals.py
echo "# placeholder" > apps/enrollments/views.py
echo "# placeholder" > apps/enrollments/serializers.py
echo "# placeholder" > apps/enrollments/urls.py
echo "# placeholder" > apps/enrollments/admin.py
echo "# placeholder" > apps/enrollments/tasks.py
echo "" > apps/enrollments/templatetags/__init__.py
echo "# placeholder" > apps/enrollments/templatetags/enrollment_tags.py
echo "# placeholder" > apps/enrollments/context_processors.py
touch apps/enrollments/migrations/__init__.py
git add -A
git commit -q -m "feat(enrollments): add enrollment app with custom manager, signals, template tag, context processor"

# Commit 4: payments app
for f in apps payments __init__ apps models managers signals views serializers urls admin tasks migrations templatetags; do :; done
mkdir -p apps/payments/migrtations apps/payments/templatetags
mkdir -p apps/payments/migrations
echo "" > apps/payments/__init__.py
echo "# placeholder" > apps/payments/apps.py
echo "# placeholder" > apps/payments/models.py
echo "# placeholder" > apps/payments/managers.py
echo "# placeholder" > apps/payments/signals.py
echo "# placeholder" > apps/payments/views.py
echo "# placeholder" > apps/payments/serializers.py
echo "# placeholder" > apps/payments/urls.py
echo "# placeholder" > apps/payments/admin.py
echo "# placeholder" > apps/payments/tasks.py
echo "" > apps/payments/templatetags/__init__.py
echo "# placeholder" > apps/payments/templatetags/payment_tags.py
echo "# placeholder" > apps/payments/context_processors.py
touch apps/payments/migrations/__init__.py
git add -A
git commit -q -m "feat(payments): add payment app with signals and template tag"

# Commit 5: certificates app
mkdir -p apps/certificates/migrations apps/certificates/templatetags
echo "" > apps/certificates/__init__.py
echo "# placeholder" > apps/certificates/apps.py
echo "# placeholder" > apps/certificates/models.py
echo "# placeholder" > apps/certificates/managers.py
echo "# placeholder" > apps/certificates/signals.py
echo "# placeholder" > apps/certificates/views.py
echo "# placeholder" > apps/certificates/serializers.py
echo "# placeholder" > apps/certificates/urls.py
echo "# placeholder" > apps/certificates/admin.py
echo "# placeholder" > apps/certificates/tasks.py
echo "" > apps/certificates/templatetags/__init__.py
echo "# placeholder" > apps/certificates/templatetags/certificate_tags.py
echo "# placeholder" > apps/certificates/context_processors.py
touch apps/certificates/migrations/__init__.py
git add -A
git commit -q -m "feat(certificates): add certificate app with legacy dead viewset"

# Commit 6: audit app
mkdir -p apps/audit/migrations apps/audit/templatetags
echo "" > apps/audit/__init__.py
echo "# placeholder" > apps/audit/apps.py
echo "# placeholder" > apps/audit/models.py
echo "# placeholder" > apps/audit/signals.py
echo "# placeholder" > apps/audit/admin.py
echo "# placeholder" > apps/audit/views.py
touch apps/audit/migrations/__init__.py
git add -A
git commit -q -m "feat(audit): add audit app with admin actions"

# Commit 7: tests
echo "" > tests/__init__.py
echo "# placeholder" > tests/conftest.py
echo "# placeholder" > tests/test_enrollments.py
echo "# placeholder" > tests/test_payments.py
echo "# placeholder" > tests/test_certificates.py
echo "# placeholder" > tests/test_admin_actions.py
git add -A
git commit -q -m "test: add pytest-django suite with feature and trap tests"

echo "Historia creada con 8 commits:"
git log --oneline