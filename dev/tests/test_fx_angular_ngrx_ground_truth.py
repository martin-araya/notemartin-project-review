"""Tests del ground truth de fx-angular-ngrx (F06l)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-angular-ngrx"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-angular-ngrx"


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
        assert "gestion-de-solicitudes" in names
        assert "aprobaciones" in names
        assert "reportes" in names

    def test_each_feature_has_min_6_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n >= 6, f"{f['id']}: only {n} outcomes"

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
        assert "@angular/core" in names
        assert "@ngrx/store" in names
        assert "rxjs" in names
        assert "jest" in names

    def test_surfaces_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("surfaces", [])) >= 10


class TestUniqueTokensFile:
    def test_at_least_20_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20, f"only {len(tokens)} tokens"

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXANGULAR-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"node_modules", "dist", "coverage", ".git", ".angular"}
        skip_files = {"unique_tokens.txt", "package-lock.json"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".ts", ".js", ".mjs", ".cjs",
                                    ".scss", ".css", ".html", ".json", ".yml", ".yaml", ".md", ".txt", ".sh"):
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


class TestAngularStructure:
    def test_angular_json(self) -> None:
        assert (FIXTURE_ROOT / "angular.json").is_file()

    def test_main_ts(self) -> None:
        assert (FIXTURE_ROOT / "src/main.ts").is_file()

    def test_app_component(self) -> None:
        assert (FIXTURE_ROOT / "src/app/app.component.ts").is_file()

    def test_app_config(self) -> None:
        assert (FIXTURE_ROOT / "src/app/app.config.ts").is_file()

    def test_app_routes(self) -> None:
        assert (FIXTURE_ROOT / "src/app/app.routes.ts").is_file()

    def test_core_module(self) -> None:
        assert (FIXTURE_ROOT / "src/app/core/core.module.ts").is_file()

    def test_interceptors(self) -> None:
        assert (FIXTURE_ROOT / "src/app/core/interceptors/auth.interceptor.ts").is_file()
        assert (FIXTURE_ROOT / "src/app/core/interceptors/logging.interceptor.ts").is_file()

    def test_services(self) -> None:
        assert (FIXTURE_ROOT / "src/app/core/services/api.service.ts").is_file()

    def test_pipes_and_directives(self) -> None:
        assert (FIXTURE_ROOT / "src/app/core/pipes/monto.pipe.ts").is_file()
        assert (FIXTURE_ROOT / "src/app/core/directives/contador.directive.ts").is_file()

    def test_solicitudes_module(self) -> None:
        assert (FIXTURE_ROOT / "src/app/solicitudes/solicitudes.module.ts").is_file()

    def test_solicitudes_store(self) -> None:
        for s in ("actions", "reducer", "effects", "state"):
            assert (FIXTURE_ROOT / f"src/app/solicitudes/store/{s}.ts").is_file(), f"missing store/{s}.ts"

    def test_solicitudes_pages(self) -> None:
        for p in ("lista-solicitudes.component", "nueva-solicitud.component", "detalle-solicitud.component"):
            assert (FIXTURE_ROOT / f"src/app/solicitudes/pages/{p}.ts").is_file(), f"missing {p}.ts"

    def test_aprobaciones_module(self) -> None:
        assert (FIXTURE_ROOT / "src/app/aprobaciones/aprobaciones.module.ts").is_file()

    def test_aprobaciones_store(self) -> None:
        for s in ("actions", "reducer", "effects", "state"):
            assert (FIXTURE_ROOT / f"src/app/aprobaciones/store/{s}.ts").is_file(), f"missing store/{s}.ts"

    def test_reportes_module(self) -> None:
        assert (FIXTURE_ROOT / "src/app/reportes/reportes.module.ts").is_file()

    def test_environments(self) -> None:
        assert (FIXTURE_ROOT / "src/environments/environment.ts").is_file()


class TestAngularSource:
    def test_ngrx_store_dependencies(self) -> None:
        pkg = json.loads((FIXTURE_ROOT / "package.json").read_text(encoding="utf-8"))
        for d in ("@ngrx/store", "@ngrx/effects", "@ngrx/entity", "@ngrx/store-devtools"):
            assert d in pkg.get("dependencies", {}), f"missing {d} in dependencies"

    def test_create_action_group_used(self) -> None:
        actions = (FIXTURE_ROOT / "src/app/solicitudes/store/actions.ts").read_text(encoding="utf-8")
        assert "createActionGroup" in actions
        assert "source:" in actions
        assert "Solicitudes" in actions

    def test_create_effect_used(self) -> None:
        effects = (FIXTURE_ROOT / "src/app/solicitudes/store/effects.ts").read_text(encoding="utf-8")
        assert "createEffect" in effects
        assert "switchMap" in effects

    def test_create_entity_adapter_used(self) -> None:
        reducer = (FIXTURE_ROOT / "src/app/solicitudes/store/reducer.ts").read_text(encoding="utf-8")
        assert "createEntityAdapter" in reducer
        assert "getInitialState" in reducer

    def test_http_interceptors_multi_true(self) -> None:
        core = (FIXTURE_ROOT / "src/app/core/core.module.ts").read_text(encoding="utf-8")
        assert "HTTP_INTERCEPTORS" in core
        # Multiple `multi: true`.
        assert core.count("multi: true") >= 2

    def test_for_root_pattern(self) -> None:
        core = (FIXTURE_ROOT / "src/app/core/core.module.ts").read_text(encoding="utf-8")
        assert "static forRoot" in core

    def test_cross_feature_effect(self) -> None:
        eff = (FIXTURE_ROOT / "src/app/aprobaciones/store/effects.ts").read_text(encoding="utf-8")
        assert "SolicitudesActions" in eff
        assert "withLatestFrom" in eff

    def test_monto_pipe_uses_default_currency(self) -> None:
        pipe = (FIXTURE_ROOT / "src/app/core/pipes/monto.pipe.ts").read_text(encoding="utf-8")
        assert "EUR" in pipe

    def test_contador_directive_uses_setinterval(self) -> None:
        d = (FIXTURE_ROOT / "src/app/core/directives/contador.directive.ts").read_text(encoding="utf-8")
        assert "setInterval" in d


class TestTrapsEcosystem:
    def test_e01_action_effect_service(self) -> None:
        effects = (FIXTURE_ROOT / "src/app/solicitudes/store/effects.ts").read_text(encoding="utf-8")
        svc = (FIXTURE_ROOT / "src/app/core/services/api.service.ts").read_text(encoding="utf-8")
        assert "createEffect" in effects
        assert "this.api.listAll" in effects
        assert "listAll" in svc

    def test_e02_create_action_group(self) -> None:
        a = (FIXTURE_ROOT / "src/app/solicitudes/store/actions.ts").read_text(encoding="utf-8")
        assert "createActionGroup" in a
        assert "source:" in a

    def test_e03_rxjs_operators(self) -> None:
        e = (FIXTURE_ROOT / "src/app/solicitudes/store/effects.ts").read_text(encoding="utf-8")
        assert "switchMap" in e
        assert "exhaustMapSafe" in e or "exhaustMap" in e
        assert "mergeMap" in e

    def test_e04_forRoot_forChild(self) -> None:
        core = (FIXTURE_ROOT / "src/app/core/core.module.ts").read_text(encoding="utf-8")
        solicitudes = (FIXTURE_ROOT / "src/app/solicitudes/solicitudes.module.ts").read_text(encoding="utf-8")
        assert "static forRoot" in core
        assert "StoreModule.forFeature" in solicitudes

    def test_e05_http_interceptors_multi(self) -> None:
        core = (FIXTURE_ROOT / "src/app/core/core.module.ts").read_text(encoding="utf-8")
        assert "HTTP_INTERCEPTORS" in core
        assert core.count("multi: true") >= 2

    def test_e06_pipe_directive_custom(self) -> None:
        pipe = (FIXTURE_ROOT / "src/app/core/pipes/monto.pipe.ts").read_text(encoding="utf-8")
        directive = (FIXTURE_ROOT / "src/app/core/directives/contador.directive.ts").read_text(encoding="utf-8")
        assert "@Pipe" in pipe
        assert "@Directive" in directive
        assert "setInterval" in directive


class TestTrapsPackage:
    def test_p01_empty_observable(self) -> None:
        svc = (FIXTURE_ROOT / "src/app/core/services/api.service.ts").read_text(encoding="utf-8")
        assert "of([])" in svc

    def test_p02_auth_interceptor_ssr(self) -> None:
        ic = (FIXTURE_ROOT / "src/app/core/interceptors/auth.interceptor.ts").read_text(encoding="utf-8")
        assert "window.localStorage" in ic
        assert "typeof window" in ic

    def test_p03_pipe_not_pure(self) -> None:
        pipe = (FIXTURE_ROOT / "src/app/core/pipes/monto.pipe.ts").read_text(encoding="utf-8")
        assert "private _currency" in pipe

    def test_p04_entity_adapter_no_selectId(self) -> None:
        r = (FIXTURE_ROOT / "src/app/solicitudes/store/reducer.ts").read_text(encoding="utf-8")
        assert "createEntityAdapter<Item>" in r
        assert "selectId:" not in r

    def test_p05_provide_store_duplicate(self) -> None:
        cfg = (FIXTURE_ROOT / "src/app/app.config.ts").read_text(encoding="utf-8")
        assert "provideStore" in cfg
        assert "importProvidersFrom" in cfg
        assert "SolicitudesModule" in cfg

    def test_p06_directive_memory_leak(self) -> None:
        d = (FIXTURE_ROOT / "src/app/core/directives/contador.directive.ts").read_text(encoding="utf-8")
        assert "OnInit" in d
        assert "setInterval" in d
        assert "OnDestroy" not in d
        assert "clearInterval" not in d


class TestTrapsSuperficial:
    def test_s01_api_base_unused(self) -> None:
        svc = (FIXTURE_ROOT / "src/app/core/services/api.service.ts").read_text(encoding="utf-8")
        assert "API_BASE_URL" in svc

    def test_s02_reportes_imports_actions(self) -> None:
        r = (FIXTURE_ROOT / "src/app/reportes/pages/reportes.component.ts").read_text(encoding="utf-8")
        assert "SolicitudesActions" in r

    def test_s03_contador_input_public(self) -> None:
        d = (FIXTURE_ROOT / "src/app/core/directives/contador.directive.ts").read_text(encoding="utf-8")
        assert "@Input" in d
        assert "fxContador" in d


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-angular-ngrx" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_package_json_has_ngrx(self) -> None:
        pkg = json.loads((FIXTURE_ROOT / "package.json").read_text(encoding="utf-8"))
        assert "@ngrx/store" in pkg.get("dependencies", {})

    def test_package_json_has_angular_core(self) -> None:
        pkg = json.loads((FIXTURE_ROOT / "package.json").read_text(encoding="utf-8"))
        assert "@angular/core" in pkg.get("dependencies", {})

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20
        for tok in tokens:
            assert tok.startswith("NPRGT-FXANGULAR-")
