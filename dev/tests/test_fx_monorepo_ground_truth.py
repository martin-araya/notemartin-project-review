"""Tests del ground truth de fx-monorepo (F06d)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-monorepo"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-monorepo"


def _load_gt() -> dict:
    return json.loads((GT_DIR / "ground_truth.json").read_text(encoding="utf-8"))


class TestGroundTruthShape:
    def test_file_exists(self) -> None:
        assert (GT_DIR / "ground_truth.json").is_file()

    def test_has_3_features(self) -> None:
        gt = _load_gt()
        assert len(gt["features"]) >= 3

    def test_each_feature_has_min_6_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n >= 6, f"{f['id']}: only {n} outcomes"

    def test_has_6_ecosystem_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["traps"]) >= 6

    def test_has_6_package_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["package_traps"]) >= 6

    def test_features_are_the_documented_ones(self) -> None:
        gt = _load_gt()
        names = {f["name"] for f in gt["features"]}
        assert "login" in names
        assert "listado-con-filtros" in names
        assert "exportar-reporte" in names

    def test_surfaces_includes_http_and_pages(self) -> None:
        gt = _load_gt()
        kinds = {s["kind"] for s in gt["surfaces"]}
        assert "http" in kinds
        assert "page" in kinds


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


class TestMonorepoStructure:
    def test_workspace_root_files_exist(self) -> None:
        assert (FIXTURE_ROOT / "package.json").is_file()
        assert (FIXTURE_ROOT / "pnpm-workspace.yaml").is_file()
        assert (FIXTURE_ROOT / "turbo.json").is_file()
        assert (FIXTURE_ROOT / ".npmrc").is_file()

    def test_three_packages_exist(self) -> None:
        assert (FIXTURE_ROOT / "libs/shared/package.json").is_file()
        assert (FIXTURE_ROOT / "apps/api/package.json").is_file()
        assert (FIXTURE_ROOT / "apps/web/package.json").is_file()

    def test_libs_shared_uses_workspace_protocol(self) -> None:
        pkg_api = json.loads((FIXTURE_ROOT / "apps/api/package.json").read_text(encoding="utf-8"))
        pkg_web = json.loads((FIXTURE_ROOT / "apps/web/package.json").read_text(encoding="utf-8"))
        assert pkg_api["dependencies"]["@fx-mono/shared"] == "workspace:*"
        assert pkg_web["dependencies"]["@fx-mono/shared"] == "workspace:*"

    def test_libs_shared_has_conditional_exports(self) -> None:
        shared = json.loads((FIXTURE_ROOT / "libs/shared/package.json").read_text(encoding="utf-8"))
        exports = shared["exports"]
        # La entrada '.' debe tener types, import, require distintos
        root = exports["."]
        assert "types" in root
        assert "import" in root
        assert "require" in root
        # Los sub-paths "./types" y "./utils" deben tener entradas separadas
        assert "./types" in exports
        assert "./utils" in exports

    def test_web_uses_workspace_path_alias(self) -> None:
        ts = json.loads((FIXTURE_ROOT / "apps/web/tsconfig.app.json").read_text(encoding="utf-8"))
        assert ts["compilerOptions"]["paths"]["@fx-mono/shared"]

    def test_web_has_angular_json(self) -> None:
        aj = json.loads((FIXTURE_ROOT / "apps/web/angular.json").read_text(encoding="utf-8"))
        assert "fx-mono-web" in aj["projects"]
        # Trampa #5: fileReplacements en development y production
        dev_cfg = aj["projects"]["fx-mono-web"]["architect"]["build"]["configurations"]["development"]
        prod_cfg = aj["projects"]["fx-mono-web"]["architect"]["build"]["configurations"]["production"]
        assert dev_cfg["fileReplacements"]
        assert prod_cfg["fileReplacements"]

    def test_web_has_proxy_conf(self) -> None:
        proxy = json.loads((FIXTURE_ROOT / "apps/web/proxy.conf.json").read_text(encoding="utf-8"))
        assert "/api" in proxy
        assert proxy["/api"]["target"].startswith("http")

    def test_environments_files_exist(self) -> None:
        env_dir = FIXTURE_ROOT / "apps/web/src/environments"
        assert (env_dir / "environment.ts").is_file()
        assert (env_dir / "environment.development.ts").is_file()
        assert (env_dir / "environment.production.ts").is_file()
        # development tiene production: false, production tiene production: true
        dev = (env_dir / "environment.development.ts").read_text(encoding="utf-8")
        prod = (env_dir / "environment.production.ts").read_text(encoding="utf-8")
        assert "production: false" in dev
        assert "production: true" in prod

    def test_routes_use_loadComponent(self) -> None:
        routes = (FIXTURE_ROOT / "apps/web/src/app/app.routes.ts").read_text(encoding="utf-8")
        assert "loadComponent" in routes
        assert "canActivate" in routes

    def test_provideHttpClient_withInterceptors(self) -> None:
        cfg = (FIXTURE_ROOT / "apps/web/src/app/app.config.ts").read_text(encoding="utf-8")
        assert "withInterceptors" in cfg

    def test_functional_guards_and_interceptors(self) -> None:
        guard = (FIXTURE_ROOT / "apps/web/src/app/core/auth.guard.ts").read_text(encoding="utf-8")
        inter = (FIXTURE_ROOT / "apps/web/src/app/core/auth.interceptor.ts").read_text(encoding="utf-8")
        assert "CanActivateFn" in guard
        assert "HttpInterceptorFn" in inter


class TestUniqueTokensFile:
    def test_at_least_20_tokens(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20

    def test_tokens_not_in_src(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXMONO-")
        # Buscar tokens en apps/*/src, libs/*/src, tests.
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(FIXTURE_ROOT).as_posix()
            if "unique_tokens" in rel:
                continue
            if path.suffix not in (".ts", ".tsx", ".json", ".md", ".kts", ".html", ".css", ".yml", ".yaml"):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            for tok in tokens:
                assert tok not in text, f"token {tok} found in {rel}"


class TestPackagesHaveTests:
    def test_libs_shared_has_tests(self) -> None:
        assert (FIXTURE_ROOT / "libs/shared/tests").is_dir()
        files = list((FIXTURE_ROOT / "libs/shared/tests").glob("*.test.ts"))
        assert len(files) >= 2

    def test_apps_api_has_tests(self) -> None:
        assert (FIXTURE_ROOT / "apps/api/tests").is_dir()
        files = list((FIXTURE_ROOT / "apps/api/tests").glob("*.test.ts"))
        assert len(files) >= 3

    def test_apps_web_has_tests(self) -> None:
        assert (FIXTURE_ROOT / "apps/web/tests").is_dir()
        files = list((FIXTURE_ROOT / "apps/web/tests").glob("*.test.ts"))
        assert len(files) >= 1
