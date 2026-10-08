"""Tests del ground truth de fx-swift-server (F06ab)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-swift-server"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-swift-server"


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
        assert "api-de-notas" in names
        assert "cli-de-importacion" in names
        assert "auditoria" in names

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
        assert "swift" in names
        assert "vapor" in names
        assert "fluent" in names
        assert "swift-argument-parser" in names
        assert "swift-syntax" in names

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
            assert tok.startswith("NPRGT-FXSWIFTSRV-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {
            "build", "vendor", "node_modules", ".git", ".bundle", "tmp",
            "log", "storage", ".build", ".swiftpm", "DerivedData"
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
            where = t.get("file", "")
            # Strip optional :line suffix
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
# Swift structure
# ---------------------------------------------------------------------------


class TestSwiftStructure:
    def test_package_swift_exists(self) -> None:
        assert (FIXTURE_ROOT / "Package.swift").is_file()

    def test_package_swift_declares_fxswiftserver(self) -> None:
        content = (FIXTURE_ROOT / "Package.swift").read_text(encoding="utf-8")
        assert "FxSwiftServer" in content

    def test_package_swift_declares_vapor(self) -> None:
        content = (FIXTURE_ROOT / "Package.swift").read_text(encoding="utf-8")
        assert "vapor" in content.lower()

    def test_package_swift_declares_swift_syntax(self) -> None:
        content = (FIXTURE_ROOT / "Package.swift").read_text(encoding="utf-8")
        assert "swift-syntax" in content

    def test_package_swift_declares_argument_parser(self) -> None:
        content = (FIXTURE_ROOT / "Package.swift").read_text(encoding="utf-8")
        assert "argument-parser" in content.lower()

    def test_macros_library_exists(self) -> None:
        assert (FIXTURE_ROOT / "Sources/FxSwiftMacros/FxSwiftMacros.swift").is_file()

    def test_route_macro_exists(self) -> None:
        assert (FIXTURE_ROOT / "Sources/FxSwiftMacros/RouteMacro.swift").is_file()

    def test_import_macro_exists(self) -> None:
        assert (FIXTURE_ROOT / "Sources/FxSwiftMacros/ImportModuleDeclMacro.swift").is_file()

    def test_models_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftServer/Models"
        assert d.is_dir()
        assert (d / "Note.swift").is_file()
        assert (d / "AuditEntry.swift").is_file()

    def test_routes_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftServer/Routes"
        assert d.is_dir()
        assert (d / "NotesRoutes.swift").is_file()
        assert (d / "AuditRoutes.swift").is_file()

    def test_services_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftServer/Services"
        assert d.is_dir()
        assert (d / "NotesService.swift").is_file()
        assert (d / "AuditRecorder.swift").is_file()
        assert (d / "UrlSessionProvider.swift").is_file()

    def test_cli_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "Sources/FxSwiftCLI"
        assert d.is_dir()
        assert (d / "main.swift").is_file()
        assert (d / "Subcommands/ImportNotes.swift").is_file()
        assert (d / "Subcommands/AuditDump.swift").is_file()


# ---------------------------------------------------------------------------
# Plugin contract
# ---------------------------------------------------------------------------


class TestBuildPluginContract:
    def test_plugin_package_swift_exists(self) -> None:
        assert (FIXTURE_ROOT / "Plugins/AuditCodesPlugin/Package.swift").is_file()

    def test_plugin_implementation_exists(self) -> None:
        assert (FIXTURE_ROOT / "Plugins/AuditCodesPlugin/Plugins/AuditCodesPlugin.swift").is_file()

    def test_plugin_declares_buildTool_capability(self) -> None:
        content = (FIXTURE_ROOT / "Plugins/AuditCodesPlugin/Package.swift").read_text(encoding="utf-8")
        assert ".buildTool()" in content

    def test_plugin_implements_buildToolPlugin(self) -> None:
        content = (FIXTURE_ROOT / "Plugins/AuditCodesPlugin/Plugins/AuditCodesPlugin.swift").read_text(encoding="utf-8")
        assert "BuildToolPlugin" in content
        assert "createBuildCommands" in content


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_macros_attached(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftMacros/RouteMacro.swift").read_text(encoding="utf-8")
        assert "PeerMacro" in src or "attached" in src

    def test_e2_build_plugin(self) -> None:
        src = (FIXTURE_ROOT / "Plugins/AuditCodesPlugin/Plugins/AuditCodesPlugin.swift").read_text(encoding="utf-8")
        assert "BuildToolPlugin" in src

    def test_e3_route_collection(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/Routes/NotesRoutes.swift").read_text(encoding="utf-8")
        assert "RouteCollection" in src
        assert "func boot(routes:" in src

    def test_e4_fluent_models(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/Models/Note.swift").read_text(encoding="utf-8")
        assert "@Field" in src
        assert "@Parent" in src
        assert "@Timestamp" in src
        assert "static let schema" in src

    def test_e5_actor_sendable(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/Services/AuditRecorder.swift").read_text(encoding="utf-8")
        dto = (FIXTURE_ROOT / "Sources/FxSwiftServer/DTOs/NoteDTO.swift").read_text(encoding="utf-8")
        assert "actor" in src
        assert "Sendable" in dto

    def test_e6_canimport(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/Services/UrlSessionProvider.swift").read_text(encoding="utf-8")
        assert "#if canImport(FoundationNetworking)" in src
        assert "#endif" in src


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_import_macro(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/App.swift").read_text(encoding="utf-8")
        assert "@ImportModuleDecl" in src

    def test_p2_unchecked_sendable(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/DTOs/LegacyNoteDTO.swift").read_text(encoding="utf-8")
        assert "class" in src
        assert "@unchecked Sendable" in src

    def test_p3_silent_try(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/Services/AuditRecorder.swift").read_text(encoding="utf-8")
        assert "catch" in src
        assert "return false" in src

    def test_p4_plugin_noop(self) -> None:
        src = (FIXTURE_ROOT / "Plugins/AuditCodesPlugin/Plugins/AuditCodesPlugin.swift").read_text(encoding="utf-8")
        assert "noop" in src

    def test_p5_unique_index(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/Migrations/CreateNote.swift").read_text(encoding="utf-8")
        assert ".unique(on:" in src
        # Verify NO IF NOT EXISTS guard (intentional trap P5)
        lines_with_unique = [
            l for l in src.splitlines() if ".unique(on:" in l
        ]
        for line in lines_with_unique:
            assert "IF NOT EXISTS" not in line, f"line {line!r} unexpectedly has IF NOT EXISTS"

    def test_p6_catch_all(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/Routes/AuditRoutes.swift").read_text(encoding="utf-8")
        catch = src.index('routes.get("*"')
        codes = src.index('routes.get("codes"')
        assert catch >= 0
        assert codes >= 0
        assert catch < codes


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_legacy_helper_unused(self) -> None:
        helper = (FIXTURE_ROOT / "Sources/FxSwiftServer/Services/LegacyHelper.swift").read_text(encoding="utf-8")
        assert "LegacyHelper" in helper
        runtime = ["App.swift", "Configure.swift", "Routes/NotesRoutes.swift", "Routes/AuditRoutes.swift"]
        for path in runtime:
            src = (FIXTURE_ROOT / "Sources/FxSwiftServer" / path).read_text(encoding="utf-8")
            assert "LegacyHelper" not in src, f"LegacyHelper referenced in {path}"

    def test_s2_unused_import_else(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/Services/UrlSessionProvider.swift").read_text(encoding="utf-8")
        assert "#else" in src
        assert "_ = URLSession.self" in src

    def test_s3_legacy_mode_env_unused(self) -> None:
        src = (FIXTURE_ROOT / "Sources/FxSwiftServer/Configure.swift").read_text(encoding="utf-8")
        assert "LEGACY_MODE" in src
        assert "_ = legacyMode" in src


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-swift-server" in content

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