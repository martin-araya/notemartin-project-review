"""Tests del ground truth de fx-cpp-cmake (F06x)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-cpp-cmake"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-cpp-cmake"


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
        assert "cargar-plugin" in names
        assert "pipeline-de-filtros" in names
        assert "exportar-resultados" in names

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
        assert "googletest" in names
        assert "dl" in names

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
            assert tok.startswith("NPRGT-FXCPP-"), f"bad prefix: {tok}"

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
            if path.suffix not in (".cpp", ".hpp", ".h", ".md", ".txt", ".sh", ".yml", ".yaml",
                                    ".json", ".erb", ".html", ".css", ".js", ".txt"):
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
            # Extraer archivos .cpp/.hpp/.h/.in y los que tienen un path
            # formado por tokens validos.
            candidates = re.findall(r"[\w/.\-]+\.(?:cpp|hpp|h|in|md|sh|yml|yaml)", where)
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

    def test_config_h_in_exists(self) -> None:
        assert (FIXTURE_ROOT / "cmake/config.h.in").is_file()

    def test_main_cpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/main.cpp").is_file()

    def test_registry_hpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxproc/registry.hpp").is_file()

    def test_pipeline_hpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxproc/pipeline.hpp").is_file()

    def test_x_macros_h_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxproc/x_macros.h").is_file()

    def test_plugin_loader_hpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxproc/plugin_loader.hpp").is_file()

    def test_executor_hpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxproc/executor.hpp").is_file()

    def test_filters_hpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxproc/filters.hpp").is_file()

    def test_result_hpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxproc/result.hpp").is_file()

    def test_version_hpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxproc/version.hpp").is_file()

    def test_plugin_transform_json_cpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "plugins/transform_json/transform_json.cpp").is_file()

    def test_plugin_cmakelists_exists(self) -> None:
        assert (FIXTURE_ROOT / "plugins/transform_json/CMakeLists.txt").is_file()

    def test_export_demo_cpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "apps/export_demo.cpp").is_file()

    def test_deprecated_helpers_hpp_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxproc/util/deprecated_helpers.hpp").is_file()

    def test_dockerfile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_manifest_yml_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()


class TestTrapsEcosystem:
    def test_e01_static_registrar(self) -> None:
        hpp = (FIXTURE_ROOT / "include/fxproc/registry.hpp").read_text(encoding="utf-8")
        assert "class Registrar" in hpp
        assert "Registry::instance().register_filter" in hpp
        cpp = (FIXTURE_ROOT / "src/filters.cpp").read_text(encoding="utf-8")
        assert cpp.count("FX_REGISTER_FILTER") >= 4

    def test_e02_concept_and_crtp(self) -> None:
        hpp = (FIXTURE_ROOT / "include/fxproc/pipeline.hpp").read_text(encoding="utf-8")
        assert "concept Filter" in hpp
        assert "PipelineBase" in hpp
        assert "std::apply" in hpp

    def test_e03_x_macros(self) -> None:
        h = (FIXTURE_ROOT / "include/fxproc/x_macros.h").read_text(encoding="utf-8")
        assert "FX_FILTERS" in h
        assert "X(ToUpper" in h

    def test_e04_cmake_configure(self) -> None:
        cm = (FIXTURE_ROOT / "CMakeLists.txt").read_text(encoding="utf-8")
        assert "configure_file" in cm
        in_text = (FIXTURE_ROOT / "cmake/config.h.in").read_text(encoding="utf-8")
        assert "FX_VERSION" in in_text or "@FXPROC_VERSION@" in in_text

    def test_e05_dlopen_dlsym(self) -> None:
        cpp = (FIXTURE_ROOT / "src/plugin_loader.cpp").read_text(encoding="utf-8")
        assert "dlopen" in cpp
        assert "dlsym" in cpp
        assert "fx_plugin_register" in cpp
        plugin = (FIXTURE_ROOT / "plugins/transform_json/transform_json.cpp").read_text(encoding="utf-8")
        assert 'extern "C"' in plugin
        assert "fx_plugin_register" in plugin

    def test_e06_init_order(self) -> None:
        cpp = (FIXTURE_ROOT / "src/filters.cpp").read_text(encoding="utf-8")
        assert "InitOrderTrap" in cpp
        hpp = (FIXTURE_ROOT / "include/fxproc/filter_base.hpp").read_text(encoding="utf-8")
        assert "virtual" in hpp


class TestTrapsPackage:
    def test_p01_thread_detach(self) -> None:
        cpp = (FIXTURE_ROOT / "src/executor.cpp").read_text(encoding="utf-8")
        assert ".detach()" in cpp

    def test_p02_silent_skip(self) -> None:
        cpp = (FIXTURE_ROOT / "src/filters.cpp").read_text(encoding="utf-8")
        assert "should_skip_filter" in cpp

    def test_p03_deleter_no_check(self) -> None:
        hpp = (FIXTURE_ROOT / "include/fxproc/plugin_loader.hpp").read_text(encoding="utf-8")
        assert "PluginDeleter" in hpp
        assert "dlclose" in hpp

    def test_p04_ofstream_no_excl(self) -> None:
        cpp = (FIXTURE_ROOT / "src/result.cpp").read_text(encoding="utf-8")
        assert "ios::trunc" in cpp
        assert "O_EXCL" not in cpp

    def test_p05_cmake_no_gate(self) -> None:
        cm = (FIXTURE_ROOT / "CMakeLists.txt").read_text(encoding="utf-8")
        assert "add_subdirectory(plugins/transform_json)" in cm
        plugin_cm = (FIXTURE_ROOT / "plugins/transform_json/CMakeLists.txt").read_text(encoding="utf-8")
        assert "if(FX_HAS_PLUGINS)" not in plugin_cm

    def test_p06_xmacro_duplicate(self) -> None:
        h = (FIXTURE_ROOT / "include/fxproc/x_macros.h").read_text(encoding="utf-8")
        # Contar ocurrencias de X(Json, en la primera lista (FX_FILTERS)
        # y la segunda (FX_FILTERS_STMT). Ambas tienen el duplicado.
        count = h.count("X(Json,")
        assert count >= 2


class TestTrapsSuperficial:
    def test_s01_dead_legacy_filter(self) -> None:
        cpp = (FIXTURE_ROOT / "src/filters.cpp").read_text(encoding="utf-8")
        assert "LegacyFilter" in cpp

    def test_s02_deprecated_helpers(self) -> None:
        hpp = (FIXTURE_ROOT / "include/fxproc/util/deprecated_helpers.hpp").read_text(encoding="utf-8")
        assert "old_slugify" in hpp
        assert "split_comma_old" in hpp
        assert "legacy_counter" in hpp

    def test_s03_commented_out_block(self) -> None:
        cpp = (FIXTURE_ROOT / "src/filters.cpp").read_text(encoding="utf-8")
        assert "TODO: soporte para colores" in cpp


class TestManifest:
    def test_manifest_file_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name_is_fx_cpp_cmake(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "name: fx-cpp-cmake" in text

    def test_manifest_requires_linux_macos(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "- linux" in text
        assert "- macos" in text

    def test_manifest_test_cmd_starts_with_make(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "test_cmd: make test" in text

    def test_manifest_container_enabled(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "enabled: true" in text

    def test_manifest_image_tag_starts_with_npr(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "image_tag: npr-fx-cpp-cmake" in text
