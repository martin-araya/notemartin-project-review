"""Tests del ground truth de fx-minified (F06e)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-minified"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-minified"


def _load_gt() -> dict:
    return json.loads((GT_DIR / "ground_truth.json").read_text(encoding="utf-8"))


class TestGroundTruthShape:
    def test_file_exists(self) -> None:
        assert (GT_DIR / "ground_truth.json").is_file()

    def test_has_3_features(self) -> None:
        gt = _load_gt()
        assert len(gt["features"]) == 3

    def test_features_match_spec(self) -> None:
        gt = _load_gt()
        names = {f["name"] for f in gt["features"]}
        assert names == {"calcular-tarifa", "validar-licencia", "sincronizar"}

    def test_each_feature_has_min_6_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n >= 6, f"{f['id']}: only {n} outcomes"

    def test_has_6_ecosystem_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["traps"]) == 6

    def test_has_6_package_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["package_traps"]) == 6

    def test_surfaces_for_each_artifact(self) -> None:
        gt = _load_gt()
        names = {s["artifact"] for s in gt["entry_points"]}
        assert "bundle.js" in names
        assert "bundle.min.js" in names
        assert "app.asar" in names
        assert "app.pyc" in names
        assert "app.jar" in names
        assert "app" in names


class TestUniqueTokensFile:
    def test_at_least_5_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 5

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXMIN-")


class TestMonorepoStructure:
    def test_source_directories_exist(self) -> None:
        assert (FIXTURE_ROOT / "src/ts").is_dir()
        assert (FIXTURE_ROOT / "src/js").is_dir()
        assert (FIXTURE_ROOT / "src/py").is_dir()
        assert (FIXTURE_ROOT / "src/java").is_dir()
        assert (FIXTURE_ROOT / "src/go").is_dir()

    def test_build_scripts_exist(self) -> None:
        assert (FIXTURE_ROOT / "build/build-bundle-with-sourcemap.mjs").is_file()
        assert (FIXTURE_ROOT / "build/build-bundle-without-sourcemap.mjs").is_file()
        assert (FIXTURE_ROOT / "build/build-asar.mjs").is_file()
        assert (FIXTURE_ROOT / "build/build-pyc.sh").is_file()
        assert (FIXTURE_ROOT / "build/build-jar.sh").is_file()
        assert (FIXTURE_ROOT / "build/build-go.sh").is_file()
        assert (FIXTURE_ROOT / "build/build-all.sh").is_file()
        assert (FIXTURE_ROOT / "build/all-tests.sh").is_file()

    def test_manifests_exist(self) -> None:
        manifests = list((FIXTURE_ROOT / "manifests").iterdir())
        names = {m.name for m in manifests}
        assert "bundle.js.with-sourcemap.json" in names
        assert "bundle.min.json.literal" in names
        assert "app.asar.json" in names
        assert "app.pyc.json" in names
        assert "app.jar.json" in names
        assert "app.go.json" in names

    def test_maven_service_loader_file(self) -> None:
        """META-INF/services en el jar (trampa #5). El archivo esta en
        src/META-INF/services/, NO adentro de com/fxmin/."""
        service_file = (FIXTURE_ROOT / "src/META-INF/services/com.fxmin.Feature")
        assert service_file.is_file()
        content = service_file.read_text(encoding="utf-8")
        assert "CalcularTarifa" in content
        assert "ValidarLicencia" in content
        assert "Sincronizar" in content

    def test_go_module_file(self) -> None:
        """go.mod es requerido para ``go build``."""
        assert (FIXTURE_ROOT / "src/go/go.mod").is_file()