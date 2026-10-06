"""Tests del ground truth de fx-sveltekit (F06k)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-sveltekit"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-sveltekit"


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
        assert "tareas" in names
        assert "etiquetas" in names
        assert "compartir" in names

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
        assert "@sveltejs/kit" in names
        assert "svelte" in names
        assert "zod" in names

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
            assert tok.startswith("NPRGT-FXSVELTE-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"node_modules", ".svelte-kit", ".output", "dist", "coverage", ".git"}
        skip_files = {"unique_tokens.txt", "package-lock.json"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".svelte", ".ts", ".js", ".mjs", ".cjs",
                                    ".scss", ".css", ".json", ".yml", ".yaml", ".md", ".txt",
                                    ".sh"):
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


class TestSveltekitStructure:
    def test_svelte_config(self) -> None:
        assert (FIXTURE_ROOT / "svelte.config.js").is_file()

    def test_vite_config(self) -> None:
        assert (FIXTURE_ROOT / "vite.config.ts").is_file()

    def test_app_html(self) -> None:
        assert (FIXTURE_ROOT / "src/app.html").is_file()

    def test_app_d_ts(self) -> None:
        assert (FIXTURE_ROOT / "src/app.d.ts").is_file()

    def test_hooks_server(self) -> None:
        assert (FIXTURE_ROOT / "src/hooks.server.ts").is_file()

    def test_layout_svelte(self) -> None:
        assert (FIXTURE_ROOT / "src/routes/+layout.svelte").is_file()

    def test_layout_server_ts(self) -> None:
        assert (FIXTURE_ROOT / "src/routes/+layout.server.ts").is_file()

    def test_page_svelte(self) -> None:
        assert (FIXTURE_ROOT / "src/routes/+page.svelte").is_file()

    def test_server_db(self) -> None:
        assert (FIXTURE_ROOT / "src/lib/server/db.ts").is_file()

    def test_server_auth(self) -> None:
        assert (FIXTURE_ROOT / "src/lib/server/auth.ts").is_file()

    def test_stores(self) -> None:
        for s in ("tasks.svelte.ts", "tags.svelte.ts", "share.svelte.ts"):
            assert (FIXTURE_ROOT / f"src/lib/stores/{s}").is_file(), f"missing {s}"

    def test_components(self) -> None:
        for c in ("TaskCard", "TaskForm", "TagPicker", "ShareButton", "HiddenPremium"):
            assert (FIXTURE_ROOT / f"src/lib/components/{c}.svelte").is_file(), f"missing {c}.svelte"

    def test_routes(self) -> None:
        for p in ("tareas/+page.svelte", "tareas/+page.server.ts",
                  "tareas/[id]/+page.svelte", "tareas/[id]/+page.server.ts",
                  "etiquetas/+page.svelte", "etiquetas/+page.server.ts",
                  "compartir/+page.svelte", "compartir/+page.server.ts"):
            assert (FIXTURE_ROOT / f"src/routes/{p}").is_file(), f"missing {p}"

    def test_styles(self) -> None:
        assert (FIXTURE_ROOT / "src/styles/main.scss").is_file()
        assert (FIXTURE_ROOT / "src/styles/_hidden.scss").is_file()

    def test_utils(self) -> None:
        assert (FIXTURE_ROOT / "src/lib/utils/formatDate.ts").is_file()
        assert (FIXTURE_ROOT / "src/lib/utils/slugify.ts").is_file()


class TestSveltekitSource:
    def test_svelte_uses_adapter_node(self) -> None:
        cfg = (FIXTURE_ROOT / "svelte.config.js").read_text(encoding="utf-8")
        assert "adapter-node" in cfg

    def test_hooks_declares_handle(self) -> None:
        src = (FIXTURE_ROOT / "src/hooks.server.ts").read_text(encoding="utf-8")
        assert "export const handle" in src
        assert "x-fx-auth" in src

    def test_layout_server_load_returns_user(self) -> None:
        src = (FIXTURE_ROOT / "src/routes/+layout.server.ts").read_text(encoding="utf-8")
        assert "LayoutServerLoad" in src
        assert "user" in src

    def test_tareas_actions(self) -> None:
        src = (FIXTURE_ROOT / "src/routes/tareas/+page.server.ts").read_text(encoding="utf-8")
        assert "actions" in src
        assert "create:" in src
        assert "delete:" in src

    def test_tareas_uses_zod(self) -> None:
        src = (FIXTURE_ROOT / "src/routes/tareas/+page.server.ts").read_text(encoding="utf-8")
        assert "z.object" in src or "z.string" in src

    def test_task_form_uses_enhance(self) -> None:
        src = (FIXTURE_ROOT / "src/lib/components/TaskForm.svelte").read_text(encoding="utf-8")
        assert "use:enhance" in src
        assert "import { enhance }" in src or "from '$app/forms'" in src

    def test_tag_picker_uses_runes(self) -> None:
        src = (FIXTURE_ROOT / "src/lib/components/TagPicker.svelte").read_text(encoding="utf-8")
        assert "$state" in src
        assert "$derived" in src
        assert "$effect" in src

    def test_share_store_cross_call(self) -> None:
        src = (FIXTURE_ROOT / "src/lib/stores/share.svelte.ts").read_text(encoding="utf-8")
        assert "createTasksStore" in src
        assert "tasks.remove" in src

    def test_compartir_action_uses_zod(self) -> None:
        src = (FIXTURE_ROOT / "src/routes/compartir/+page.server.ts").read_text(encoding="utf-8")
        assert "z.string" in src
        assert "email" in src


class TestTrapsEcosystem:
    def test_e01_file_conventions(self) -> None:
        import os
        routes = FIXTURE_ROOT / "src/routes"
        files = os.listdir(routes)
        assert "+layout.svelte" in files
        assert "+layout.server.ts" in files
        assert "+page.svelte" in files

    def test_e02_layout_server_load(self) -> None:
        import re
        src = (FIXTURE_ROOT / "src/routes/+layout.server.ts").read_text(encoding="utf-8")
        assert re.search(r"load\s*:\s*LayoutServerLoad", src)

    def test_e03_form_actions_and_enhance(self) -> None:
        server = (FIXTURE_ROOT / "src/routes/tareas/+page.server.ts").read_text(encoding="utf-8")
        form = (FIXTURE_ROOT / "src/lib/components/TaskForm.svelte").read_text(encoding="utf-8")
        assert "actions" in server
        assert "create:" in server
        assert "use:enhance" in form

    def test_e04_handle_in_hooks(self) -> None:
        src = (FIXTURE_ROOT / "src/hooks.server.ts").read_text(encoding="utf-8")
        assert "export const handle" in src

    def test_e05_runes(self) -> None:
        tag = (FIXTURE_ROOT / "src/lib/components/TagPicker.svelte").read_text(encoding="utf-8")
        assert "$state" in tag and "$derived" in tag and "$effect" in tag

    def test_e06_lib_alias(self) -> None:
        for path in ["src/lib/stores/tasks.svelte.ts", "src/lib/components/TaskCard.svelte",
                     "src/routes/tareas/+page.server.ts"]:
            src = (FIXTURE_ROOT / path).read_text(encoding="utf-8")
            assert "$lib" in src


class TestTrapsPackage:
    def test_p01_formatdate_unused(self) -> None:
        import os
        for path in (FIXTURE_ROOT / "src/routes").rglob("*.svelte"):
            t = path.read_text(encoding="utf-8", errors="replace")
            assert "formatDate" not in t
        for path in (FIXTURE_ROOT / "src/lib/components").rglob("*.svelte"):
            t = path.read_text(encoding="utf-8", errors="replace")
            assert "formatDate" not in t

    def test_p02_cross_store_wrong_semantic(self) -> None:
        src = (FIXTURE_ROOT / "src/lib/stores/share.svelte.ts").read_text(encoding="utf-8")
        assert "createTasksStore" in src
        assert "tasks.remove" in src

    def test_p03_handle_no_auth_check(self) -> None:
        src = (FIXTURE_ROOT / "src/hooks.server.ts").read_text(encoding="utf-8")
        assert "locals.user" in src
        assert "return new Response(" not in src

    def test_p04_effect_memory_leak(self) -> None:
        src = (FIXTURE_ROOT / "src/lib/components/TagPicker.svelte").read_text(encoding="utf-8")
        assert "$effect" in src
        assert "setInterval" in src
        assert "clearInterval" in src

    def test_p05_action_not_found_silent(self) -> None:
        src = (FIXTURE_ROOT / "src/routes/tareas/+page.server.ts").read_text(encoding="utf-8")
        # El bloque actions solo contiene create y delete, no foo.
        import re
        m = re.search(r"actions\s*:\s*Actions\s*=\s*\{([\s\S]*?)\n\s*\}\s*;", src)
        assert m is not None
        body = m.group(1)
        assert "?" not in body

    def test_p06_load_with_side_effect(self) -> None:
        src = (FIXTURE_ROOT / "src/routes/+layout.server.ts").read_text(encoding="utf-8")
        assert "seedTareasExtra" in src


class TestTrapsSuperficial:
    def test_s01_formatdate_exists(self) -> None:
        f = FIXTURE_ROOT / "src/lib/utils/formatDate.ts"
        assert f.is_file()
        src = f.read_text(encoding="utf-8")
        assert "function formatDate" in src

    def test_s02_seed_extra_exists_no_app_use(self) -> None:
        db = (FIXTURE_ROOT / "src/lib/server/db.ts").read_text(encoding="utf-8")
        assert "export function seedTareasExtra" in db

    def test_s03_hidden_premium_explicit_import(self) -> None:
        src = (FIXTURE_ROOT / "src/routes/+page.svelte").read_text(encoding="utf-8")
        assert "import HiddenPremium" in src
        assert "$lib/components/HiddenPremium.svelte" in src


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-sveltekit" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_package_json_has_svelte(self) -> None:
        pkg = json.loads((FIXTURE_ROOT / "package.json").read_text(encoding="utf-8"))
        assert "svelte" in pkg.get("dependencies", {})

    def test_package_json_has_vitest(self) -> None:
        pkg = json.loads((FIXTURE_ROOT / "package.json").read_text(encoding="utf-8"))
        assert "vitest" in pkg.get("devDependencies", {})

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20
        for tok in tokens:
            assert tok.startswith("NPRGT-FXSVELTE-")
