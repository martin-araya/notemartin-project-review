"""Tests del ground truth de fx-java-micronaut (F06c)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-java-micronaut"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-java-micronaut"


def _load_gt() -> dict:
    return json.loads((GT_DIR / "ground_truth.json").read_text(encoding="utf-8"))


class TestGroundTruthShape:
    def test_file_exists(self) -> None:
        assert (GT_DIR / "ground_truth.json").is_file()

    def test_has_4_features(self) -> None:
        gt = _load_gt()
        assert len(gt["features"]) >= 4

    def test_each_feature_has_min_6_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n >= 6, f"{f['id']}: only {n} outcomes"

    def test_has_6_ecosystem_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["traps"]) >= 6

    def test_has_6_package_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["package_traps"]) >= 6

    def test_features_are_the_documented_ones(self) -> None:
        gt = _load_gt()
        names = {f["name"] for f in gt["features"]}
        assert "alta-cliente" in names
        assert "consulta-score-externo" in names
        assert "cierre-diario-programado" in names
        assert "notificar-evento" in names

    def test_surfaces_includes_http_and_events(self) -> None:
        gt = _load_gt()
        kinds = {s["kind"] for s in gt["surfaces"]}
        assert "http" in kinds
        assert "event" in kinds
        assert "scheduled" in kinds
        assert "client" in kinds

    def test_unique_tokens_not_in_src(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXMICRO-")
        # Walk src/ and ensure no token appears.
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in (".java", ".yml", ".sql", ".xml", ".kts", ".properties", ".md"):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            for tok in tokens:
                if tok in text:
                    rel = path.relative_to(FIXTURE_ROOT).as_posix()
                    assert "unique_tokens" in rel, f"token {tok} found in {rel}"


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


class TestJavaSourceStructure:
    def test_uses_micronaut(self) -> None:
        src_main = FIXTURE_ROOT / "src/main/java"
        assert src_main.is_dir()
        java_files = list(src_main.rglob("*.java"))
        assert len(java_files) > 10
        # All have `package com.fxmicronaut`.
        for jf in java_files[:5]:
            content = jf.read_text(encoding="utf-8")
            assert content.startswith("package com.fxmicronaut")

    def test_uses_requires_annotation(self) -> None:
        factory = FIXTURE_ROOT / "src/main/java/com/fxmicronaut/factory/DataSourceFactory.java"
        assert factory.is_file()
        content = factory.read_text(encoding="utf-8")
        assert "@Requires" in content
        assert "@Factory" in content

    def test_uses_client_annotation(self) -> None:
        client = FIXTURE_ROOT / "src/main/java/com/fxmicronaut/client/ScoreClient.java"
        assert client.is_file()
        content = client.read_text(encoding="utf-8")
        assert "@Client" in content
        # Es interface (no class).
        assert "public interface" in content
        assert "public class" not in content

    def test_uses_event_listener_annotation(self) -> None:
        notifier = FIXTURE_ROOT / "src/main/java/com/fxmicronaut/services/NotifierService.java"
        assert notifier.is_file()
        content = notifier.read_text(encoding="utf-8")
        assert "@EventListener" in content

    def test_uses_scheduled_annotation(self) -> None:
        scheduler = FIXTURE_ROOT / "src/main/java/com/fxmicronaut/scheduler/DailyCloseScheduler.java"
        assert scheduler.is_file()
        content = scheduler.read_text(encoding="utf-8")
        assert "@Scheduled" in content
        # La expresion cron viene de la configuracion.
        assert "cron = \"${daily-close.cron}\"" in content

    def test_flyway_migrations_exist(self) -> None:
        v1 = FIXTURE_ROOT / "src/main/resources/db/migration/V1__create_clientes.sql"
        v2 = FIXTURE_ROOT / "src/main/resources/db/migration/V2__add_score_extra.sql"
        assert v1.is_file()
        assert v2.is_file()
        v1_content = v1.read_text(encoding="utf-8")
        v2_content = v2.read_text(encoding="utf-8")
        assert "clientes" in v1_content
        assert "scores" in v1_content
        assert "categoria_ajustada" in v2_content

    def test_application_yml_profiles_exist(self) -> None:
        res = FIXTURE_ROOT / "src/main/resources"
        assert (res / "application.yml").is_file()
        assert (res / "application-dev.yml").is_file()
        assert (res / "application-test.yml").is_file()

    def test_jdk_21_in_build(self) -> None:
        build = FIXTURE_ROOT / "build.gradle.kts"
        content = build.read_text(encoding="utf-8")
        assert "21" in content
        assert "micronaut" in content.lower()
        assert "flyway" in content.lower()

    def test_gradle_daemon_disabled(self) -> None:
        props = FIXTURE_ROOT / "gradle.properties"
        content = props.read_text(encoding="utf-8")
        assert "org.gradle.daemon=false" in content


class TestUniqueTokensFile:
    def test_at_least_20_tokens(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20
