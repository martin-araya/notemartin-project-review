"""Tests del ground truth de fx-flutter-dart (F06ad)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-flutter-dart"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-flutter-dart"


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
        assert "lector-de-documentos" in names
        assert "favoritos" in names
        assert "ajustes" in names

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
        assert "flutter" in names
        assert "flutter_riverpod" in names
        assert "go_router" in names
        assert "freezed_annotation" in names
        assert "build_runner" in names

    def test_entry_points_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("entry_points", [])) >= 10

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
            assert tok.startswith("NPRGT-FXFLUTTER-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {
            "build", "vendor", "node_modules", ".git", ".bundle", "tmp",
            "log", "storage", ".dart_tool", ".pub-cache", ".flutter-plugins",
            ".flutter-plugins-dependencies", ".dart_tool-cache"
        }
        skip_files = {
            "unique_tokens.txt", "build-history.sh", "pubspec.lock",
            ".metadata", ".packages"
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
                ".dart", ".kt", ".swift", ".yaml", ".yml",
                ".json", ".md", ".txt", ".sh"
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
                if "build/" in cite or ".build/" in cite or ".dart_tool/" in cite:
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
# Flutter structure
# ---------------------------------------------------------------------------


class TestFlutterStructure:
    def test_pubspec_exists(self) -> None:
        assert (FIXTURE_ROOT / "pubspec.yaml").is_file()

    def test_pubspec_declares_flutter_riverpod(self) -> None:
        content = (FIXTURE_ROOT / "pubspec.yaml").read_text(encoding="utf-8")
        assert "flutter_riverpod" in content

    def test_pubspec_declares_go_router(self) -> None:
        content = (FIXTURE_ROOT / "pubspec.yaml").read_text(encoding="utf-8")
        assert "go_router" in content

    def test_pubspec_declares_freezed_annotation(self) -> None:
        content = (FIXTURE_ROOT / "pubspec.yaml").read_text(encoding="utf-8")
        assert "freezed_annotation" in content

    def test_pubspec_declares_build_runner(self) -> None:
        content = (FIXTURE_ROOT / "pubspec.yaml").read_text(encoding="utf-8")
        assert "build_runner" in content

    def test_main_dart_exists(self) -> None:
        assert (FIXTURE_ROOT / "lib/main.dart").is_file()

    def test_app_dart_exists(self) -> None:
        assert (FIXTURE_ROOT / "lib/app.dart").is_file()

    def test_router_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "lib/router"
        assert d.is_dir()
        assert (d / "app_router.dart").is_file()
        assert (d / "routes.dart").is_file()

    def test_reader_feature_exists(self) -> None:
        d = FIXTURE_ROOT / "lib/features/reader"
        assert d.is_dir()
        assert (d / "domain/document.dart").is_file()
        assert (d / "data/document_remote_source.dart").is_file()
        assert (d / "application/reader_controller.dart").is_file()
        assert (d / "presentation/reader_screen.dart").is_file()

    def test_favorites_feature_exists(self) -> None:
        d = FIXTURE_ROOT / "lib/features/favorites"
        assert d.is_dir()
        assert (d / "domain/favorite.dart").is_file()
        assert (d / "data/favorites_storage.dart").is_file()
        assert (d / "application/favorites_controller.dart").is_file()
        assert (d / "presentation/favorites_screen.dart").is_file()

    def test_settings_feature_exists(self) -> None:
        d = FIXTURE_ROOT / "lib/features/settings"
        assert d.is_dir()
        assert (d / "application/settings_controller.dart").is_file()
        assert (d / "presentation/settings_screen.dart").is_file()

    def test_platform_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "lib/platform"
        assert d.is_dir()
        assert (d / "native_method_channel.dart").is_file()
        assert (d / "platform_widget.dart").is_file()

    def test_android_stub_exists(self) -> None:
        assert (FIXTURE_ROOT / "android_stub/MainActivity.kt").is_file()

    def test_ios_stub_exists(self) -> None:
        assert (FIXTURE_ROOT / "ios_stub/AppDelegate.swift").is_file()

    def test_util_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "lib/util"
        assert d.is_dir()
        assert (d / "logger.dart").is_file()


# ---------------------------------------------------------------------------
# Freezed + build_runner
# ---------------------------------------------------------------------------


class TestBuildRunner:
    def test_domain_documents_have_freezed_part(self) -> None:
        content = (FIXTURE_ROOT / "lib/features/reader/domain/document.dart").read_text(encoding="utf-8")
        assert "@freezed" in content
        assert "part 'document.freezed.dart';" in content
        assert "part 'document.g.dart';" in content

    def test_build_runner_in_dev_dependencies(self) -> None:
        content = (FIXTURE_ROOT / "pubspec.yaml").read_text(encoding="utf-8")
        assert "build_runner" in content


# ---------------------------------------------------------------------------
# Platform channels
# ---------------------------------------------------------------------------


class TestPlatformChannels:
    def test_dart_method_channel_string(self) -> None:
        content = (FIXTURE_ROOT / "lib/platform/native_method_channel.dart").read_text(encoding="utf-8")
        assert "MethodChannel" in content
        # The remote source uses the channel with method strings
        rs_content = (FIXTURE_ROOT / "lib/features/reader/data/document_remote_source.dart").read_text(encoding="utf-8")
        assert "scanDocument" in rs_content

    def test_android_stub_has_method_handler(self) -> None:
        content = (FIXTURE_ROOT / "android_stub/MainActivity.kt").read_text(encoding="utf-8")
        assert "MethodChannel" in content
        assert "scanDocument" in content

    def test_ios_stub_has_method_handler(self) -> None:
        content = (FIXTURE_ROOT / "ios_stub/AppDelegate.swift").read_text(encoding="utf-8")
        assert "FlutterMethodChannel" in content
        assert "scanDocument" in content


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_freezed_part_directives(self) -> None:
        content = (FIXTURE_ROOT / "lib/features/reader/domain/document.dart").read_text(encoding="utf-8")
        assert "part 'document.freezed.dart';" in content
        assert "part 'document.g.dart';" in content

    def test_e2_riverpod_ref_watch(self) -> None:
        content = (FIXTURE_ROOT / "lib/features/favorites/application/favorites_controller.dart").read_text(encoding="utf-8")
        assert "ref.watch(readerControllerProvider)" in content

    def test_e3_platform_channel_strings(self) -> None:
        rs = (FIXTURE_ROOT / "lib/features/reader/data/document_remote_source.dart").read_text(encoding="utf-8")
        kotlin = (FIXTURE_ROOT / "android_stub/MainActivity.kt").read_text(encoding="utf-8")
        swift = (FIXTURE_ROOT / "ios_stub/AppDelegate.swift").read_text(encoding="utf-8")
        assert "scanDocument" in rs
        assert "scanDocument" in kotlin
        assert "scanDocument" in swift

    def test_e4_go_router_redirect(self) -> None:
        content = (FIXTURE_ROOT / "lib/router/app_router.dart").read_text(encoding="utf-8")
        assert "redirect:" in content
        assert "GoRouter" in content

    def test_e5_dart_define(self) -> None:
        content = (FIXTURE_ROOT / "lib/features/settings/application/settings_controller.dart").read_text(encoding="utf-8")
        assert "bool.fromEnvironment" in content
        assert "FX_ENABLE_PREMIUM" in content

    def test_e6_adaptive_widgets(self) -> None:
        content = (FIXTURE_ROOT / "lib/platform/platform_widget.dart").read_text(encoding="utf-8")
        assert "TargetPlatform.iOS" in content
        assert "CupertinoSwitch" in content


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_reader_no_try_catch(self) -> None:
        content = (FIXTURE_ROOT / "lib/features/reader/application/reader_controller.dart").read_text(encoding="utf-8")
        assert "AsyncNotifier" in content

    def test_p2_silent_catch_on_method_channel(self) -> None:
        content = (FIXTURE_ROOT / "lib/platform/native_method_channel.dart").read_text(encoding="utf-8")
        assert "catch (_)" in content

    def test_p3_router_redirect_ignores_auth(self) -> None:
        content = (FIXTURE_ROOT / "lib/router/app_router.dart").read_text(encoding="utf-8")
        assert "redirect:" in content
        # The redirect lambda body has no check; only checks `state.matchedLocation`
        assert "matchedLocation" in content
        # The body should NOT inspect any token/session/user variable
        redirect_section = content[content.index("redirect:"):]
        content_section = redirect_section[: redirect_section.index("),\n")]
        # Strip comments before checking
        import re
        body_no_comments = re.sub(r"//[^\n]*", "", content_section)
        assert "auth" not in body_no_comments.lower()
        assert "session" not in body_no_comments.lower()
        assert "user" not in body_no_comments.lower()
        assert "token" not in body_no_comments.lower()

    def test_p4_settings_dart_define_and_sp(self) -> None:
        content = (FIXTURE_ROOT / "lib/features/settings/application/settings_controller.dart").read_text(encoding="utf-8")
        assert "enablePremium" in content
        assert "SharedPreferences" in content

    def test_p5_freezed_generates_copyWith(self) -> None:
        content = (FIXTURE_ROOT / "lib/features/reader/domain/document.dart").read_text(encoding="utf-8")
        assert "@freezed" in content

    def test_p6_cupertino_slider_dead(self) -> None:
        content = (FIXTURE_ROOT / "lib/platform/platform_widget.dart").read_text(encoding="utf-8")
        assert "TODO: CupertinoSlider" in content


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_logger_unused(self) -> None:
        helper = (FIXTURE_ROOT / "lib/util/logger.dart").read_text(encoding="utf-8")
        assert "Logger" in helper
        # Check not used in runtime code
        for entity in (FIXTURE_ROOT / "lib").rglob("*.dart"):
            if entity.name == "logger.dart":
                continue
            content = entity.read_text(encoding="utf-8")
            assert "Logger.print" not in content

    def test_s2_default_locale_unused(self) -> None:
        content = (FIXTURE_ROOT / "lib/features/settings/application/settings_controller.dart").read_text(encoding="utf-8")
        assert "_DEFAULT_LOCALE" in content

    def test_s3_format_double_dead(self) -> None:
        content = (FIXTURE_ROOT / "lib/platform/platform_widget.dart").read_text(encoding="utf-8")
        # The function declaration is expected; we only check it is NOT invoked.
        # An invocation matches `_formatDouble(<args>)` excluding the declaration.
        import re
        # Match `_formatDouble(` NOT followed by `double` (declaration form)
        invocations = re.findall(r"_formatDouble\((?!double)", content)
        assert invocations == [], f"_formatDouble invoked: {invocations}"


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-flutter-dart" in content

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