"""Tests del ground truth de fx-react-spa (F06g)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-react-spa"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-react-spa"


def _load_gt() -> dict:
    return json.loads((GT_DIR / "ground_truth.json").read_text(encoding="utf-8"))


class TestGroundTruthShape:
    def test_file_exists(self) -> None:
        assert (GT_DIR / "ground_truth.json").is_file()

    def test_has_4_features(self) -> None:
        gt = _load_gt()
        assert len(gt["features"]) == 4

    def test_features_match_spec(self) -> None:
        gt = _load_gt()
        names = {f["name"] for f in gt["features"]}
        assert "autenticacion" in names
        assert "catalogo-y-carrito" in names
        assert "checkout" in names
        assert "panel-de-pedidos" in names

    def test_each_feature_has_min_6_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n >= 6, f"{f['id']}: only {n} outcomes"

    def test_has_6_ecosystem_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["traps"]) == 6

    def test_has_6_package_traps(self) -> None:
        gt = _load_gt()
        assert len(gt["package_traps"]) == 6

    def test_each_trap_has_resolution(self) -> None:
        gt = _load_gt()
        for t in gt["traps"] + gt["package_traps"]:
            assert t.get("resolution"), f"trap {t.get('id')} missing resolution"

    def test_outcome_user_sees_present(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            for o in f.get("outcomes", []):
                assert o.get("user_sees"), (
                    f"{f['id']}/{o['id']} missing user_sees"
                )


class TestUniqueTokensFile:
    def test_at_least_20_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXREACT-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(FIXTURE_ROOT).as_posix()
            if "unique_tokens" in rel:
                continue
            if path.suffix not in (".ts", ".tsx", ".js", ".jsx", ".json",
                                    ".md", ".yml", ".yaml", ".html", ".css", ".txt"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
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


class TestReactStructure:
    def test_index_html_exists(self) -> None:
        assert (FIXTURE_ROOT / "index.html").is_file()

    def test_main_tsx_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/main.tsx").is_file()

    def test_router_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/routes/router.tsx").is_file()

    def test_base_api_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/api/baseApi.ts").is_file()

    def test_store_files(self) -> None:
        assert (FIXTURE_ROOT / "src/store/index.ts").is_file()
        assert (FIXTURE_ROOT / "src/store/slices/auth.slice.ts").is_file()
        assert (FIXTURE_ROOT / "src/store/slices/cart.slice.ts").is_file()

    def test_features_dirs(self) -> None:
        for f in ("auth", "catalog", "cart", "checkout", "orders"):
            assert (FIXTURE_ROOT / f"src/features/{f}").is_dir()

    def test_main_has_5_plus_providers(self) -> None:
        src = (FIXTURE_ROOT / "src/main.tsx").read_text(encoding="utf-8")
        for p in ("StoreProvider", "QueryClientProvider", "I18nextProvider",
                  "ThemeProvider", "ToastProvider", "ErrorBoundary"):
            assert p in src, f"main.tsx missing {p}"

    def test_main_uses_suspense(self) -> None:
        src = (FIXTURE_ROOT / "src/main.tsx").read_text(encoding="utf-8")
        assert "Suspense" in src

    def test_env_uses_import_meta_env(self) -> None:
        src = (FIXTURE_ROOT / "src/lib/env.ts").read_text(encoding="utf-8")
        assert "import.meta.env.VITE_API_URL" in src
        assert "import.meta.env.VITE_DEFAULT_LOCALE" in src

    def test_base_api_create_api(self) -> None:
        src = (FIXTURE_ROOT / "src/api/baseApi.ts").read_text(encoding="utf-8")
        assert "createApi" in src
        for ep in ("login:", "register:", "getProducts:", "getProduct:", "getOrders:"):
            assert ep in src, f"baseApi.ts missing endpoint {ep}"

    def test_loader_in_separate_file(self) -> None:
        assert (FIXTURE_ROOT / "src/features/catalog/productsLoader.ts").is_file()

    def test_action_in_separate_file(self) -> None:
        assert (FIXTURE_ROOT / "src/features/checkout/checkoutAction.ts").is_file()

    def test_polling_in_orders_hooks(self) -> None:
        src = (FIXTURE_ROOT / "src/features/orders/orders.hooks.ts").read_text(encoding="utf-8")
        assert "pollingInterval: 1000" in src

    def test_useEffect_chain_in_catalog_hooks(self) -> None:
        src = (FIXTURE_ROOT / "src/features/catalog/catalog.hooks.ts").read_text(encoding="utf-8")
        assert src.count("useEffect(") >= 2

    def test_button_uses_forwardRef_and_memo(self) -> None:
        src = (FIXTURE_ROOT / "src/components/Button.tsx").read_text(encoding="utf-8")
        assert "forwardRef" in src
        assert "memo" in src

    def test_cart_item_uses_forwardRef_memo_and_hoc(self) -> None:
        src = (FIXTURE_ROOT / "src/features/cart/CartItem.tsx").read_text(encoding="utf-8")
        assert "forwardRef" in src
        assert "memo" in src
        assert "withLogger" in src
        assert "CartLineItem" in src  # displayName falso


class TestBatsFilesExist:
    def test_setup(self) -> None:
        assert (FIXTURE_ROOT / "tests/setup.ts").is_file()

    def test_handlers(self) -> None:
        assert (FIXTURE_ROOT / "tests/handlers.ts").is_file()

    def test_auth_tests(self) -> None:
        assert (FIXTURE_ROOT / "tests/auth.test.tsx").is_file()

    def test_catalog_tests(self) -> None:
        assert (FIXTURE_ROOT / "tests/catalog.test.tsx").is_file()

    def test_cart_tests(self) -> None:
        assert (FIXTURE_ROOT / "tests/cart.test.tsx").is_file()

    def test_checkout_tests(self) -> None:
        assert (FIXTURE_ROOT / "tests/checkout.test.tsx").is_file()

    def test_orders_tests(self) -> None:
        assert (FIXTURE_ROOT / "tests/orders.test.tsx").is_file()

    def test_routing_tests(self) -> None:
        assert (FIXTURE_ROOT / "tests/routing.test.tsx").is_file()

    def test_env_tests(self) -> None:
        assert (FIXTURE_ROOT / "tests/env.test.tsx").is_file()

    def test_providers_tests(self) -> None:
        assert (FIXTURE_ROOT / "tests/providers.test.tsx").is_file()

    def test_traps_ecosystem_tests(self) -> None:
        assert (FIXTURE_ROOT / "tests/traps_ecosystem.test.tsx").is_file()

    def test_at_least_9_test_files(self) -> None:
        files = (
            list((FIXTURE_ROOT / "tests").glob("*.test.ts"))
            + list((FIXTURE_ROOT / "tests").glob("*.test.tsx"))
        )
        assert len(files) >= 9, f"only {len(files)} test files"


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-react-spa" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()