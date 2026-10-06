"""Tests del .jar (trampa #5 del ecosistema: META-INF/services)."""
from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

ARTIFACTS = Path(__file__).resolve().parent.parent / "artifacts"


@pytest.fixture
def jar_path() -> Path:
    p = ARTIFACTS / "app.jar"
    if not p.exists():
        pytest.skip(f"{p} missing; run build/build-all.sh")
    return p


class TestJarStructure:
    def test_jar_is_valid_zip(self, jar_path: Path) -> None:
        with zipfile.ZipFile(jar_path) as zf:
            names = zf.namelist()
        assert any(n.endswith("CalcularTarifa.class") for n in names)
        assert any(n.endswith("ValidarLicencia.class") for n in names)
        assert any(n.endswith("Sincronizar.class") for n in names)
        assert any(n.endswith("Feature.class") for n in names)

    def test_service_registry_lists_all_features(self, jar_path: Path) -> None:
        with zipfile.ZipFile(jar_path) as zf:
            content = zf.read("META-INF/services/com.fxmin.Feature").decode("utf-8")
        for feature in ("CalcularTarifa", "ValidarLicencia", "Sincronizar"):
            assert feature in content, f"ServiceLoader registry missing {feature}"


class TestJarFeatureLiterals:
    def test_class_files_contain_feature_names(self, jar_path: Path) -> None:
        with zipfile.ZipFile(jar_path) as zf:
            calc = zf.read("com/fxmin/CalcularTarifa.class").decode("latin-1")
            val = zf.read("com/fxmin/ValidarLicencia.class").decode("latin-1")
            sync = zf.read("com/fxmin/Sincronizar.class").decode("latin-1")
        for content, expected in [
            (calc, "calcular_tarifa"),
            (val, "validar_licencia"),
            (sync, "sincronizar"),
        ]:
            assert expected in content, f"class missing literal {expected!r}"


class TestJarPackageTraps:
    def test_jar_without_services_falls_back_to_class_scan(self, tmp_path: Path) -> None:
        # Si el jar no tiene META-INF/services, la skill cae al class scanning.
        bad_jar = tmp_path / "no-services.jar"
        with zipfile.ZipFile(bad_jar, "w") as zf:
            zf.writestr("com/fxmin/CalcularTarifa.class", b"fake")
        with zipfile.ZipFile(bad_jar) as zf:
            names = zf.namelist()
        assert "META-INF/services/com.fxmin.Feature" not in names
        assert any("CalcularTarifa.class" in n for n in names)