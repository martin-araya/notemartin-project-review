"""Tests del ground truth de fx-csharp-aspnet (F06o)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-csharp-aspnet"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-csharp-aspnet"


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
        assert "pedidos" in names
        assert "facturacion" in names
        assert "reintentos" in names

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
        assert "MediatR" in names
        assert "Microsoft.EntityFrameworkCore.Sqlite" in names
        assert "Microsoft.AspNetCore.Mvc.Testing" in names
        assert "xunit" in names

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
            assert tok.startswith("NPRGT-FXCS-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"bin", "obj", "node_modules", "dist", ".git"}
        skip_files = {"unique_tokens.txt"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".cs", ".csproj", ".json", ".yml", ".yaml",
                                    ".md", ".txt", ".sh", ".sln"):
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

    def test_all_decision_points_resolve(self) -> None:
        gt = _load_gt()
        errors = []
        for f in gt["features"]:
            fid = f["id"]
            for di, dp in enumerate(f.get("decision_points", [])):
                cite = f"{dp['file']}:{dp['line']}"
                errs = check_cite(FIXTURE_ROOT, cite)
                for e in errs:
                    errors.append(f"{fid}/dp[{di}]: {e}")
        if errors:
            pytest.fail("\n".join(errors[:20]))


class TestDotnetStructure:
    def test_csproj(self) -> None:
        assert (FIXTURE_ROOT / "FxAspNet.csproj").is_file()

    def test_tests_csproj(self) -> None:
        assert (FIXTURE_ROOT / "tests/FxAspNet.Tests/FxAspNet.Tests.csproj").is_file()

    def test_program_cs(self) -> None:
        assert (FIXTURE_ROOT / "Program.cs").is_file()

    def test_program_partial(self) -> None:
        program = (FIXTURE_ROOT / "Program.cs").read_text(encoding="utf-8")
        assert "public partial class Program" in program

    def test_appdbcontext(self) -> None:
        assert (FIXTURE_ROOT / "src/Infrastructure/Persistence/AppDbContext.cs").is_file()

    def test_pedido_configuration(self) -> None:
        assert (FIXTURE_ROOT / "src/Infrastructure/Persistence/Configurations/PedidoConfiguration.cs").is_file()

    def test_factura_configuration(self) -> None:
        assert (FIXTURE_ROOT / "src/Infrastructure/Persistence/Configurations/FacturaConfiguration.cs").is_file()

    def test_trabajo_configuration(self) -> None:
        assert (FIXTURE_ROOT / "src/Infrastructure/Persistence/Configurations/TrabajoConfiguration.cs").is_file()

    def test_orders_endpoints(self) -> None:
        assert (FIXTURE_ROOT / "src/Web/Endpoints/OrdersEndpoints.cs").is_file()

    def test_billing_endpoints(self) -> None:
        assert (FIXTURE_ROOT / "src/Web/Endpoints/BillingEndpoints.cs").is_file()

    def test_retries_endpoints(self) -> None:
        assert (FIXTURE_ROOT / "src/Web/Endpoints/RetriesEndpoints.cs").is_file()

    def test_background_service(self) -> None:
        assert (FIXTURE_ROOT / "src/Infrastructure/Background/ReintentosBackgroundService.cs").is_file()

    def test_tests_dir(self) -> None:
        assert (FIXTURE_ROOT / "tests/FxAspNet.Tests").is_dir()


class TestEcosystemTraps:
    def test_e01_mediator_by_type(self) -> None:
        h = (FIXTURE_ROOT / "src/Features/Pedidos/Commands/CrearPedidoHandler.cs").read_text(encoding="utf-8")
        assert "IRequestHandler<CrearPedidoCommand" in h

    def test_e02_fluent_no_dataannotations(self) -> None:
        ctx = (FIXTURE_ROOT / "src/Infrastructure/Persistence/AppDbContext.cs").read_text(encoding="utf-8")
        assert "ApplyConfigurationsFromAssembly" in ctx
        cfg = (FIXTURE_ROOT / "src/Infrastructure/Persistence/Configurations/PedidoConfiguration.cs").read_text(encoding="utf-8")
        assert "IEntityTypeConfiguration<Pedido>" in cfg
        entity = (FIXTURE_ROOT / "src/Domain/Pedidos/Pedido.cs").read_text(encoding="utf-8")
        assert "DataAnnotations" not in entity

    def test_e03_source_generators(self) -> None:
        csproj = (FIXTURE_ROOT / "FxAspNet.csproj").read_text(encoding="utf-8")
        assert "MediatR" in csproj

    def test_e04_partial_class(self) -> None:
        a = (FIXTURE_ROOT / "src/Domain/Pedidos/PedidoItem.cs").read_text(encoding="utf-8")
        b = (FIXTURE_ROOT / "src/Domain/Pedidos/PedidoItem.ParteB.cs").read_text(encoding="utf-8")
        assert "public partial class PedidoItem" in a
        assert "public partial class PedidoItem" in b

    def test_e05_pipeline_order(self) -> None:
        program = (FIXTURE_ROOT / "Program.cs").read_text(encoding="utf-8")
        idx_map = program.index("MapOrdersEndpoints")
        idx_exc = program.index("UseExceptionHandler")
        assert idx_map < idx_exc, "UseExceptionHandler debe ir despues de MapOrdersEndpoints (trampa)"

    def test_e06_extension_method(self) -> None:
        m = (FIXTURE_ROOT / "src/Infrastructure/Mediator/MediatorRegistration.cs").read_text(encoding="utf-8")
        assert "AddOrdersModule" in m
        program = (FIXTURE_ROOT / "Program.cs").read_text(encoding="utf-8")
        assert "AddOrdersModule()" not in program


class TestPackageTraps:
    def test_p01_invalid_operation_caught(self) -> None:
        ep = (FIXTURE_ROOT / "src/Web/Endpoints/OrdersEndpoints.cs").read_text(encoding="utf-8")
        assert "cliente_requerido" in ep
        assert "BadRequest" in ep

    def test_p02_comando_sin_handler_existe(self) -> None:
        c = (FIXTURE_ROOT / "src/Features/Pedidos/Commands/ComandoSinHandler.cs").read_text(encoding="utf-8")
        assert "ComandoSinHandler" in c
        assert "IRequest" in c

    def test_p03_two_saves(self) -> None:
        h = (FIXTURE_ROOT / "src/Features/Pedidos/Commands/CrearPedidoHandler.cs").read_text(encoding="utf-8")
        assert h.count("SaveChangesAsync") >= 2

    def test_p04_background_no_update_ultimo(self) -> None:
        bg = (FIXTURE_ROOT / "src/Infrastructure/Background/ReintentosBackgroundService.cs").read_text(encoding="utf-8")
        assert "Fallido" in bg
        assert "LogWarning" in bg
        bloque = bg[bg.index("TrabajoEstado.Fallido"):]
        assert "UltimoIntentoEn" not in bloque

    def test_p05_route_prefix(self) -> None:
        ep = (FIXTURE_ROOT / "src/Web/Endpoints/OrdersEndpoints.cs").read_text(encoding="utf-8")
        assert 'MapGet("/' in ep
        assert 'MapGet("/{id:int}"' in ep

    def test_p06_shared_cache(self) -> None:
        f = (FIXTURE_ROOT / "tests/FxAspNet.Tests/Fixtures/FxAspNetFactory.cs").read_text(encoding="utf-8")
        assert "cache=shared" in f


class TestSuperficialTraps:
    def test_s01_validator_dead(self) -> None:
        v = (FIXTURE_ROOT / "src/Features/Pedidos/Commands/CrearPedidoValidator.cs").read_text(encoding="utf-8")
        assert "Validar" in v

    def test_s02_logger_dead(self) -> None:
        c = (FIXTURE_ROOT / "src/Infrastructure/Persistence/AppDbContext.cs").read_text(encoding="utf-8")
        assert "_log" in c

    def test_s03_health_endpoint(self) -> None:
        ep = (FIXTURE_ROOT / "src/Web/Endpoints/OrdersEndpoints.cs").read_text(encoding="utf-8")
        assert 'MapGet("/health"' in ep


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-csharp-aspnet" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_csproj_has_mediatr(self) -> None:
        csproj = (FIXTURE_ROOT / "FxAspNet.csproj").read_text(encoding="utf-8")
        assert "MediatR" in csproj
        assert "Microsoft.EntityFrameworkCore.Sqlite" in csproj

    def test_csproj_tests_has_xunit(self) -> None:
        csproj = (FIXTURE_ROOT / "tests/FxAspNet.Tests/FxAspNet.Tests.csproj").read_text(encoding="utf-8")
        assert "xunit" in csproj
        assert "Microsoft.AspNetCore.Mvc.Testing" in csproj

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 25
        for tok in tokens:
            assert tok.startswith("NPRGT-FXCS-")