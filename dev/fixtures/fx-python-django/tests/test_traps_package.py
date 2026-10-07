"""Tests for the 6 package traps planted in the fixture."""
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parents[1]


def test_p01_signals_sin_transaction_envelope():
    signals_py = (FIXTURE_ROOT / "apps/enrollments/signals.py").read_text(encoding="utf-8")
    # El receiver NO envuelve en transaction.on_commit
    assert "transaction.on_commit" not in signals_py
    assert "@receiver(post_save" in signals_py


def test_p02_queryset_metodo_sin_indice():
    managers_py = (FIXTURE_ROOT / "apps/payments/managers.py").read_text(encoding="utf-8")
    models_py = (FIXTURE_ROOT / "apps/payments/models.py").read_text(encoding="utf-8")
    assert "def completed(self)" in managers_py
    # El manager expone .completed() pero el modelo solo tiene Index en
    # el campo status (no en enrollment que es el filtro real).
    assert 'models.Index(fields=["status"])' in models_py
    assert 'models.Index(fields=["enrollment"]' not in models_py


def test_p03_admin_action_sin_permission_check():
    audit_admin = (FIXTURE_ROOT / "apps/audit/admin.py").read_text(encoding="utf-8")
    # La action export_csv NO verifica is_superuser
    bloque = audit_admin[audit_admin.index("def export_csv"):audit_admin.index("def mark_reviewed")]
    assert "is_superuser" not in bloque


def test_p04_celery_eager_swallows_exceptions():
    celery_py = (FIXTURE_ROOT / "fxdjango/celery.py").read_text(encoding="utf-8")
    dev_py = (FIXTURE_ROOT / "fxdjango/settings/dev.py").read_text(encoding="utf-8")
    assert "memory://" in celery_py
    assert "CELERY_TASK_ALWAYS_EAGER = True" in dev_py


def test_p05_router_basename_payment():
    urls_py = (FIXTURE_ROOT / "apps/payments/urls.py").read_text(encoding="utf-8")
    assert 'basename="payment"' in urls_py
    assert "router.register" in urls_py


def test_p06_secret_key_env_or_default():
    base_py = (FIXTURE_ROOT / "fxdjango/settings/base.py").read_text(encoding="utf-8")
    assert "SECRET_KEY = os.environ.get" in base_py
    assert "FXDJ_SECRET_KEY" in base_py