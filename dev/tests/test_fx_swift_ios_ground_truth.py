"""Tests del ground truth de fx-swift-ios (F06aa)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-swift-ios"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-swift-ios"


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
        assert "onboarding" in names
        assert "lista-de-gastos" in names
        assert "sincronizacion-icloud" in names
        assert "widget-de-resumen" in names

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
        assert "swift" in names
        assert "swiftui" in names
        assert "uikit" in names
        assert "widgetkit" in names
        assert "xcodebuild" in names

    def test_entry_points_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("entry_points", [])) >= 10

    def test_surfaces_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("surfaces", [])) >= 10

    def test_modules_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("modules", [])) >= 12


class TestUniqueTokensFile:
    def test_at_least_25_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 25, f"only {len(tokens)} tokens"

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXSWIFT-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {
            "build", "vendor", "node_modules", ".git", ".bundle", "tmp",
            "log", "storage", ".build", ".swiftpm", "DerivedData"
        }
        skip_files = {"unique_tokens.txt", "build-history.sh", "project.pbxproj"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(part in skip_dirs for part in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (
                ".swift", ".h", ".m", ".plist", ".entitlements", ".xcconfig",
                ".py", ".sh", ".yml", ".yaml", ".json", ".md", ".txt"
            ):
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
                if "build/" in cite or ".build/" in cite or ".swiftpm/" in cite:
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
            where = t.get("where", "")
            candidates = re.findall(r"[\w/.\-]+\.(?:swift|h|m|plist|entitlements|xcconfig)", where)
            for file_part in candidates:
                if file_part and "/" in file_part and not file_part.startswith("."):
                    full = FIXTURE_ROOT / file_part
                    if not full.is_file():
                        errors.append(f"trap {t['id']}: missing file {file_part}")
        assert not errors, "trap locations with missing files:\n" + "\n".join(errors)

    def test_all_surfaces_have_handler_file(self) -> None:
        gt = _load_gt()
        for s in gt.get("surfaces", []):
            f = s.get("file", "")
            if not f or "/" not in f:
                continue
            # Strip optional :line or :line:col suffix.
            f_clean = re.split(r":[0-9]+(?::[0-9]+)?$", f, maxsplit=1)[0]
            full = FIXTURE_ROOT / f_clean
            assert full.is_file(), f"surface {s.get('id')} missing file {f_clean}"


class TestSwiftStructure:
    def test_package_swift_exists(self) -> None:
        assert (FIXTURE_ROOT / "Package.swift").is_file()

    def test_models_dir(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftCore/Models"
        assert d.is_dir()
        for f in ("Expense.swift", "ExpenseCategory.swift", "OnboardingState.swift", "SyncStatus.swift"):
            assert (d / f).is_file(), f"missing {f}"

    def test_property_wrappers_dir(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftCore/PropertyWrappers"
        assert d.is_dir()
        assert (d / "Debounced.swift").is_file()
        assert (d / "UserDefaultsBacked.swift").is_file()

    def test_protocols_dir(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftCore/Protocols"
        assert d.is_dir()
        assert (d / "Describable.swift").is_file()
        assert (d / "Describable+Category.swift").is_file()
        assert (d / "Syncable.swift").is_file()

    def test_appgroup_dir(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftCore/AppGroup"
        assert d.is_dir()
        assert (d / "AppGroupPaths.swift").is_file()
        assert (d / "AppGroupStore.swift").is_file()

    def test_persistence_dir(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftCore/Persistence"
        assert d.is_dir()
        assert (d / "ExpensesRepository.swift").is_file()
        assert (d / "ExpensesStore.swift").is_file()

    def test_sync_dir(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftCore/Sync"
        assert d.is_dir()
        assert (d / "CloudKitSyncEngine.swift").is_file()
        assert (d / "SyncCoordinator.swift").is_file()

    def test_widget_dir(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftCore/Widget"
        assert d.is_dir()
        for f in ("WidgetSummary.swift", "WidgetSummaryProvider.swift", "AppGroupReader.swift"):
            assert (d / f).is_file(), f"missing {f}"

    def test_objc_bridge_files(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftCore/ObjCBridge"
        assert (d / "LegacyLogger.h").is_file()
        assert (d / "LegacyLogger.m").is_file()
        assert (d / "FxSwift-Bridging-Header.h").is_file()

    def test_build_flags_file(self) -> None:
        assert (FIXTURE_ROOT / "Sources/FxSwiftCore/BuildFlags/BuildFlags.swift").is_file()

    def test_ui_files(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftCore/UI"
        for f in ("OnboardingView.swift", "ExpenseListView.swift", "ExpenseRow.swift",
                  "DeepLinkRouter.swift", "LegacySettingsView.swift"):
            assert (d / f).is_file(), f"missing {f}"

    def test_umbrella_file(self) -> None:
        assert (FIXTURE_ROOT / "Sources/FxSwiftCore/FxSwiftCore.swift").is_file()

    def test_xcode_project(self) -> None:
        assert (FIXTURE_ROOT / "Examples/FxSwift.xcodeproj/project.pbxproj").is_file()

    def test_xcode_app_files(self) -> None:
        d = FIXTURE_ROOT / "Examples/FxSwiftApp"
        for f in ("AppMain.swift", "Info.plist", "FxSwiftApp.entitlements",
                  "FxSwift-Bridging-Header.h", "LegacyLogger.h", "LegacyLogger.m",
                  "SettingsHostController.swift", "Configs/Common.xcconfig",
                  "Configs/Debug.xcconfig", "Configs/Release.xcconfig"):
            assert (d / f).is_file(), f"missing {f}"

    def test_xcode_widget_files(self) -> None:
        d = FIXTURE_ROOT / "Examples/FxSwiftWidget"
        for f in ("WidgetMain.swift", "Info.plist", "FxSwiftWidget.entitlements"):
            assert (d / f).is_file(), f"missing {f}"

    def test_dockerfile_test(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_readme(self) -> None:
        assert (FIXTURE_ROOT / "README.md").is_file()

    def test_manifest(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()


class TestObjCBridge:
    def test_header_declares_interface(self) -> None:
        h = (FIXTURE_ROOT / "Sources/FxSwiftCore/ObjCBridge/LegacyLogger.h").read_text()
        assert "@interface LegacyLogger" in h
        assert "@property" in h
        assert "+ (instancetype)sharedLogger" in h

    def test_header_exposes_log(self) -> None:
        h = (FIXTURE_ROOT / "Sources/FxSwiftCore/ObjCBridge/LegacyLogger.h").read_text()
        assert "- (void)log:" in h
        assert "- (void)clear" in h

    def test_implementation_uses_dynamic(self) -> None:
        m = (FIXTURE_ROOT / "Sources/FxSwiftCore/ObjCBridge/LegacyLogger.m").read_text()
        assert "@implementation LegacyLogger" in m
        assert "@dynamic lastMessage" in m

    def test_implementation_uses_nsobjclass(self) -> None:
        m = (FIXTURE_ROOT / "Sources/FxSwiftCore/ObjCBridge/LegacyLogger.m").read_text()
        assert "NSNotificationCenter" in m
        assert "postNotificationName" in m

    def test_bridging_header_imports(self) -> None:
        b = (FIXTURE_ROOT / "Sources/FxSwiftCore/ObjCBridge/FxSwift-Bridging-Header.h").read_text()
        assert '#import "LegacyLogger.h"' in b

    def test_legacy_logger_posted_in_copied(self) -> None:
        copied = FIXTURE_ROOT / "Examples/FxSwiftApp/LegacyLogger.m"
        assert copied.is_file()
        m = copied.read_text()
        assert "@implementation LegacyLogger" in m


class TestAppGroup:
    def test_group_identifier(self) -> None:
        paths = (FIXTURE_ROOT / "Sources/FxSwiftCore/AppGroup/AppGroupPaths.swift").read_text()
        assert "group.com.example.fxswift" in paths

    def test_resolver_function(self) -> None:
        paths = (FIXTURE_ROOT / "Sources/FxSwiftCore/AppGroup/AppGroupPaths.swift").read_text()
        assert "containerURL(forSecurityApplicationGroupIdentifier:" in paths

    def test_app_entitlements_declares_group(self) -> None:
        ent = (FIXTURE_ROOT / "Examples/FxSwiftApp/FxSwiftApp.entitlements").read_text()
        assert "application-groups" in ent
        assert "group.com.example.fxswift" in ent

    def test_widget_entitlements_declares_group(self) -> None:
        ent = (FIXTURE_ROOT / "Examples/FxSwiftWidget/FxSwiftWidget.entitlements").read_text()
        assert "application-groups" in ent
        assert "group.com.example.fxswift" in ent


class TestWidgetExtension:
    def test_widget_info_plist_has_widgetkit_identifier(self) -> None:
        plist = (FIXTURE_ROOT / "Examples/FxSwiftWidget/Info.plist").read_text()
        assert "com.apple.widgetkit-extension" in plist

    def test_widget_main_has_main_and_widget(self) -> None:
        main = (FIXTURE_ROOT / "Examples/FxSwiftWidget/WidgetMain.swift").read_text()
        assert "@main" in main
        assert "Widget" in main

    def test_widget_imports_widgetkit(self) -> None:
        main = (FIXTURE_ROOT / "Examples/FxSwiftWidget/WidgetMain.swift").read_text()
        assert "import WidgetKit" in main

    def test_widget_imports_fxswiftcore(self) -> None:
        main = (FIXTURE_ROOT / "Examples/FxSwiftWidget/WidgetMain.swift").read_text()
        assert "import FxSwiftCore" in main


class TestTrapsEcosystem:
    def test_e01_property_wrappers(self) -> None:
        d = (FIXTURE_ROOT / "Sources/FxSwiftCore/PropertyWrappers/Debounced.swift").read_text()
        assert "@propertyWrapper" in d
        assert "public final class Debounced" in d

    def test_e02_navigation_destination(self) -> None:
        v = (FIXTURE_ROOT / "Sources/FxSwiftCore/UI/OnboardingView.swift").read_text()
        assert "NavigationStack" in v
        assert "navigationDestination(for: OnboardingState.self)" in v

    def test_e03_protocol_default_split(self) -> None:
        p = (FIXTURE_ROOT / "Sources/FxSwiftCore/Protocols/Describable.swift").read_text()
        c = (FIXTURE_ROOT / "Sources/FxSwiftCore/Protocols/Describable+Category.swift").read_text()
        assert "extension Describable" in p
        assert "extension ExpenseCategory: Describable" in c

    def test_e04_objc_dynamic(self) -> None:
        h = (FIXTURE_ROOT / "Sources/FxSwiftCore/ObjCBridge/LegacyLogger.h").read_text()
        m = (FIXTURE_ROOT / "Sources/FxSwiftCore/ObjCBridge/LegacyLogger.m").read_text()
        assert "@interface LegacyLogger" in h
        assert "@dynamic lastMessage" in m

    def test_e05_build_flags(self) -> None:
        b = (FIXTURE_ROOT / "Sources/FxSwiftCore/BuildFlags/BuildFlags.swift").read_text()
        assert "#if os(iOS)" in b
        assert "#if DEBUG" in b
        assert "targetEnvironment(simulator)" in b

    def test_e06_app_group(self) -> None:
        p = (FIXTURE_ROOT / "Sources/FxSwiftCore/AppGroup/AppGroupPaths.swift").read_text()
        plist = (FIXTURE_ROOT / "Examples/FxSwiftApp/Info.plist").read_text()
        assert "group.com.example.fxswift" in p
        assert "fxswift" in plist


class TestTrapsPackage:
    def test_p01_sync_swallows_errors(self) -> None:
        s = (FIXTURE_ROOT / "Sources/FxSwiftCore/Sync/CloudKitSyncEngine.swift").read_text()
        assert "invalid amount" in s
        assert "skipped" in s

    def test_p02_widget_timeline_exists(self) -> None:
        w = (FIXTURE_ROOT / "Sources/FxSwiftCore/Widget/WidgetSummaryProvider.swift").read_text()
        assert "timeline" in w

    def test_p03_sink_sin_store_in(self) -> None:
        s = (FIXTURE_ROOT / "Sources/FxSwiftCore/Persistence/ExpensesStore.swift").read_text()
        assert ".sink" in s
        assert "cancellables" in s
        assert "Trampa P3" in s

    def test_p04_appgroup_save_swallows_errors(self) -> None:
        s = (FIXTURE_ROOT / "Sources/FxSwiftCore/AppGroup/AppGroupStore.swift").read_text()
        assert "try? data.write" in s
        assert "Trampa P4" in s

    def test_p05_deeplink_swallows_uuid(self) -> None:
        r = (FIXTURE_ROOT / "Sources/FxSwiftCore/UI/DeepLinkRouter.swift").read_text()
        assert "try? UUID(uuidString:" in r
        assert "Trampa P5" in r

    def test_p6_objc_register_not_called(self) -> None:
        c = (FIXTURE_ROOT / "Examples/FxSwiftApp/SettingsHostController.swift").read_text()
        assert "registerForNotifications" in c
        assert "// logger.registerForNotifications()" in c


class TestTrapsSuperficial:
    def test_s01_setter_ignores_value(self) -> None:
        s = (FIXTURE_ROOT / "Sources/FxSwiftCore/Protocols/Syncable.swift").read_text()
        assert "set { _ = newValue }" in s

    def test_s02_override_env_var(self) -> None:
        p = (FIXTURE_ROOT / "Sources/FxSwiftCore/AppGroup/AppGroupPaths.swift").read_text()
        assert "overrideEnvVar" in p

    def test_s03_unused_init(self) -> None:
        s = (FIXTURE_ROOT / "Sources/FxSwiftCore/Sync/CloudKitSyncEngine.swift").read_text()
        assert "public init() {}" in s


class TestManifest:
    def test_manifest_file_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name_is_fx_swift_ios(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text()
        assert "name: fx-swift-ios" in text

    def test_manifest_requires_macos(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text()
        assert "- macos" in text

    def test_manifest_test_cmd_starts_with_make(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text()
        assert "test_cmd: make test" in text

    def test_manifest_container_disabled(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text()
        assert "enabled: false" in text

    def test_manifest_image_tag_starts_with_npr(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text()
        assert "image_tag: npr-fx-swift-ios" in text


class TestCC11InFixture:
    """CC-11: el codigo del fixture no menciona el ground truth ni rutas
    de dev/ que rompan el aislamiento. La version estricta de CC-11
    (`_check_cc11`) sobre nombres de features se omite a proposito:
    la palabra 'onboarding' aparece de forma legitima en identificadores
    de Swift (OnboardingView, OnboardingState) y renombrarla para
    evitar el linter haria el fixture menos realista."""

    def test_no_ground_truth_or_dev_paths_in_code(self) -> None:
        """Verifica que los archivos .swift/.h/.m/.plist no mencionan el
        ground truth ni rutas de dev/."""
        skip_dirs = {
            "build", "vendor", "node_modules", ".git", ".bundle", "tmp",
            "log", "storage", ".build", ".swiftpm", "DerivedData"
        }
        skip_files = {"unique_tokens.txt", "build-history.sh", "project.pbxproj"}
        forbidden_substrings = [
            "ground_truth", "ground-truth",
            "dev/fixtures", "dev/ground-truth", "NPRGT-FXSWIFT-",
        ]
        checked_exts = (".swift", ".h", ".m", ".plist", ".entitlements", ".xcconfig")
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(part in skip_dirs for part in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in checked_exts:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            rel = path.relative_to(FIXTURE_ROOT).as_posix()
            lower_text = text.lower()
            for sub in forbidden_substrings:
                if sub.lower() in lower_text:
                    pytest.fail(f"{rel} contiene la cadena prohibida '{sub}'")
