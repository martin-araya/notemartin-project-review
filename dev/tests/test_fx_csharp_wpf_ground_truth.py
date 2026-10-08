"""Tests del ground truth de fx-csharp-wpf (F06ag)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite

GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-csharp-wpf"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-csharp-wpf"


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
        assert "clientes" in names
        assert "cotizaciones" in names
        assert "impresión" in names

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
        assert "communitytoolkit-mvvm" in names
        assert "xunit" in names
        assert "wpf" in names

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
            assert tok.startswith("NPRGT-FXWPF-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"bin", "obj", ".vs", ".nuget-cache", "Generated"}
        skip_files = {
            "unique_tokens.txt", "build-history.sh", "Makefile",
            "manifest.yml", "Dockerfile.test", "README.md",
            "FxWpf.sln", "Directory.Build.props",
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
                ".cs", ".xaml", ".csproj", ".sln", ".props", ".targets",
                ".json", ".md", ".txt", ".sh", ".yml", ".yaml",
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
# C# structure
# ---------------------------------------------------------------------------


class TestCSharpStructure:
    def test_solution_exists(self) -> None:
        assert (FIXTURE_ROOT / "FxWpf.sln").is_file()

    def test_directory_build_props_exists(self) -> None:
        assert (FIXTURE_ROOT / "Directory.Build.props").is_file()

    def test_app_csproj_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/FxWpf.App/FxWpf.App.csproj").is_file()

    def test_core_csproj_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/FxWpf.Core/FxWpf.Core.csproj").is_file()

    def test_viewmodels_csproj_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/FxWpf.ViewModels/FxWpf.ViewModels.csproj").is_file()

    def test_tests_csproj_exists(self) -> None:
        assert (FIXTURE_ROOT / "tests/FxWpf.Tests/FxWpf.Tests.csproj").is_file()

    def test_trap_tests_csproj_exists(self) -> None:
        assert (FIXTURE_ROOT / "tests/FxWpf.TrapTests/FxWpf.TrapTests.csproj").is_file()

    def test_core_models_exist(self) -> None:
        d = FIXTURE_ROOT / "src/FxWpf.Core/Models"
        assert d.is_dir()
        assert (d / "Cliente.cs").is_file()
        assert (d / "Cotizacion.cs").is_file()
        assert (d / "Producto.cs").is_file()

    def test_core_interfaces_exist(self) -> None:
        d = FIXTURE_ROOT / "src/FxWpf.Core/Interfaces"
        assert d.is_dir()
        assert (d / "IClienteService.cs").is_file()

    def test_viewmodels_dir_exists(self) -> None:
        d = FIXTURE_ROOT / "src/FxWpf.ViewModels"
        assert d.is_dir()
        assert (d / "ClientesViewModel.cs").is_file()
        assert (d / "CotizacionesViewModel.cs").is_file()
        assert (d / "PrintPreviewViewModel.cs").is_file()
        assert (d / "ShellViewModel.cs").is_file()

    def test_viewmodels_commands_exist(self) -> None:
        d = FIXTURE_ROOT / "src/FxWpf.ViewModels/Commands"
        assert d.is_dir()
        assert (d / "AsyncRelayCommand.cs").is_file()

    def test_app_converters_exist(self) -> None:
        d = FIXTURE_ROOT / "src/FxWpf.App/Converters"
        assert d.is_dir()
        assert (d / "BoolToVisibilityConverter.cs").is_file()
        assert (d / "NullToBoolConverter.cs").is_file()
        assert (d / "CurrencyConverter.cs").is_file()

    def test_app_themes_exist(self) -> None:
        d = FIXTURE_ROOT / "src/FxWpf.App/Themes"
        assert d.is_dir()
        assert (d / "Colors.xaml").is_file()
        assert (d / "Buttons.xaml").is_file()
        assert (d / "Controls.xaml").is_file()

    def test_app_styles_exist(self) -> None:
        d = FIXTURE_ROOT / "src/FxWpf.App/Styles"
        assert d.is_dir()
        assert (d / "ButtonStyles.xaml").is_file()

    def test_app_views_exist(self) -> None:
        d = FIXTURE_ROOT / "src/FxWpf.App/Views"
        assert d.is_dir()
        assert (d / "MainWindow.xaml").is_file()
        assert (d / "MainWindow.xaml.cs").is_file()
        assert (d / "ClientesView.xaml").is_file()
        assert (d / "CotizacionesView.xaml").is_file()
        assert (d / "PrintPreviewView.xaml").is_file()

    def test_app_view_templates_exist(self) -> None:
        d = FIXTURE_ROOT / "src/FxWpf.App/Views/Templates"
        assert d.is_dir()
        assert (d / "ClienteTemplate.xaml").is_file()

    def test_app_xaml_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/FxWpf.App/App.xaml").is_file()
        assert (FIXTURE_ROOT / "src/FxWpf.App/App.xaml.cs").is_file()


# ---------------------------------------------------------------------------
# Package config
# ---------------------------------------------------------------------------


class TestPackageConfig:
    def test_app_csproj_targets_wpf(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/FxWpf.App.csproj").read_text(encoding="utf-8")
        assert "net9.0-windows" in content
        assert "UseWPF" in content

    def test_core_csproj_uses_mvvm_toolkit(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.Core/FxWpf.Core.csproj").read_text(encoding="utf-8")
        assert "CommunityToolkit.Mvvm" in content

    def test_tests_use_xunit(self) -> None:
        content = (FIXTURE_ROOT / "tests/FxWpf.Tests/FxWpf.Tests.csproj").read_text(encoding="utf-8")
        assert "xunit" in content

    def test_viewmodels_csproj_has_mvvm(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.ViewModels/FxWpf.ViewModels.csproj").read_text(encoding="utf-8")
        assert "CommunityToolkit.Mvvm" in content


# ---------------------------------------------------------------------------
# Merged dictionaries (E6)
# ---------------------------------------------------------------------------


class TestMergedDictionaries:
    def test_app_xaml_declares_4_merged(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/App.xaml").read_text(encoding="utf-8")
        sources = re.findall(r'Source="([^"]+)"', content)
        assert len(sources) >= 3
        assert "Themes/Colors.xaml" in sources
        assert "Themes/Buttons.xaml" in sources
        assert "Themes/Controls.xaml" in sources

    def test_app_xaml_registers_3_converters(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/App.xaml").read_text(encoding="utf-8")
        assert "BoolToVisibilityConverter" in content
        assert "NullToBoolConverter" in content
        assert "CurrencyConverter" in content


# ---------------------------------------------------------------------------
# Traps ecosystem
# ---------------------------------------------------------------------------


class TestTrapsEcosystem:
    def test_e1_xaml_bindings(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/Views/MainWindow.xaml").read_text(encoding="utf-8")
        assert "{Binding Title}" in content

    def test_e2_observable_property_and_relay_command(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.ViewModels/ClientesViewModel.cs").read_text(encoding="utf-8")
        assert "[ObservableProperty]" in content
        assert "[RelayCommand]" in content

    def test_e3_data_template_with_datatype(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/Views/Templates/ClienteTemplate.xaml").read_text(encoding="utf-8")
        assert "DataTemplate" in content
        assert "DataType" in content

    def test_e4_value_converters(self) -> None:
        assert (FIXTURE_ROOT / "src/FxWpf.App/Converters/BoolToVisibilityConverter.cs").is_file()
        assert (FIXTURE_ROOT / "src/FxWpf.App/Converters/NullToBoolConverter.cs").is_file()
        assert (FIXTURE_ROOT / "src/FxWpf.App/Converters/CurrencyConverter.cs").is_file()

    def test_e5_style_with_triggers(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/Styles/ButtonStyles.xaml").read_text(encoding="utf-8")
        assert "<Style.Triggers>" in content
        assert "<DataTrigger" in content

    def test_e6_merged_dictionaries(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/App.xaml").read_text(encoding="utf-8")
        assert "MergedDictionaries" in content


# ---------------------------------------------------------------------------
# Traps package
# ---------------------------------------------------------------------------


class TestTrapsPackage:
    def test_p1_no_null_check(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.ViewModels/ClientesViewModel.cs").read_text(encoding="utf-8")
        assert "OnSelectedClienteChanged" in content

    def test_p2_task_run_without_await(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.ViewModels/CotizacionesViewModel.cs").read_text(encoding="utf-8")
        assert "Task.Run" in content

    def test_p3_convert_back_not_impl(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/Converters/BoolToVisibilityConverter.cs").read_text(encoding="utf-8")
        assert "ConvertBack" in content
        assert "NotImplementedException" in content

    def test_p4_overlapping_styles(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/Styles/ButtonStyles.xaml").read_text(encoding="utf-8")
        assert "ButtonStylePrimary" in content
        assert "ButtonStyleOverriding" in content

    def test_p5_can_execute_false(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.ViewModels/Commands/AsyncRelayCommand.cs").read_text(encoding="utf-8")
        assert "CanExecute" in content
        assert "return false" in content

    def test_p6_template_typo(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/Views/Templates/ClienteTemplate.xaml").read_text(encoding="utf-8")
        assert "ClientesViewModel" in content


# ---------------------------------------------------------------------------
# Traps superficial
# ---------------------------------------------------------------------------


class TestTrapsSuperficial:
    def test_s1_legacy_converter_unused(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/Converters/LegacyConverter.cs").read_text(encoding="utf-8")
        assert "LegacyConverter" in content

    def test_s2_fonts_xaml_has_brandfont(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.App/Themes/Fonts.xaml").read_text(encoding="utf-8")
        assert "FontFamily" in content
        assert "BrandFont" in content

    def test_s3_experimental_viewmodel_unused(self) -> None:
        content = (FIXTURE_ROOT / "src/FxWpf.ViewModels/ExperimentalViewModel.cs").read_text(encoding="utf-8")
        assert "ExperimentalViewModel" in content


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


class TestManifest:
    def test_manifest_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name(self) -> None:
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-csharp-wpf" in content

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