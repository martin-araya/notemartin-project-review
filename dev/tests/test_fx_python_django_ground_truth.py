"""Tests del ground truth de fx-python-django (F06p)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-python-django"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-python-django"


def _load_gt() -> dict:
    return json.loads((GT_DIR / "ground_truth.json").read_text(encoding="utf-8"))


class TestGroundTruthShape:
    def test_file_exists(self) -> None:
        assert (GT_DIR / "ground_truth.json").is_file()

    def test_has_4_features(self) -> None:
        gt = _load_gt()
        assert len(gt["features"]) == 4

    def test_features_match_spec(self) -> None:
        gt = _load_gt()
        names = {f["name"] for f in gt["features"]}
        assert "matriculas" in names
        assert "pagos" in names
        assert "certificados" in names
        assert "acciones-de-admin" in names

    def test_each_feature_has_at_least_7_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n >= 7, f"{f['id']}: expected >=7, got {n}"

    def test_has_6_ecosystem_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["traps"]) == 6

    def test_has_6_package_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["package_traps"]) == 6

    def test_has_3_superficial_traps(self) -> None:
        gt = _load_gt()
        assert len(gt.get("superficial_traps", [])) == 3

    def test_each_trap_has_resolution(self) -> None:
        gt = _load_gt()
        for t in gt["traps"] + gt["package_traps"] + gt["superficial_traps"]:
            assert t.get("resolution"), f"trap {t.get('id')} missing resolution"

    def test_outcome_user_sees_present(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for o in f.get("outcomes", []):
                assert o.get("user_sees"), f"{f['id']}/{o['id']} missing user_sees"

    def test_dependencies_listed(self) -> None:
        gt = _load_gt()
        names = {d["name"] for d in gt.get("dependencies", [])}
        assert "Django" in names
        assert "djangorestframework" in names
        assert "celery" in names
        assert "pytest-django" in names

    def test_surfaces_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("surfaces", [])) >= 12


class TestUniqueTokensFile:
    def test_at_least_25_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 25, f"only {len(tokens)} tokens"

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXDJ-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"__pycache__", "node_modules", "dist", ".git", ".pytest_cache"}
        skip_files = {"unique_tokens.txt", "pytest.ini", "requirements.txt"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".py", ".md", ".txt", ".sh", ".yml", ".yaml",
                                    ".json", ".ini"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            rel = path.relative_to(FIXTURE_ROOT).as_posix()
            for tok in tokens:
                assert tok not in text, f"token {tok} found in {rel}"


class TestAllCitesValid:
    def test_all_traces_resolve(self) -> None:
        gt = _load_gt()
        errors = []
        for f in gt["features"]:
            fid = f["id"]
            for ti, t in enumerate(f.get("traces", [])):
                cite = t.get("cite", "")
                if not cite:
                    continue
                errs = check_cite(FIXTURE_ROOT, cite)
                for e in errs:
                    errors.append(f"{fid}/trace[{ti}]: {e}")
        if errors:
            pytest.fail("\n".join(errors[:20]))

    def test_all_decision_points_resolve(self) -> None:
        gt = _load_gt()
        errors = []
        for f in gt["features"]:
            fid = f["id"]
            for di, dp in enumerate(f.get("decision_points", [])):
                cite = f"{dp['file']}:{dp['line']}"
                errs = check_cite(FIXTURE_ROOT, cite)
                for e in errs:
                    errors.append(f"{fid}/dp[{di}]: {e}")
        if errors:
            pytest.fail("\n".join(errors[:20]))


class TestDjangoStructure:
    def test_manage_py(self) -> None:
        assert (FIXTURE_ROOT / "manage.py").is_file()

    def test_requirements_txt(self) -> None:
        assert (FIXTURE_ROOT / "requirements.txt").is_file()

    def test_pytest_ini(self) -> None:
        assert (FIXTURE_ROOT / "pytest.ini").is_file()

    def test_settings_base(self) -> None:
        assert (FIXTURE_ROOT / "fxdjango/settings/base.py").is_file()

    def test_settings_dev(self) -> None:
        assert (FIXTURE_ROOT / "fxdjango/settings/dev.py").is_file()

    def test_settings_prod(self) -> None:
        assert (FIXTURE_ROOT / "fxdjango/settings/prod.py").is_file()

    def test_urls(self) -> None:
        assert (FIXTURE_ROOT / "fxdjango/urls.py").is_file()

    def test_celery(self) -> None:
        assert (FIXTURE_ROOT / "fxdjango/celery.py").is_file()

    def test_enrollments_app(self) -> None:
        for f in ("apps.py", "models.py", "managers.py", "signals.py",
                 "serializers.py", "views.py", "urls.py", "admin.py",
                 "tasks.py"):
            assert (FIXTURE_ROOT / "apps/enrollments" / f).is_file(), f"missing {f}"

    def test_payments_app(self) -> None:
        for f in ("apps.py", "models.py", "managers.py", "signals.py",
                 "serializers.py", "views.py", "urls.py", "admin.py"):
            assert (FIXTURE_ROOT / "apps/payments" / f).is_file(), f"missing {f}"

    def test_certificates_app(self) -> None:
        for f in ("apps.py", "models.py", "serializers.py", "views.py",
                 "urls.py", "admin.py"):
            assert (FIXTURE_ROOT / "apps/certificates" / f).is_file(), f"missing {f}"

    def test_audit_app(self) -> None:
        for f in ("apps.py", "models.py", "admin.py"):
            assert (FIXTURE_ROOT / "apps/audit" / f).is_file(), f"missing {f}"

    def test_templatetags(self) -> None:
        assert (FIXTURE_ROOT / "apps/enrollments/templatetags/enrollment_tags.py").is_file()

    def test_context_processors(self) -> None:
        assert (FIXTURE_ROOT / "apps/enrollments/context_processors.py").is_file()

    def test_tests_dir(self) -> None:
        assert (FIXTURE_ROOT / "tests").is_dir()


class TestEcosystemTraps:
    def test_e01_signals_en_apps_ready(self) -> None:
        apps_py = (FIXTURE_ROOT / "apps/enrollments/apps.py").read_text(encoding="utf-8")
        signals_py = (FIXTURE_ROOT / "apps/enrollments/signals.py").read_text(encoding="utf-8")
        assert "def ready(self):" in apps_py
        assert "from . import signals" in apps_py
        assert "@receiver(post_save" in signals_py

    def test_e02_drf_router_generated_routes(self) -> None:
        urls_py = (FIXTURE_ROOT / "apps/enrollments/urls.py").read_text(encoding="utf-8")
        assert "DefaultRouter()" in urls_py
        assert "router.register" in urls_py
        assert "urlpatterns = router.urls" in urls_py

    def test_e03_custom_manager_queryset(self) -> None:
        managers_py = (FIXTURE_ROOT / "apps/enrollments/managers.py").read_text(encoding="utf-8")
        models_py = (FIXTURE_ROOT / "apps/enrollments/models.py").read_text(encoding="utf-8")
        assert "class EnrollmentQuerySet(models.QuerySet)" in managers_py
        assert "def active(self)" in managers_py
        assert "EnrollmentManager = models.Manager.from_queryset" in managers_py
        assert "objects = EnrollmentManager()" in models_py

    def test_e04_settings_split_por_entorno(self) -> None:
        base_py = (FIXTURE_ROOT / "fxdjango/settings/base.py").read_text(encoding="utf-8")
        dev_py = (FIXTURE_ROOT / "fxdjango/settings/dev.py").read_text(encoding="utf-8")
        prod_py = (FIXTURE_ROOT / "fxdjango/settings/prod.py").read_text(encoding="utf-8")
        assert "INSTALLED_APPS" in base_py
        assert "DEBUG = True" in dev_py
        assert "from .base import *" in dev_py
        assert "from .base import *" in prod_py
        assert "DEBUG = False" in prod_py

    def test_e05_admin_action_no_public_route(self) -> None:
        audit_admin = (FIXTURE_ROOT / "apps/audit/admin.py").read_text(encoding="utf-8")
        assert "@admin.action" in audit_admin
        assert "export_csv" in audit_admin
        assert "mark_reviewed" in audit_admin
        urls_py = (FIXTURE_ROOT / "fxdjango/urls.py").read_text(encoding="utf-8")
        assert "admin.site.urls" in urls_py
        assert "api/enrollments" in urls_py

    def test_e06_template_tags_y_context_processors(self) -> None:
        base_py = (FIXTURE_ROOT / "fxdjango/settings/base.py").read_text(encoding="utf-8")
        enrollment_tags = (FIXTURE_ROOT / "apps/enrollments/templatetags/enrollment_tags.py").read_text(encoding="utf-8")
        enrollment_ctx = (FIXTURE_ROOT / "apps/enrollments/context_processors.py").read_text(encoding="utf-8")
        assert "apps.enrollments.context_processors.enrollment_counts" in base_py
        assert "@register.simple_tag" in enrollment_tags
        assert "enrollment_counts" in enrollment_ctx


class TestPackageTraps:
    def test_p01_signals_sin_transaction_envelope(self) -> None:
        signals_py = (FIXTURE_ROOT / "apps/enrollments/signals.py").read_text(encoding="utf-8")
        assert "transaction.on_commit" not in signals_py
        assert "@receiver(post_save" in signals_py

    def test_p02_queryset_metodo_sin_indice(self) -> None:
        managers_py = (FIXTURE_ROOT / "apps/payments/managers.py").read_text(encoding="utf-8")
        models_py = (FIXTURE_ROOT / "apps/payments/models.py").read_text(encoding="utf-8")
        assert "def completed(self)" in managers_py
        assert 'models.Index(fields=["status"])' in models_py
        assert 'models.Index(fields=["enrollment"]' not in models_py

    def test_p03_admin_action_sin_permission_check(self) -> None:
        audit_admin = (FIXTURE_ROOT / "apps/audit/admin.py").read_text(encoding="utf-8")
        bloque = audit_admin[audit_admin.index("def export_csv"):audit_admin.index("def mark_reviewed")]
        assert "is_superuser" not in bloque
        assert "has_perm" not in bloque

    def test_p04_celery_eager_swallows_exceptions(self) -> None:
        celery_py = (FIXTURE_ROOT / "fxdjango/celery.py").read_text(encoding="utf-8")
        dev_py = (FIXTURE_ROOT / "fxdjango/settings/dev.py").read_text(encoding="utf-8")
        assert "memory://" in celery_py
        assert "CELERY_TASK_ALWAYS_EAGER = True" in dev_py

    def test_p05_router_basename_payment(self) -> None:
        urls_py = (FIXTURE_ROOT / "apps/payments/urls.py").read_text(encoding="utf-8")
        assert 'basename="payment"' in urls_py
        assert "router.register" in urls_py

    def test_p06_secret_key_env_or_default(self) -> None:
        base_py = (FIXTURE_ROOT / "fxdjango/settings/base.py").read_text(encoding="utf-8")
        assert "SECRET_KEY = os.environ.get" in base_py
        assert "FXDJ_SECRET_KEY" in base_py


class TestSuperficialTraps:
    def test_s01_legacy_certificate_viewset_dead(self) -> None:
        views_py = (FIXTURE_ROOT / "apps/certificates/views.py").read_text(encoding="utf-8")
        urls_py = (FIXTURE_ROOT / "apps/certificates/urls.py").read_text(encoding="utf-8")
        assert "class LegacyCertificateViewSet" in views_py
        assert "LegacyCertificateViewSet" not in urls_py

    def test_s02_signal_handler_dead(self) -> None:
        signals_py = (FIXTURE_ROOT / "apps/payments/signals.py").read_text(encoding="utf-8")
        assert "def handler_pago_fallido" in signals_py
        # No debe estar conectado como signal
        bloque_handler = signals_py.split("def handler_pago_fallido")[1]
        assert "@receiver" not in bloque_handler

    def test_s03_template_tag_dead(self) -> None:
        tags_py = (FIXTURE_ROOT / "apps/certificates/templatetags/certificate_tags.py").read_text(encoding="utf-8")
        assert "def format_certificate_id" in tags_py


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-python-django" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_requirements_has_django(self) -> None:
        requirements = (FIXTURE_ROOT / "requirements.txt").read_text(encoding="utf-8")
        assert "Django" in requirements
        assert "djangorestframework" in requirements
        assert "celery" in requirements

    def test_pytest_ini_has_django_settings(self) -> None:
        ini = (FIXTURE_ROOT / "pytest.ini").read_text(encoding="utf-8")
        assert "DJANGO_SETTINGS_MODULE" in ini
        assert "fxdjango.settings.dev" in ini

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 25
        for tok in tokens:
            assert tok.startswith("NPRGT-FXDJ-")