"""Tests for the 3 superficial traps planted in the fixture."""
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parents[1]


def test_s01_legacy_certificate_viewset_dead():
    views_py = (FIXTURE_ROOT / "apps/certificates/views.py").read_text(encoding="utf-8")
    urls_py = (FIXTURE_ROOT / "apps/certificates/urls.py").read_text(encoding="utf-8")
    assert "class LegacyCertificateViewSet" in views_py
    assert "LegacyCertificateViewSet" not in urls_py


def test_s02_signal_handler_dead():
    signals_py = (FIXTURE_ROOT / "apps/payments/signals.py").read_text(encoding="utf-8")
    assert "def handler_pago_fallido" in signals_py
    assert "@receiver" not in signals_py.split("def handler_pago_fallido")[1]


def test_s03_template_tag_dead():
    tags_py = (FIXTURE_ROOT / "apps/certificates/templatetags/certificate_tags.py").read_text(encoding="utf-8")
    assert "def format_certificate_id" in tags_py