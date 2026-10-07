"""Tests del ground truth de fx-kotlin-ktor (F06n)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-kotlin-ktor"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-kotlin-ktor"


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
        assert "inventario" in names
        assert "reservas-de-stock" in names
        assert "alertas" in names

    def test_each_feature_has_7_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n == 7, f"{f['id']}: expected 7, got {n}"

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
        assert "ktor-server-core" in names
        assert "koin-ktor" in names
        assert "exposed-core" in names
        assert "kotlinx-coroutines-core" in names

    def test_surfaces_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("surfaces", [])) >= 12


class TestUniqueTokensFile:
    def test_at_least_20_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20, f"only {len(tokens)} tokens"

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXKTOR-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"node_modules", "build", ".gradle", "dist", ".git"}
        skip_files = {"unique_tokens.txt", "gradle.lockfile"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".kt", ".kts", ".sql", ".yml", ".yaml",
                                    ".md", ".txt", ".sh"):
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


class TestKotlinStructure:
    def test_gradle_kts(self) -> None:
        assert (FIXTURE_ROOT / "build.gradle.kts").is_file()

    def test_settings_gradle_kts(self) -> None:
        assert (FIXTURE_ROOT / "settings.gradle.kts").is_file()

    def test_gradle_properties(self) -> None:
        assert (FIXTURE_ROOT / "gradle.properties").is_file()

    def test_fxktor_application(self) -> None:
        assert (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/FxKtorApplication.kt").is_file()

    def test_plugins(self) -> None:
        for p in ("Routing", "Auth", "StatusPages", "Serializacion", "Monitoring"):
            assert (FIXTURE_ROOT / f"src/main/kotlin/com/example/fxktor/plugins/{p}.kt").is_file(), f"missing {p}.kt"

    def test_di(self) -> None:
        assert (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/di/AppModule.kt").is_file()

    def test_domain(self) -> None:
        for d in ("Item", "StockEvent", "Alert"):
            assert (FIXTURE_ROOT / f"src/main/kotlin/com/example/fxktor/domain/{d}.kt").is_file(), f"missing {d}.kt"

    def test_repositories(self) -> None:
        for r in ("ItemRepository", "AlertRepository"):
            assert (FIXTURE_ROOT / f"src/main/kotlin/com/example/fxktor/repository/{r}.kt").is_file(), f"missing {r}.kt"

    def test_services(self) -> None:
        for s in ("InventarioService", "AlertasService"):
            assert (FIXTURE_ROOT / f"src/main/kotlin/com/example/fxktor/service/{s}.kt").is_file(), f"missing {s}.kt"

    def test_routes(self) -> None:
        for r in ("InventarioRoutes", "ReservasRoutes", "AlertasRoutes"):
            assert (FIXTURE_ROOT / f"src/main/kotlin/com/example/fxktor/routes/{r}.kt").is_file(), f"missing {r}.kt"

    def test_tests_dir(self) -> None:
        assert (FIXTURE_ROOT / "src/test/kotlin").is_dir()


class TestKtorSource:
    def test_kotlin_application_annotation(self) -> None:
        app = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/FxKtorApplication.kt").read_text(encoding="utf-8")
        assert "fun main()" in app
        assert "embeddedServer" in app

    def test_routing_dsl_with_extension_functions(self) -> None:
        r = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/plugins/Routing.kt").read_text(encoding="utf-8")
        assert "fun Route.routes()" in r
        assert "inventario()" in r
        assert "reservas()" in r
        assert "alertas()" in r

    def test_koin_in_app_module(self) -> None:
        m = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/di/AppModule.kt").read_text(encoding="utf-8")
        assert "module" in m
        assert "single" in m

    def test_koincomponent_with_by_inject(self) -> None:
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/service/InventarioService.kt").read_text(encoding="utf-8")
        assert "KoinComponent" in s
        assert "by inject()" in s

    def test_exposed_table_in_repository(self) -> None:
        r = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/repository/ItemRepository.kt").read_text(encoding="utf-8")
        assert "Table(\"items\")" in r
        assert "selectAll" in r

    def test_sealed_class_with_subtypes(self) -> None:
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/domain/StockEvent.kt").read_text(encoding="utf-8")
        assert "@Serializable" in s
        assert "sealed class StockEvent" in s
        assert "data class ItemCreated" in s
        assert "data class ItemUpdated" in s
        assert "data class ItemDeleted" in s

    def test_flow_emission(self) -> None:
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/service/InventarioService.kt").read_text(encoding="utf-8")
        assert "Flow<Item>" in s
        assert "flow {" in s

    def test_coroutines_launch_in_service(self) -> None:
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/service/AlertasService.kt").read_text(encoding="utf-8")
        assert "scope.launch" in s
        assert "CoroutineScope" in s


class TestTrapsEcosystem:
    def test_e01_dsl_nested(self) -> None:
        r = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/plugins/Routing.kt").read_text(encoding="utf-8")
        assert "fun Route.routes()" in r
        # Las 3 extension functions se llaman.
        assert "inventario()" in r and "reservas()" in r and "alertas()" in r

    def test_e02_plugins_installed(self) -> None:
        a = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/plugins/Auth.kt").read_text(encoding="utf-8")
        sp = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/plugins/StatusPages.kt").read_text(encoding="utf-8")
        assert "install(Authentication)" in a
        assert "install(StatusPages)" in sp

    def test_e03_extension_functions(self) -> None:
        for p in ("InventarioRoutes", "ReservasRoutes", "AlertasRoutes"):
            src = (FIXTURE_ROOT / f"src/main/kotlin/com/example/fxktor/routes/{p}.kt").read_text(encoding="utf-8")
            assert "fun Route." in src

    def test_e04_coroutines_flow(self) -> None:
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/service/InventarioService.kt").read_text(encoding="utf-8")
        assert "flow {" in s
        assert "emit(it)" in s

    def test_e05_sealed_class_when(self) -> None:
        d = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/domain/StockEvent.kt").read_text(encoding="utf-8")
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/service/InventarioService.kt").read_text(encoding="utf-8")
        assert "sealed class" in d
        assert "is StockEvent.ItemCreated" in s
        assert "is StockEvent.ItemUpdated" in s
        assert "is StockEvent.ItemDeleted" in s

    def test_e06_delegated_property(self) -> None:
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/service/InventarioService.kt").read_text(encoding="utf-8")
        assert "by inject()" in s
        assert "KoinComponent" in s


class TestTrapsPackage:
    def test_p01_routing_sin_auth(self) -> None:
        main = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/FxKtorApplication.kt").read_text(encoding="utf-8")
        assert "routing { routes() }" in main
        # auth() no se llama en FxKtorApplication.
        assert "auth()" not in main

    def test_p02_sealed_class_when_statement(self) -> None:
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/service/InventarioService.kt").read_text(encoding="utf-8")
        # El when en handle() cubre los 3 subtipos conocidos.
        assert "is StockEvent.ItemCreated" in s
        assert "is StockEvent.ItemUpdated" in s
        assert "is StockEvent.ItemDeleted" in s
        # La trampa es que un nuevo subtipo (e.g. ItemArchived) no
        # actualizaria este when y el codigo compila como
        # statement fallando en runtime.
        assert "ItemArchived" not in s

    def test_p03_flow_sin_buffer(self) -> None:
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/service/InventarioService.kt").read_text(encoding="utf-8")
        assert "Flow<Item>" in s
        # Verificamos que el codigo no llama a operaciones de
        # backpressure (.conflate, .buffer, .sample, etc).
        # El Flow se construye con `flow { emit(it) }` simple.
        assert ".conflate()" not in s
        assert ".sample(" not in s

    def test_p04_by_inject_no_lazy(self) -> None:
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/service/InventarioService.kt").read_text(encoding="utf-8")
        assert "by inject()" in s
        # La trampa es que by inject() no es lazy; el @Lazy
        # property delegate seria la forma correcta.
        assert "val repo: ItemRepository by lazy" not in s

    def test_p05_exposed_sin_transaccion(self) -> None:
        r = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/repository/ItemRepository.kt").read_text(encoding="utf-8")
        # listAll() ejecuta selectAll() sin envolver en transaction { }.
        # El bloque transaction solo aparece en init().
        assert "transaction(db)" in r
        # Verificamos que la query no este dentro del bloque
        # transaction.
        m = re.search(r"fun listAll.*?(?=fun|\Z)", r, re.DOTALL)
        assert m is not None
        assert "transaction" not in m.group(0)

    def test_p06_kotlinx_serializacion_sealed(self) -> None:
        d = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/domain/StockEvent.kt").read_text(encoding="utf-8")
        assert "@Serializable" in d
        assert "sealed class" in d


class TestTrapsSuperficial:
    def test_s01_inventario_audit_dead(self) -> None:
        r = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/routes/InventarioRoutes.kt").read_text(encoding="utf-8")
        assert "/audit" in r

    def test_s02_sendEmail_dead(self) -> None:
        s = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/service/AlertasService.kt").read_text(encoding="utf-8")
        assert "sendEmail" in s

    def test_s03_dummy_logger_no_usado(self) -> None:
        d = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/di/AppModule.kt").read_text(encoding="utf-8")
        assert "DummyLogger" in d
        m = (FIXTURE_ROOT / "src/main/kotlin/com/example/fxktor/plugins/Monitoring.kt").read_text(encoding="utf-8")
        assert "DummyLogger" not in m


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-kotlin-ktor" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_gradle_has_ktor(self) -> None:
        gradle = (FIXTURE_ROOT / "build.gradle.kts").read_text(encoding="utf-8")
        assert "ktor-server-core" in gradle
        assert "koin-ktor" in gradle
        assert "exposed-core" in gradle
        assert "kotlinx-serialization-json" in gradle

    def test_gradle_has_testcontainers(self) -> None:
        gradle = (FIXTURE_ROOT / "build.gradle.kts").read_text(encoding="utf-8")
        # No usamos testcontainers aqui (usa H2), pero verificamos
        # ktor-server-test-host.
        assert "ktor-server-test-host" in gradle
        assert "koin-test" in gradle

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20
        for tok in tokens:
            assert tok.startswith("NPRGT-FXKTOR-")
