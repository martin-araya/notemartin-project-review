"""Tests del ground truth de fx-nextjs-fullstack (F06h)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-nextjs-fullstack"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-nextjs-fullstack"


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
        assert "registro" in names
        assert "publicar-articulo" in names
        assert "comentarios" in names
        assert "panel-admin" in names

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
                assert o.get("user_sees"), f"{f['id']}/{o['id']} missing user_sees"


class TestUniqueTokensFile:
    def test_at_least_20_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXNEXT-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(FIXTURE_ROOT).as_posix()
            if "unique_tokens" in rel:
                continue
            if path.suffix not in (".ts", ".tsx", ".js", ".jsx", ".json",
                                    ".md", ".yml", ".yaml", ".html", ".css", ".txt", ".prisma"):
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


class TestNextStructure:
    def test_app_layout_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/layout.tsx").is_file()

    def test_app_home_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/page.tsx").is_file()

    def test_middleware_in_root(self) -> None:
        assert (FIXTURE_ROOT / "middleware.ts").is_file()
        assert not (FIXTURE_ROOT / "app/middleware.ts").exists()

    def test_prisma_schema_exists(self) -> None:
        assert (FIXTURE_ROOT / "prisma/schema.prisma").is_file()

    def test_route_groups_marketing(self) -> None:
        assert (FIXTURE_ROOT / "app/(marketing)").is_dir()

    def test_dynamic_segment_slug(self) -> None:
        assert (FIXTURE_ROOT / "app/(marketing)/articulos/[slug]/page.tsx").is_file()

    def test_parallel_route_modal(self) -> None:
        assert (FIXTURE_ROOT / "app/@modal/default.tsx").is_file()
        assert (FIXTURE_ROOT / "app/@modal/(.)comentarios").is_dir()

    def test_route_handlers(self) -> None:
        assert (FIXTURE_ROOT / "app/api/comentarios/route.ts").is_file()
        assert (FIXTURE_ROOT / "app/api/health/route.ts").is_file()

    def test_panel_admin_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/panel-admin/page.tsx").is_file()


class TestEcosystemTraps:
    def test_use_client_directive_count(self) -> None:
        def has_use_client(path: Path) -> bool:
            try:
                lines = path.read_text(encoding="utf-8").splitlines()[:10]
            except Exception:
                return False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(("'", '"')) and "use client" in stripped:
                    return True
            return False

        use_client_files = list((FIXTURE_ROOT / "app").rglob("*.tsx"))
        count = sum(1 for f in use_client_files if has_use_client(f))
        assert count >= 4, f"solo {count} archivos con 'use client'"

    def test_use_server_directive_count(self) -> None:
        def has_use_server(path: Path) -> bool:
            try:
                lines = path.read_text(encoding="utf-8").splitlines()[:10]
            except Exception:
                return False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(("'", '"')) and "use server" in stripped:
                    return True
            return False

        actions = (FIXTURE_ROOT / "app/actions").glob("*.ts")
        count = sum(1 for f in actions if has_use_server(f))
        assert count >= 3, f"solo {count} archivos con 'use server'"

    def test_middleware_redirects_panel(self) -> None:
        src = (FIXTURE_ROOT / "middleware.ts").read_text(encoding="utf-8")
        assert "pathname.startsWith(\"/panel-admin\")" in src
        assert "NextResponse.redirect" in src

    def test_revalidate_tag_used(self) -> None:
        auth = (FIXTURE_ROOT / "app/actions/articles.ts").read_text(encoding="utf-8")
        assert "revalidateTag(" in auth
        comments = (FIXTURE_ROOT / "app/actions/comments.ts").read_text(encoding="utf-8")
        assert "revalidateTag(" in comments

    def test_revalidate_isr(self) -> None:
        page = (FIXTURE_ROOT / "app/(marketing)/articulos/[slug]/page.tsx").read_text(encoding="utf-8")
        assert "export const revalidate" in page

    def test_prisma_relations(self) -> None:
        schema = (FIXTURE_ROOT / "prisma/schema.prisma").read_text(encoding="utf-8")
        assert "@relation" in schema
        assert "onDelete: Cascade" in schema


class TestUnitTestFiles:
    def test_actions_auth(self) -> None:
        assert (FIXTURE_ROOT / "tests/unit/actions_auth.test.ts").is_file()

    def test_actions_articles(self) -> None:
        assert (FIXTURE_ROOT / "tests/unit/actions_articles.test.ts").is_file()

    def test_middleware_test(self) -> None:
        assert (FIXTURE_ROOT / "tests/unit/middleware.test.ts").is_file()

    def test_tags_test(self) -> None:
        assert (FIXTURE_ROOT / "tests/unit/tags.test.ts").is_file()

    def test_traps_test(self) -> None:
        assert (FIXTURE_ROOT / "tests/unit/traps.test.ts").is_file()

    def test_setup(self) -> None:
        assert (FIXTURE_ROOT / "tests/setup.ts").is_file()

    def test_at_least_5_unit_test_files(self) -> None:
        files = (
            list((FIXTURE_ROOT / "tests/unit").glob("*.test.ts"))
            + list((FIXTURE_ROOT / "tests/unit").glob("*.test.tsx"))
        )
        assert len(files) >= 5, f"only {len(files)} unit test files"

    def test_at_least_3_e2e_spec_files(self) -> None:
        files = list((FIXTURE_ROOT / "tests/e2e").glob("*.spec.ts"))
        assert len(files) >= 3, f"only {len(files)} e2e spec files"


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-nextjs-fullstack" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_playwright_config(self) -> None:
        assert (FIXTURE_ROOT / "playwright.config.ts").is_file()