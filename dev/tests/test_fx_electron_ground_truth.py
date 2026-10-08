"""Tests del ground truth de fx-electron (F06af)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-electron"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-electron"


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
        assert "abrir-proyecto" in names
        assert "exportar-pdf" in names
        assert "actualización-automática" in names

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
        assert "electron" in names
        assert "electron-builder" in names
        assert "vitest" in names
        assert "esbuild" in names

    def test_entry_points_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("entry_points", [])) >= 12

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
            assert tok.startswith("NPRGT-FXELEC-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {
            "node_modules", "dist", "release", "out", ".git",
            ".yarn-cache", ".cache", "coverage", "Generated"
        }
        skip_files = {
            "unique_tokens.txt", "build-history.sh", "package-lock.json",
            "yarn.lock", ".metadata", "icon.png"
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
                ".ts", ".tsx", ".js", ".mjs", ".cjs", ".json",
                ".md", ".txt", ".sh", ".yml", ".yaml", ".xml",
                ".css", ".html",
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
# Electron structure
# ---------------------------------------------------------------------------


class TestElectronStructure:
    def test_package_json_exists(self) -> None:
        assert (FIXTURE_ROOT / "package.json").is_file()

    def test_package_json_declares_electron(self) -> None:
        content = (FIXTURE_ROOT / "package.json").read_text(encoding="utf-8")
        assert "electron" in content

    def test_package_json_declares_electron_builder(self) -> None:
        content = (FIXTURE_ROOT / "package.json").read_text(encoding="utf-8")
        assert "electron-builder" in content

    def test_package_json_declares_vitest(self) -> None:
        content = (FIXTURE_ROOT / "package.json").read_text(encoding="utf-8")
        assert "vitest" in content

    def test_tsconfig_main_exists(self) -> None:
        assert (FIXTURE_ROOT / "tsconfig.main.json").is_file()

    def test_tsconfig_renderer_exists(self) -> None:
        assert (FIXTURE_ROOT / "tsconfig.renderer.json").is_file()

    def test_electron_builder_yml_exists(self) -> None:
        assert (FIXTURE_ROOT / "electron-builder.yml").is_file()

    def test_main_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/main"
        assert d.is_dir()
        assert (d / "index.ts").is_file()
        assert (d / "windows.ts").is_file()
        assert (d / "autoUpdater.ts").is_file()

    def test_main_ipc_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/main/ipc"
        assert d.is_dir()
        assert (d / "handlers.ts").is_file()
        assert (d / "channels.ts").is_file()

    def test_main_menu_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/main/menu"
        assert d.is_dir()
        assert (d / "appMenu.ts").is_file()

    def test_main_protocol_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/main/protocol"
        assert d.is_dir()
        assert (d / "appProtocol.ts").is_file()

    def test_main_workers_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/main/workers"
        assert d.is_dir()
        assert (d / "updater.ts").is_file()
        assert (d / "pdfExporter.ts").is_file()

    def test_preload_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/preload"
        assert d.is_dir()
        assert (d / "index.ts").is_file()
        assert (d / "api.ts").is_file()

    def test_renderer_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/renderer"
        assert d.is_dir()
        assert (d / "index.html").is_file()
        assert (d / "renderer.ts").is_file()
        assert (d / "styles.css").is_file()

    def test_workers_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/workers"
        assert d.is_dir()
        assert (d / "updater-worker.ts").is_file()
        assert (d / "pdf-worker.ts").is_file()

    def test_resources_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "resources"
        assert d.is_dir()
        assert (d / "native-menu.json").is_file()
        assert (d / "translations.json").is_file()

    def test_util_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/main/util"
        assert d.is_dir()
        assert (d / "legacyLogger.ts").is_file()
        assert (d / "featureFlags.ts").is_file()


# ---------------------------------------------------------------------------
# Electron builder config
# ---------------------------------------------------------------------------


class TestElectronBuilder:
    def test_electron_builder_has_asar_unpack(self) -> None:
        content = (FIXTURE_ROOT / "electron-builder.yml").read_text(encoding="utf-8")
        assert "asarUnpack" in content

    def test_electron_builder_has_extra_resources(self) -> None:
        content = (FIXTURE_ROOT / "electron-builder.yml").read_text(encoding="utf-8")
        assert "extraResources" in content

    def test_electron_builder_has_multiple_targets(self) -> None:
        content = (FIXTURE_ROOT / "electron-builder.yml").read_text(encoding="utf-8")
        assert "mac:" in content
        assert "win:" in content
        assert "linux:" in content


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_ipc_channels_strings(self) -> None:
        content = (FIXTURE_ROOT / "src/main/ipc/handlers.ts").read_text(encoding="utf-8")
        assert "project:open" in content
        assert "pdf:export" in content
        assert "update:check" in content
        assert "ipcMain.handle" in content

    def test_e2_context_bridge(self) -> None:
        content = (FIXTURE_ROOT / "src/preload/index.ts").read_text(encoding="utf-8")
        assert "contextBridge" in content
        assert "exposeInMainWorld" in content
        assert "'api'" in content

    def test_e3_menu_accelerators(self) -> None:
        content = (FIXTURE_ROOT / "src/main/menu/appMenu.ts").read_text(encoding="utf-8")
        assert "Menu.buildFromTemplate" in content
        assert "accelerator" in content
        assert "CmdOrCtrl+O" in content
        assert "CmdOrCtrl+E" in content

    def test_e4_utility_process(self) -> None:
        updater = (FIXTURE_ROOT / "src/main/workers/updater.ts").read_text(encoding="utf-8")
        assert "utilityProcess.fork" in updater
        pdf = (FIXTURE_ROOT / "src/main/workers/pdfExporter.ts").read_text(encoding="utf-8")
        assert "fork" in pdf

    def test_e5_app_protocol(self) -> None:
        content = (FIXTURE_ROOT / "src/main/protocol/appProtocol.ts").read_text(encoding="utf-8")
        assert "'app'" in content
        assert "protocol.handle" in content
        assert "registerSchemesAsPrivileged" in content

    def test_e6_electron_builder(self) -> None:
        content = (FIXTURE_ROOT / "electron-builder.yml").read_text(encoding="utf-8")
        assert "asarUnpack" in content
        assert "extraResources" in content


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_ipc_no_try_catch(self) -> None:
        content = (FIXTURE_ROOT / "src/main/ipc/handlers.ts").read_text(encoding="utf-8")
        # The PROJECT_OPEN handler should NOT wrap readFile in try/catch
        # Find the handler body
        idx = content.index("IPC_CHANNELS.PROJECT_OPEN")
        next_handler_idx = content.find("IPC_CHANNELS.", idx + 30)
        if next_handler_idx == -1:
            body = content[idx:]
        else:
            body = content[idx:next_handler_idx]
        assert "try {" not in body

    def test_p2_menu_accelerator_duplicated(self) -> None:
        content = (FIXTURE_ROOT / "src/main/menu/appMenu.ts").read_text(encoding="utf-8")
        occurrences = (content.count("'CmdOrCtrl+O'"))
        assert occurrences >= 2

    def test_p3_utility_process_no_exit_handler(self) -> None:
        content = (FIXTURE_ROOT / "src/main/workers/updater.ts").read_text(encoding="utf-8")
        assert "utilityProcess.fork" in content
        assert "on('exit'" not in content

    def test_p4_context_bridge_no_function(self) -> None:
        content = (FIXTURE_ROOT / "src/preload/index.ts").read_text(encoding="utf-8")
        # Should expose plain functions, not Function references
        assert "ipcRenderer.invoke" in content

    def test_p5_protocol_register_privileged_before(self) -> None:
        content = (FIXTURE_ROOT / "src/main/protocol/appProtocol.ts").read_text(encoding="utf-8")
        reg_idx = content.index("registerSchemesAsPrivileged")
        handle_idx = content.index("protocol.handle")
        assert reg_idx < handle_idx

    def test_p6_autoupdater_http_not_https(self) -> None:
        content = (FIXTURE_ROOT / "src/main/autoUpdater.ts").read_text(encoding="utf-8")
        assert "setFeedURL" in content
        assert "http://example.com/updates" in content


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_legacy_logger_unused(self) -> None:
        logger_src = (FIXTURE_ROOT / "src/main/util/legacyLogger.ts").read_text(encoding="utf-8")
        assert "LegacyLogger" in logger_src
        # Check not used in runtime code
        for rel in [
            "src/main/index.ts",
            "src/main/ipc/handlers.ts",
            "src/main/workers/updater.ts",
        ]:
            content = (FIXTURE_ROOT / rel).read_text(encoding="utf-8")
            assert "LegacyLogger" not in content

    def test_s2_feature_flags_unread(self) -> None:
        flags_src = (FIXTURE_ROOT / "src/main/util/featureFlags.ts").read_text(encoding="utf-8")
        assert "ENABLE_BETA" in flags_src
        for rel in [
            "src/main/index.ts",
            "src/main/windows.ts",
        ]:
            content = (FIXTURE_ROOT / rel).read_text(encoding="utf-8")
            assert "ENABLE_BETA" not in content

    def test_s3_format_timestamp_unused(self) -> None:
        api_src = (FIXTURE_ROOT / "src/preload/api.ts").read_text(encoding="utf-8")
        assert "formatTimestamp" in api_src
        preload_src = (FIXTURE_ROOT / "src/preload/index.ts").read_text(encoding="utf-8")
        assert "formatTimestamp" not in preload_src


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-electron" in content

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