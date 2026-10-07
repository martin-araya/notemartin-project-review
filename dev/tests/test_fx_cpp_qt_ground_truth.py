"""Tests del ground truth de fx-cpp-qt (F06z)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-cpp-qt"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-cpp-qt"


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
        assert "editor" in names
        assert "preferencias" in names
        assert "exportar" in names

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
        assert "gcc" in names
        assert "cmake" in names
        assert "qt6-base-dev" in names
        assert "libqt6test6" in names

    def test_surfaces_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("surfaces", [])) >= 12


class TestUniqueTokensFile:
    def test_at_least_25_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 25, f"only {len(tokens)} tokens"

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXCPPQT-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"build", "vendor", "node_modules", ".git", ".bundle", "tmp", "log", "storage"}
        skip_files = {"unique_tokens.txt", "build-history.sh"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(part in skip_dirs for part in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".cpp", ".h", ".hpp", ".ui", ".qml", ".qrc", ".svg",
                                    ".qss", ".py", ".sh", ".yml", ".yaml",
                                    ".json", ".md", ".txt"):
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
                # Skip generated build paths.
                if "build/" in cite or "moc_" in cite or "ui_" in cite or "qrc_" in cite:
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
            candidates = re.findall(r"[\w/.\-]+\.(?:cpp|hpp|h|qml|ui|qrc)", where)
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
            if f and "/" in f:
                full = FIXTURE_ROOT / f
                assert full.is_file(), f"surface {s.get('id')} missing file {f}"


class TestCppStructure:
    def test_cmakelists_exists(self) -> None:
        assert (FIXTURE_ROOT / "CMakeLists.txt").is_file()

    def test_main_cpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/main.cpp").is_file()

    def test_editor_header_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/qtapp/editor.h").is_file()

    def test_preferences_header_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/qtapp/preferences.h").is_file()

    def test_exporter_header_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/qtapp/exporter.h").is_file()

    def test_mainwindow_header_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/qtapp/main_window.h").is_file()

    def test_preferences_proxy_header_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/qtapp/preferences_proxy.h").is_file()

    def test_ui_main_window_exists(self) -> None:
        assert (FIXTURE_ROOT / "ui/main_window.ui").is_file()

    def test_qml_preferences_exists(self) -> None:
        assert (FIXTURE_ROOT / "qml/PreferencesPage.qml").is_file()

    def test_qml_theme_exists(self) -> None:
        assert (FIXTURE_ROOT / "qml/ThemeSwitcher.qml").is_file()

    def test_resources_qrc_exists(self) -> None:
        assert (FIXTURE_ROOT / "resources/resources.qrc").is_file()

    def test_icon_save_exists(self) -> None:
        assert (FIXTURE_ROOT / "resources/icons/save.svg").is_file()

    def test_icon_open_exists(self) -> None:
        assert (FIXTURE_ROOT / "resources/icons/open.svg").is_file()

    def test_icon_export_exists(self) -> None:
        assert (FIXTURE_ROOT / "resources/icons/export.svg").is_file()

    def test_style_exists(self) -> None:
        assert (FIXTURE_ROOT / "resources/styles/app.qss").is_file()

    def test_dockerfile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_test_runner_py_exists(self) -> None:
        assert (FIXTURE_ROOT / "tests/test_runner.py").is_file()


class TestTrapsEcosystem:
    def test_e01_signal_slot(self) -> None:
        c = (FIXTURE_ROOT / "src/main_window.cpp").read_text(encoding="utf-8")
        assert "QObject::connect" in c
        assert "textChanged" in c
        h = (FIXTURE_ROOT / "include/qtapp/editor.h").read_text(encoding="utf-8")
        assert "signals:" in h
        assert "textChanged" in h

    def test_e02_autoconnect(self) -> None:
        h = (FIXTURE_ROOT / "include/qtapp/main_window.h").read_text(encoding="utf-8")
        assert "on_saveButton_clicked" in h
        assert "on_exitButton_clicked" in h
        assert "on_exportButton_clicked" in h
        c = (FIXTURE_ROOT / "src/main_window.cpp").read_text(encoding="utf-8")
        assert "setupUi" in c

    def test_e03_widgets_in_ui(self) -> None:
        u = (FIXTURE_ROOT / "ui/main_window.ui").read_text(encoding="utf-8")
        assert "saveButton" in u
        assert "exitButton" in u
        assert "exportButton" in u
        assert "preferencesButton" in u

    def test_e04_q_property(self) -> None:
        h = (FIXTURE_ROOT / "include/qtapp/preferences.h").read_text(encoding="utf-8")
        assert "Q_PROPERTY" in h
        assert "Q_INVOKABLE" in h
        assert "NOTIFY" in h
        # PreferencesProxy tambien expone Q_PROPERTY para QML.
        hp = (FIXTURE_ROOT / "include/qtapp/preferences_proxy.h").read_text(encoding="utf-8")
        assert "Q_PROPERTY" in hp
        assert "Q_INVOKABLE" in hp

    def test_e05_qrc_resources(self) -> None:
        q = (FIXTURE_ROOT / "resources/resources.qrc").read_text(encoding="utf-8")
        assert "<file>" in q
        assert "save.svg" in q
        assert "open.svg" in q
        assert "export.svg" in q
        c = (FIXTURE_ROOT / "CMakeLists.txt").read_text(encoding="utf-8")
        assert "qt_add_resources" in c

    def test_e06_moc(self) -> None:
        # Todos los headers con Q_OBJECT generan moc.
        for h in ["editor", "preferences", "exporter", "main_window", "preferences_proxy"]:
            path = FIXTURE_ROOT / "include" / "qtapp" / f"{h}.h"
            if h == "preferences_proxy":
                path = FIXTURE_ROOT / "include" / "qtapp" / f"{h}.h"
            content = path.read_text(encoding="utf-8")
            assert "Q_OBJECT" in content
        c = (FIXTURE_ROOT / "CMakeLists.txt").read_text(encoding="utf-8")
        assert "CMAKE_AUTOMOC" in c


class TestTrapsPackage:
    def test_p01_connect_5_args(self) -> None:
        c = (FIXTURE_ROOT / "src/main_window.cpp").read_text(encoding="utf-8")
        assert "P01" in c or "connect_5_args" in c

    def test_p02_signal_loop(self) -> None:
        c = (FIXTURE_ROOT / "src/exporter.cpp").read_text(encoding="utf-8")
        assert "loop" in c
        assert "P02" in c

    def test_p03_q_property_no_notify(self) -> None:
        h = (FIXTURE_ROOT / "include/qtapp/preferences.h").read_text(encoding="utf-8")
        assert "legacyProperty" in h
        # legacyProperty NO tiene NOTIFY.
        idx = h.find("legacyProperty")
        assert "NOTIFY" not in h[idx:idx+200]

    def test_p04_qrc_path(self) -> None:
        # Verificamos que el test del ground truth tiene el comment.
        c = (FIXTURE_ROOT / "tests/test_main.cpp").read_text(encoding="utf-8")
        assert "P04" in c or "qrc_path_no_colon" in c

    def test_p05_typo_slot(self) -> None:
        h = (FIXTURE_ROOT / "include/qtapp/main_window.h").read_text(encoding="utf-8")
        assert "on_savebutton_clicked_TYPO" in h

    def test_p06_qml_garbage_collected(self) -> None:
        c = (FIXTURE_ROOT / "src/preferences_proxy.cpp").read_text(encoding="utf-8")
        assert "P06" in c


class TestTrapsSuperficial:
    def test_s01_dead_signal(self) -> None:
        h = (FIXTURE_ROOT / "include/qtapp/editor.h").read_text(encoding="utf-8")
        assert "someUnusedSignal" in h

    def test_s02_alias(self) -> None:
        q = (FIXTURE_ROOT / "resources/resources.qrc").read_text(encoding="utf-8")
        # Verificamos que el .qrc tiene declaraciones de archivos
        # (puede o no tener alias, pero al menos tiene SVGs).
        assert "<file" in q
        assert ".svg" in q

    def test_s03_commented_connect(self) -> None:
        c = (FIXTURE_ROOT / "src/main_window.cpp").read_text(encoding="utf-8")
        assert "TODO: connect" in c


class TestManifest:
    def test_manifest_file_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name_is_fx_cpp_qt(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "name: fx-cpp-qt" in text

    def test_manifest_requires_linux(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "- linux" in text

    def test_manifest_test_cmd_starts_with_make(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "test_cmd: make test" in text

    def test_manifest_container_enabled(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "enabled: true" in text

    def test_manifest_image_tag_starts_with_npr(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "image_tag: npr-fx-cpp-qt" in text
