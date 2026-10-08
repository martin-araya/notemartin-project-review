"""Tests del ground truth de fx-react-native (F06ae)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-react-native"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-react-native"


def _load_gt() -> dict:
    return json.loads((GT_DIR / "ground_truth.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Shape
# ---------------------------------------------------------------------------


class TestGroundTruthShape:
    def test_file_exists(self) -> None:
        assert (GT_DIR / "ground_truth.json").is_file()

    def test_has_3_features(self) -> None:
        gt = _load_gt()
        assert len(gt["features"]) == 3

    def test_features_match_spec(self) -> None:
        gt = _load_gt()
        names = {f["name"] for f in gt["features"]}
        assert "pagos-con-nfc" in names
        assert "historial" in names
        assert "notificaciones-push" in names

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

    def test_has_2_superficial_traps(self) -> None:
        gt = _load_gt()
        assert len(gt.get("superficial_traps", [])) == 2

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
        assert "react-native" in names
        assert "expo" in names
        assert "@reduxjs/toolkit" in names
        assert "@react-navigation/native" in names
        assert "metro" in names

    def test_entry_points_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("entry_points", [])) >= 12

    def test_surfaces_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("surfaces", [])) >= 8


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
            assert tok.startswith("NPRGT-FXRN-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {
            "node_modules", "vendor", ".git", ".bundle", "tmp",
            "log", "storage", ".expo", "dist", "web-build",
            ".yarn-cache", "ios", "android", "coverage", "Generated"
        }
        skip_files = {
            "unique_tokens.txt", "build-history.sh", "package-lock.json",
            "yarn.lock", ".metadata",
        }
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(p in skip_dirs for p in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (
                ".ts", ".tsx", ".js", ".jsx", ".kt", ".swift", ".m", ".mm",
                ".json", ".md", ".txt", ".sh", ".yml", ".yaml", ".xml",
                ".plist",
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

    def test_entry_point_cites_exist(self) -> None:
        gt = _load_gt()
        errors = []
        for ep in gt.get("entry_points", []):
            f = ep["file"]
            cite = f if ":" in f else f"{f}:1"
            errs = check_cite(FIXTURE_ROOT, cite)
            if errs:
                errors.append(f"entry_point {ep['id']}: {errs}")
        if errors:
            pytest.fail("\n".join(errors[:10]))


# ---------------------------------------------------------------------------
# React Native structure
# ---------------------------------------------------------------------------


class TestRNStructure:
    def test_package_json_exists(self) -> None:
        assert (FIXTURE_ROOT / "package.json").is_file()

    def test_app_json_exists(self) -> None:
        assert (FIXTURE_ROOT / "app.json").is_file()

    def test_app_tsx_exists(self) -> None:
        assert (FIXTURE_ROOT / "App.tsx").is_file()

    def test_index_js_exists(self) -> None:
        assert (FIXTURE_ROOT / "index.js").is_file()

    def test_babel_config_exists(self) -> None:
        assert (FIXTURE_ROOT / "babel.config.js").is_file()

    def test_metro_config_exists(self) -> None:
        assert (FIXTURE_ROOT / "metro.config.js").is_file()

    def test_jest_config_exists(self) -> None:
        assert (FIXTURE_ROOT / "jest.config.js").is_file()

    def test_tsconfig_exists(self) -> None:
        assert (FIXTURE_ROOT / "tsconfig.json").is_file()

    def test_jest_setup_exists(self) -> None:
        assert (FIXTURE_ROOT / "jest.setup.js").is_file()

    def test_navigation_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/navigation"
        assert d.is_dir()
        assert (d / "RootNavigator.tsx").is_file()
        assert (d / "linkingConfig.ts").is_file()
        assert (d / "routes.ts").is_file()

    def test_store_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/store"
        assert d.is_dir()
        assert (d / "index.ts").is_file()
        assert (d / "hooks.ts").is_file()
        assert (d / "slices/paymentsSlice.ts").is_file()
        assert (d / "slices/historySlice.ts").is_file()
        assert (d / "slices/notificationsSlice.ts").is_file()

    def test_payments_feature_exists(self) -> None:
        d = FIXTURE_ROOT / "src/features/payments"
        assert d.is_dir()
        assert (d / "domain/NfcPayment.ts").is_file()
        assert (d / "data/NfcManager.ts").is_file()
        assert (d / "application/PaymentsController.ts").is_file()
        assert (d / "presentation/PaymentsScreen.tsx").is_file()
        assert (d / "presentation/PaymentsScreen.ios.tsx").is_file()
        assert (d / "presentation/PaymentsScreen.android.tsx").is_file()

    def test_history_feature_exists(self) -> None:
        d = FIXTURE_ROOT / "src/features/history"
        assert d.is_dir()
        assert (d / "presentation/HistoryScreen.tsx").is_file()

    def test_notifications_feature_exists(self) -> None:
        d = FIXTURE_ROOT / "src/features/notifications"
        assert d.is_dir()
        assert (d / "application/NotificationHandler.ts").is_file()
        assert (d / "presentation/NotificationsScreen.tsx").is_file()

    def test_plugins_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/plugins"
        assert d.is_dir()
        assert (d / "withNfc.ts").is_file()
        assert (d / "withDeepLinking.ts").is_file()

    def test_android_stub_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "android_stub"
        assert d.is_dir()
        assert (d / "NfcManagerModule.kt").is_file()
        assert (d / "NfcManagerPackage.kt").is_file()
        assert (d / "AndroidManifest.xml").is_file()

    def test_ios_stub_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "ios_stub"
        assert d.is_dir()
        assert (d / "NfcManagerModule.swift").is_file()
        assert (d / "NfcManagerModule.mm").is_file()
        assert (d / "Info.plist").is_file()


# ---------------------------------------------------------------------------
# Package config
# ---------------------------------------------------------------------------


class TestPackageConfig:
    def test_package_has_react_nave(self) -> None:
        content = (FIXTURE_ROOT / "package.json").read_text(encoding="utf-8")
        assert "react-native" in content
        assert "0.74" in content

    def test_package_has_expo(self) -> None:
        content = (FIXTURE_ROOT / "package.json").read_text(encoding="utf-8")
        assert "expo" in content

    def test_package_has_redux(self) -> None:
        content = (FIXTURE_ROOT / "package.json").read_text(encoding="utf-8")
        assert "@reduxjs/toolkit" in content
        assert "react-redux" in content

    def test_package_has_react_navigation(self) -> None:
        content = (FIXTURE_ROOT / "package.json").read_text(encoding="utf-8")
        assert "@react-navigation/native" in content
        assert "@react-navigation/native-stack" in content


# ---------------------------------------------------------------------------
# App.json plugins
# ---------------------------------------------------------------------------


class TestAppJsonPlugins:
    def test_app_json_declares_with_nfc(self) -> None:
        content = (FIXTURE_ROOT / "app.json").read_text(encoding="utf-8")
        assert "./plugins/withNfc" in content

    def test_app_json_declares_expo_plugins(self) -> None:
        content = (FIXTURE_ROOT / "app.json").read_text(encoding="utf-8")
        assert "expo-build-properties" in content
        assert "expo-notifications" in content
        assert "expo-linking" in content


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_bridge_native_module(self) -> None:
        dart = (FIXTURE_ROOT / "src/features/payments/data/NfcManager.ts").read_text(encoding="utf-8")
        kotlin = (FIXTURE_ROOT / "android_stub/NfcManagerModule.kt").read_text(encoding="utf-8")
        swift = (FIXTURE_ROOT / "ios_stub/NfcManagerModule.swift").read_text(encoding="utf-8")
        assert "NativeModules.RtcNfcManager" in dart
        assert "@ReactModule(name = \"RtcNfcManager\")" in kotlin
        assert "RtcNfcManager" in swift

    def test_e2_platform_files(self) -> None:
        ios = (FIXTURE_ROOT / "src/features/payments/presentation/PaymentsScreen.ios.tsx").read_text(encoding="utf-8")
        android = (FIXTURE_ROOT / "src/features/payments/presentation/PaymentsScreen.android.tsx").read_text(encoding="utf-8")
        assert "iOS" in ios
        assert "Android" in android

    def test_e3_expo_config_plugins(self) -> None:
        app_json = (FIXTURE_ROOT / "app.json").read_text(encoding="utf-8")
        assert "./plugins/withNfc" in app_json
        assert "./plugins/withDeepLinking" in app_json
        assert "expo-build-properties" in app_json
        assert "expo-notifications" in app_json

    def test_e4_deep_linking(self) -> None:
        linking = (FIXTURE_ROOT / "src/navigation/linkingConfig.ts").read_text(encoding="utf-8")
        assert "fxrn://" in linking
        assert "Linking.createURL" in linking
        assert "screens" in linking

    def test_e5_metro_aliases(self) -> None:
        metro = (FIXTURE_ROOT / "metro.config.js").read_text(encoding="utf-8")
        babel = (FIXTURE_ROOT / "babel.config.js").read_text(encoding="utf-8")
        assert "'@app'" in metro
        assert "'@features'" in metro
        assert "extraNodeModules" in metro
        assert "module-resolver" in babel

    def test_e6_notification_handler(self) -> None:
        handler = (FIXTURE_ROOT / "src/features/notifications/application/NotificationHandler.ts").read_text(encoding="utf-8")
        assert "setNotificationHandler" in handler
        assert "handleNotification" in handler
        assert "getExpoPushTokenAsync" in handler


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_nfc_no_try_catch(self) -> None:
        nfc = (FIXTURE_ROOT / "src/features/payments/data/NfcManager.ts").read_text(encoding="utf-8")
        # The readTag method should NOT be wrapped in try/catch
        assert "readTag" in nfc
        # Find the readTag method body
        read_tag_idx = nfc.index("static async readTag")
        next_method_idx = nfc.index("static", read_tag_idx + 1)
        body = nfc[read_tag_idx:next_method_idx]
        assert "try {" not in body

    def test_p2_redux_slice_direct_mutation(self) -> None:
        slice = (FIXTURE_ROOT / "src/store/slices/paymentsSlice.ts").read_text(encoding="utf-8")
        assert "state.items.push" in slice

    def test_p3_notification_silent_catch(self) -> None:
        handler = (FIXTURE_ROOT / "src/features/notifications/application/NotificationHandler.ts").read_text(encoding="utf-8")
        assert "catch (_)" in handler

    def test_p4_linking_config_no_android_disable(self) -> None:
        linking = (FIXTURE_ROOT / "src/navigation/linkingConfig.ts").read_text(encoding="utf-8")
        assert "fxrn://" in linking

    def test_p5_nfc_start_no_permissions(self) -> None:
        nfc = (FIXTURE_ROOT / "src/features/payments/data/NfcManager.ts").read_text(encoding="utf-8")
        # NfcManager.start() should NOT call PermissionsAndroid
        assert "PermissionsAndroid" not in nfc

    def test_p6_metro_alias(self) -> None:
        metro = (FIXTURE_ROOT / "metro.config.js").read_text(encoding="utf-8")
        assert "'@features'" in metro
        assert "path.resolve(__dirname, 'src/features')" in metro


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_logger_unused(self) -> None:
        logger_src = (FIXTURE_ROOT / "src/util/logger.ts").read_text(encoding="utf-8")
        assert "Logger" in logger_src
        # Check Logger.log is not used in runtime code
        for entity in (FIXTURE_ROOT / "src").rglob("*.ts*"):
            if entity.name == "logger.ts":
                continue
            content = entity.read_text(encoding="utf-8")
            assert "Logger.log" not in content
            assert "Logger.warn" not in content

    def test_s2_date_format_unused(self) -> None:
        date_src = (FIXTURE_ROOT / "src/util/dateFormat.ts").read_text(encoding="utf-8")
        assert "formatDate" in date_src
        for entity in (FIXTURE_ROOT / "src/features").rglob("*.tsx"):
            content = entity.read_text(encoding="utf-8")
            assert "formatDate" not in content


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-react-native" in content

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