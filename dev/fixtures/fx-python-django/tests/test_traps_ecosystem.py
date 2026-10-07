"""Tests for the 6 ecosystem traps planted in the fixture."""
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parents[1]


def test_e01_signals_conectados_en_apps_py_ready():
    apps_py = (FIXTURE_ROOT / "apps/enrollments/apps.py").read_text(encoding="utf-8")
    signals_py = (FIXTURE_ROOT / "apps/enrollments/signals.py").read_text(encoding="utf-8")
    assert "def ready(self):" in apps_py
    assert "from . import signals" in apps_py
    assert "@receiver(post_save" in signals_py


def test_e02_drf_router_generated_routes():
    urls_py = (FIXTURE_ROOT / "apps/enrollments/urls.py").read_text(encoding="utf-8")
    assert "DefaultRouter()" in urls_py
    assert "router.register" in urls_py
    assert "urlpatterns = router.urls" in urls_py


def test_e03_custom_manager_queryset():
    managers_py = (FIXTURE_ROOT / "apps/enrollments/managers.py").read_text(encoding="utf-8")
    models_py = (FIXTURE_ROOT / "apps/enrollments/models.py").read_text(encoding="utf-8")
    assert "class EnrollmentQuerySet(models.QuerySet)" in managers_py
    assert "def active(self)" in managers_py
    assert "EnrollmentManager = models.Manager.from_queryset" in managers_py
    assert "objects = EnrollmentManager()" in models_py


def test_e04_settings_split_por_entorno():
    base_py = (FIXTURE_ROOT / "fxdjango/settings/base.py").read_text(encoding="utf-8")
    dev_py = (FIXTURE_ROOT / "fxdjango/settings/dev.py").read_text(encoding="utf-8")
    prod_py = (FIXTURE_ROOT / "fxdjango/settings/prod.py").read_text(encoding="utf-8")
    assert "INSTALLED_APPS" in base_py
    assert "DEBUG = True" in dev_py
    assert "from .base import *" in dev_py
    assert "from .base import *" in prod_py
    assert "DEBUG = False" in prod_py


def test_e05_admin_action_no_public_route():
    audit_admin = (FIXTURE_ROOT / "apps/audit/admin.py").read_text(encoding="utf-8")
    assert "@admin.action" in audit_admin
    assert "export_csv" in audit_admin
    assert "mark_reviewed" in audit_admin
    # Las acciones NO estan en urls.py del proyecto
    urls_py = (FIXTURE_ROOT / "fxdjango/urls.py").read_text(encoding="utf-8")
    assert "admin.site.urls" in urls_py
    assert "api/enrollments" in urls_py  # las APIs usan router DRF, no exponen admin actions


def test_e06_template_tags_y_context_processors():
    base_py = (FIXTURE_ROOT / "fxdjango/settings/base.py").read_text(encoding="utf-8")
    enrollment_tags = (FIXTURE_ROOT / "apps/enrollments/templatetags/enrollment_tags.py").read_text(encoding="utf-8")
    enrollment_ctx = (FIXTURE_ROOT / "apps/enrollments/context_processors.py").read_text(encoding="utf-8")
    assert "apps.enrollments.context_processors.enrollment_counts" in base_py
    assert "@register.simple_tag" in enrollment_tags
    assert "enrollment_counts" in enrollment_ctx