"""Tests del ground truth de fx-kotlin-android (F06ac)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-kotlin-android"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-kotlin-android"


def _load_gt() -> dict:
    return json.loads((GT_DIR / "ground_truth.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Shape
# ---------------------------------------------------------------------------


class TestGroundTruthShape:
    def test_file_exists(self) -> None:
        assert (GT_DIR / "ground_truth.json").is_file()

    def test_has_4_features(self) -> None:
        gt = _load_gt()
        assert len(gt["features"]) == 4

    def test_features_match_spec(self) -> None:
        gt = _load_gt()
        names = {f["name"] for f in gt["features"]}
        assert "escaneo-de-productos" in names
        assert "historial" in names
        assert "sincronizacion-en-segundo-plano" in names
        assert "funcion-premium" in names

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


# ---------------------------------------------------------------------------
# Outcomes & citations
# ---------------------------------------------------------------------------


class TestOutcomesAndCitations:
    def test_outcome_user_sees_present(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for o in f.get("outcomes", []):
                assert o.get("user_sees"), f"{f['id']}/{o['id']} missing user_sees"

    def test_each_outcome_has_reversible(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for o in f.get("outcomes", []):
                assert "reversible" in o, f"{f['id']}/{o['id']} missing reversible"

    def test_decision_points_have_branches(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for dp in f.get("decision_points", []):
                assert dp.get("branches"), f"{f['id']}/{dp['id']} missing branches"
                assert dp.get("file"), f"{f['id']}/{dp['id']} missing file"
                assert isinstance(dp.get("line"), int), f"{f['id']}/{dp['id']} line must be int"

    def test_dependencies_listed(self) -> None:
        gt = _load_gt()
        names = {d["name"] for d in gt.get("dependencies", [])}
        assert "kotlin" in names
        assert "hilt" in names
        assert "room" in names
        assert "compose-bom" in names
        assert "navigation-compose" in names
        assert "workmanager" in names
        assert "robolectric" in names

    def test_entry_points_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("entry_points", [])) >= 10

    def test_surfaces_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("surfaces", [])) >= 10


# ---------------------------------------------------------------------------
# Unique tokens
# ---------------------------------------------------------------------------


class TestUniqueTokensFile:
    def test_at_least_30_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 30, f"only {len(tokens)} tokens"

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXANDROID-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {
            "build", "vendor", "node_modules", ".git", ".bundle", "tmp",
            "log", "storage", ".gradle", ".gradle-cache", ".kotlin",
            ".idea", "build-cache", ".cxx"
        }
        skip_files = {"unique_tokens.txt", "build-history.sh"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(p in skip_dirs for p in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (
                ".kt", ".kts", ".xml", ".properties", ".yml", ".yaml",
                ".json", ".md", ".txt", ".toml", ".pro", ".sh"
            ):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            rel = path.relative_to(FIXTURE_ROOT).as_posix()
            for tok in tokens:
                assert tok not in text, f"token {tok} found in {rel}"


# ---------------------------------------------------------------------------
# Cites
# ---------------------------------------------------------------------------


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
                if "build/" in cite or ".build/" in cite or ".gradle/" in cite:
                    continue
                errs = check_cite(FIXTURE_ROOT, cite)
                for e in errs:
                    errors.append(f"{fid}/trace[{ti}]: {e}")
        if errors:
            pytest.fail("\n".join(errors[:20]))

    def test_all_traps_resolve(self) -> None:
        gt = _load_gt()
        errors = []
        for t in gt["traps"] + gt["package_traps"] + gt["superficial_traps"]:
            where = t.get("file", "")
            where_clean = re.split(r":[0-9]+$", where, maxsplit=1)[0]
            full = FIXTURE_ROOT / where_clean
            if not full.is_file():
                errors.append(f"trap {t['id']}: missing file {where_clean}")
        assert not errors, "trap locations with missing files:\n" + "\n".join(errors)

    def test_all_surfaces_have_handler_file(self) -> None:
        gt = _load_gt()
        for s in gt.get("surfaces", []):
            f = s.get("file", "")
            if not f or "/" not in f:
                continue
            f_clean = re.split(r":[0-9]+(?::[0-9]+)?$", f, maxsplit=1)[0]
            full = FIXTURE_ROOT / f_clean
            assert full.is_file(), f"surface {s.get('id')} missing file {f_clean}"


# ---------------------------------------------------------------------------
# Android structure
# ---------------------------------------------------------------------------


class TestAndroidStructure:
    def test_settings_gradle_exists(self) -> None:
        assert (FIXTURE_ROOT / "settings.gradle.kts").is_file()

    def test_app_build_gradle_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/build.gradle.kts").is_file()

    def test_app_build_gradle_declares_flavors(self) -> None:
        content = (FIXTURE_ROOT / "app/build.gradle.kts").read_text(encoding="utf-8")
        assert "free" in content
        assert "paid" in content
        assert "productFlavors" in content or "create(\"free\")" in content

    def test_app_build_gradle_declares_hilt(self) -> None:
        content = (FIXTURE_ROOT / "app/build.gradle.kts").read_text(encoding="utf-8")
        assert "hilt" in content.lower()

    def test_app_build_gradle_declares_room(self) -> None:
        content = (FIXTURE_ROOT / "app/build.gradle.kts").read_text(encoding="utf-8")
        assert "room" in content.lower()

    def test_app_build_gradle_declares_compose(self) -> None:
        content = (FIXTURE_ROOT / "app/build.gradle.kts").read_text(encoding="utf-8")
        assert "compose" in content.lower()

    def test_version_catalog_exists(self) -> None:
        assert (FIXTURE_ROOT / "gradle/libs.versions.toml").is_file()

    def test_gradle_properties_exists(self) -> None:
        assert (FIXTURE_ROOT / "gradle.properties").is_file()

    def test_android_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/src/main/AndroidManifest.xml").is_file()

    def test_main_java_di_exists(self) -> None:
        d = FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/di"
        assert d.is_dir()
        assert (d / "AppModule.kt").is_file()
        assert (d / "DatabaseModule.kt").is_file()

    def test_main_java_data_local_exists(self) -> None:
        d = FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/data/local"
        assert d.is_dir()
        assert (d / "FxDatabase.kt").is_file()
        assert (d / "dao/ProductDao.kt").is_file()
        assert (d / "dao/HistoryDao.kt").is_file()
        assert (d / "dao/ScanDao.kt").is_file()
        assert (d / "entity/ProductEntity.kt").is_file()
        assert (d / "entity/HistoryEntity.kt").is_file()

    def test_main_java_data_repository_exists(self) -> None:
        d = FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/data/repository"
        assert d.is_dir()
        assert (d / "ProductRepository.kt").is_file()
        assert (d / "HistoryRepository.kt").is_file()

    def test_main_java_ui_scan_exists(self) -> None:
        d = FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/ui/scan"
        assert d.is_dir()
        assert (d / "ScanScreen.kt").is_file()
        assert (d / "ScanViewModel.kt").is_file()

    def test_main_java_ui_history_exists(self) -> None:
        d = FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/ui/history"
        assert d.is_dir()
        assert (d / "HistoryScreen.kt").is_file()
        assert (d / "HistoryViewModel.kt").is_file()

    def test_main_java_ui_legacy_exists(self) -> None:
        d = FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/ui/legacy"
        assert d.is_dir()
        assert (d / "LegacyProductActivity.kt").is_file()
        assert (d / "LegacyProductFragment.kt").is_file()

    def test_main_java_work_exists(self) -> None:
        d = FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/work"
        assert d.is_dir()
        assert (d / "SyncWorker.kt").is_file()
        assert (d / "SyncScheduler.kt").is_file()

    def test_main_java_receiver_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/receiver/SyncTriggerReceiver.kt").is_file()

    def test_main_java_navigation_exists(self) -> None:
        d = FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/navigation"
        assert d.is_dir()
        assert (d / "FxNavGraph.kt").is_file()
        assert (d / "Routes.kt").is_file()


# ---------------------------------------------------------------------------
# Flavor source sets (E4)
# ---------------------------------------------------------------------------


class TestFlavors:
    def test_free_flavor_has_premium_disabled(self) -> None:
        f = FIXTURE_ROOT / "app/src/free/java/com/example/fxandroid/featurepremium/PremiumDisabled.kt"
        assert f.is_file()

    def test_paid_flavor_has_premium_enabled(self) -> None:
        f = FIXTURE_ROOT / "app/src/paid/java/com/example/fxandroid/featurepremium/PremiumEnabled.kt"
        assert f.is_file()


# ---------------------------------------------------------------------------
# Manifest entries (E1, E6)
# ---------------------------------------------------------------------------


class TestManifestEntries:
    def test_manifest_declares_activity(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/AndroidManifest.xml").read_text(encoding="utf-8")
        assert "<activity" in content
        assert "LegacyProductActivity" in content

    def test_manifest_declares_receiver(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/AndroidManifest.xml").read_text(encoding="utf-8")
        assert "<receiver" in content
        assert "SyncTriggerReceiver" in content

    def test_manifest_has_intent_filter(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/AndroidManifest.xml").read_text(encoding="utf-8")
        assert "<intent-filter>" in content

    def test_manifest_has_deep_link_scheme(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/AndroidManifest.xml").read_text(encoding="utf-8")
        assert "fxandroid" in content


# ---------------------------------------------------------------------------
# Build config
# ---------------------------------------------------------------------------


class TestBuildConfig:
    def test_build_gradle_uses_compose_plugin(self) -> None:
        content = (FIXTURE_ROOT / "app/build.gradle.kts").read_text(encoding="utf-8")
        assert "buildFeatures" in content
        assert "compose = true" in content

    def test_build_gradle_uses_view_binding(self) -> None:
        content = (FIXTURE_ROOT / "app/build.gradle.kts").read_text(encoding="utf-8")
        assert "viewBinding = true" in content


# ---------------------------------------------------------------------------
# Tests source set
# ---------------------------------------------------------------------------


class TestTestSourceSet:
    def test_test_java_scan_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "app/src/test/java/com/example/fxandroid/ui/scan"
        assert d.is_dir()

    def test_test_uses_junit5(self) -> None:
        # Robolectric + JUnit5 (no @RunWith RobolectricTestRunner for pure VM tests)
        any_junit = False
        for path in FIXTURE_ROOT.rglob("app/src/test/**/*.kt"):
            try:
                content = path.read_text(encoding="utf-8")
            except Exception:
                continue
            if "org.junit.jupiter" in content:
                any_junit = True
                break
        assert any_junit, "no JUnit5 imports found in test sources"

    def test_test_android_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/src/test/AndroidManifest.xml").is_file()


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_manifest_components(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/AndroidManifest.xml").read_text(encoding="utf-8")
        assert "<activity" in content
        assert "<receiver" in content

    def test_e2_hilt_generated(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/FxAndroidApp.kt").read_text(encoding="utf-8")
        assert "@HiltAndroidApp" in content

    def test_e3_room_dao_query(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/data/local/dao/HistoryDao.kt").read_text(encoding="utf-8")
        assert "@Query" in content

    def test_e4_flavors(self) -> None:
        content = (FIXTURE_ROOT / "app/build.gradle.kts").read_text(encoding="utf-8")
        assert "free" in content
        assert "paid" in content
        assert "featurepremium" in (FIXTURE_ROOT / "app/src/free/java/com/example/fxandroid/featurepremium/PremiumDisabled.kt").read_text(encoding="utf-8")
        assert "PremiumEnabled" in (FIXTURE_ROOT / "app/src/paid/java/com/example/fxandroid/featurepremium/PremiumEnabled.kt").read_text(encoding="utf-8")

    def test_e5_onclick_resource(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/res/layout/activity_legacy_product.xml").read_text(encoding="utf-8")
        assert "android:onClick" in content

    def test_e6_deeplinks_in_nav_graph(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/res/navigation/nav_graph.xml").read_text(encoding="utf-8")
        assert "deepLink" in content
        assert "fxandroid://" in content


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_dao_query_pattern(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/data/local/dao/HistoryDao.kt").read_text(encoding="utf-8")
        assert "@Query" in content

    def test_p2_repo_not_singleton(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/di/AppModule.kt").read_text(encoding="utf-8")
        assert "ProductRepositoryImpl" in content

    def test_p3_sync_expedited_silent(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/work/SyncScheduler.kt").read_text(encoding="utf-8")
        assert "setExpedited" in content

    def test_p4_room_no_migrations(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/di/DatabaseModule.kt").read_text(encoding="utf-8")
        assert "Room.databaseBuilder" in content
        assert "addMigrations" not in content

    def test_p5_legacy_activity_execSQL(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/ui/legacy/LegacyProductActivity.kt").read_text(encoding="utf-8")
        assert "execSQL" in content

    def test_p6_scan_viewmodel_silent_catch(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/ui/scan/ScanViewModel.kt").read_text(encoding="utf-8")
        assert "catch (e: Exception)" in content


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_legacy_date_formatter_unused(self) -> None:
        helper = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/util/LegacyDateFormatter.kt").read_text(encoding="utf-8")
        assert "LegacyDateFormatter" in helper
        # Check it is not referenced from runtime code
        runtime = [
            "ui/scan/ScanViewModel.kt",
            "ui/scan/ScanScreen.kt",
            "ui/history/HistoryViewModel.kt",
            "ui/history/HistoryScreen.kt",
            "ui/legacy/LegacyProductActivity.kt",
            "ui/premium/PremiumGateScreen.kt",
            "work/SyncWorker.kt",
            "work/SyncScheduler.kt",
            "receiver/SyncTriggerReceiver.kt",
            "navigation/FxNavGraph.kt"
        ]
        for path in runtime:
            src = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid" / path).read_text(encoding="utf-8")
            assert "LegacyDateFormatter" not in src, f"LegacyDateFormatter referenced in {path}"

    def test_s2_env_config_debug_unused(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/util/EnvConfig.kt").read_text(encoding="utf-8")
        assert "BuildConfig.DEBUG" in content

    def test_s3_legacy_fragment_returns_null(self) -> None:
        content = (FIXTURE_ROOT / "app/src/main/java/com/example/fxandroid/ui/legacy/LegacyProductFragment.kt").read_text(encoding="utf-8")
        assert "return null" in content


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-kotlin-android" in content

    def test_manifest_requires(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "linux" in content

    def test_dockerfile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_makefile_has_test_target(self) -> None:
        content = (FIXTURE_ROOT / "Makefile").read_text(encoding="utf-8")
        assert "test:" in content

    def test_build_history_exists(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()