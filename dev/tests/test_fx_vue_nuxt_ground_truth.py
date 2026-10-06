"""Tests del ground truth de fx-vue-nuxt (F06j)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-vue-nuxt"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-vue-nuxt"


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
        assert "reservas" in names
        assert "perfil" in names
        assert "notificaciones" in names

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
        assert "nuxt" in names
        assert "vue" in names
        assert "pinia" in names
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
            assert tok.startswith("NPRGT-FXVUE-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"node_modules", "dist", "coverage", ".git", ".nuxt", ".output"}
        skip_files = {"unique_tokens.txt", "package-lock.json"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".ts", ".vue", ".js", ".mjs", ".cjs",
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


class TestNuxtStructure:
    def test_nuxt_config(self) -> None:
        assert (FIXTURE_ROOT / "nuxt.config.ts").is_file()

    def test_app_vue(self) -> None:
        assert (FIXTURE_ROOT / "app.vue").is_file()

    def test_pages_index(self) -> None:
        assert (FIXTURE_ROOT / "pages/index.vue").is_file()

    def test_pages_reservas_index(self) -> None:
        assert (FIXTURE_ROOT / "pages/reservas/index.vue").is_file()

    def test_pages_reservas_id(self) -> None:
        assert (FIXTURE_ROOT / "pages/reservas/[id].vue").is_file()

    def test_pages_perfil_index(self) -> None:
        assert (FIXTURE_ROOT / "pages/perfil/index.vue").is_file()

    def test_pages_notificaciones_index(self) -> None:
        assert (FIXTURE_ROOT / "pages/notificaciones/index.vue").is_file()

    def test_components(self) -> None:
        for c in ("ReservaCard", "ReservaForm", "PerfilEditor", "NotificacionItem", "HiddenPremium"):
            assert (FIXTURE_ROOT / f"components/{c}.vue").is_file(), f"missing {c}.vue"

    def test_composables(self) -> None:
        for c in ("useReservas", "useProfile", "useDateFmt", "useSession"):
            assert (FIXTURE_ROOT / f"composables/{c}.ts").is_file(), f"missing {c}.ts"

    def test_stores(self) -> None:
        for s in ("reservations", "profile", "notifications"):
            assert (FIXTURE_ROOT / f"stores/{s}.ts").is_file(), f"missing {s}.ts"

    def test_plugins(self) -> None:
        assert (FIXTURE_ROOT / "plugins/0.api-base.ts").is_file()
        assert (FIXTURE_ROOT / "plugins/1.i18n.ts").is_file()

    def test_middleware(self) -> None:
        assert (FIXTURE_ROOT / "middleware/auth.global.ts").is_file()
        assert (FIXTURE_ROOT / "middleware/reservas-only.ts").is_file()

    def test_server_api(self) -> None:
        for p in ("reservas.get.ts", "reservas.post.ts",
                  "reservas/[id].delete.ts", "profile.get.ts",
                  "profile.patch.ts", "notifications.get.ts"):
            assert (FIXTURE_ROOT / f"server/api/{p}").is_file(), f"missing server/api/{p}"

    def test_server_utils(self) -> None:
        assert (FIXTURE_ROOT / "server/utils/db.ts").is_file()

    def test_types(self) -> None:
        assert (FIXTURE_ROOT / "types/index.ts").is_file()

    def test_assets_css(self) -> None:
        assert (FIXTURE_ROOT / "assets/css/main.scss").is_file()
        assert (FIXTURE_ROOT / "assets/css/_hidden.scss").is_file()


class TestNuxtSource:
    def test_nuxt_uses_pinia(self) -> None:
        cfg = (FIXTURE_ROOT / "nuxt.config.ts").read_text(encoding="utf-8")
        assert "@pinia/nuxt" in cfg

    def test_nuxt_uses_payload_extraction_false(self) -> None:
        cfg = (FIXTURE_ROOT / "nuxt.config.ts").read_text(encoding="utf-8")
        assert "payloadExtraction" in cfg
        assert "false" in cfg

    def test_reservas_index_no_imports(self) -> None:
        src = (FIXTURE_ROOT / "pages/reservas/index.vue").read_text(encoding="utf-8")
        bloque = src[src.index("<script"):src.index("</script>")]
        # No debe haber lineas que empiecen por `import`.
        lines = [l for l in bloque.split("\n") if l.strip()]
        assert not any(l.lstrip().startswith("import ") for l in lines), \
            "pages/reservas/index.vue no debe contener imports (auto-imports)"

    def test_reservas_index_uses_define_page_meta(self) -> None:
        src = (FIXTURE_ROOT / "pages/reservas/index.vue").read_text(encoding="utf-8")
        assert "definePageMeta" in src
        assert "middleware:" in src

    def test_perfil_index_uses_define_page_meta(self) -> None:
        src = (FIXTURE_ROOT / "pages/perfil/index.vue").read_text(encoding="utf-8")
        assert "definePageMeta" in src

    def test_reserva_form_uses_define_model(self) -> None:
        src = (FIXTURE_ROOT / "components/ReservaForm.vue").read_text(encoding="utf-8")
        assert "defineModel" in src
        assert "defineEmits" in src
        assert "preventDefault" in src

    def test_notifications_uses_other_store(self) -> None:
        src = (FIXTURE_ROOT / "stores/notifications.ts").read_text(encoding="utf-8")
        assert "useReservationsStore" in src
        assert ".cancelar(" in src

    def test_api_plugin_provides(self) -> None:
        src = (FIXTURE_ROOT / "plugins/0.api-base.ts").read_text(encoding="utf-8")
        assert "provide:" in src
        assert "api" in src

    def test_i18n_plugin_fallback(self) -> None:
        src = (FIXTURE_ROOT / "plugins/1.i18n.ts").read_text(encoding="utf-8")
        assert "provide:" in src
        assert "t" in src
        # Fallback: devuelve string vacio sin warn.
        assert "return ''" in src

    def test_auth_global_middleware(self) -> None:
        src = (FIXTURE_ROOT / "middleware/auth.global.ts").read_text(encoding="utf-8")
        assert "navigateTo('/login')" in src
        # No debe inspeccionar la ruta destino.
        assert "to.path" not in src

    def test_reservas_only_middleware(self) -> None:
        src = (FIXTURE_ROOT / "middleware/reservas-only.ts").read_text(encoding="utf-8")
        assert "useProfileStore" in src
        assert "navigateTo('/')" in src

    def test_server_post_uses_zod(self) -> None:
        src = (FIXTURE_ROOT / "server/api/reservas.post.ts").read_text(encoding="utf-8")
        assert "z.object" in src
        assert "safeParse" in src

    def test_server_delete_no_owner_check(self) -> None:
        src = (FIXTURE_ROOT / "server/api/reservas/[id].delete.ts").read_text(encoding="utf-8")
        assert "removeReserva" in src
        # No valida que el caller sea dueno.
        assert "owner" not in src
        assert "usuarioId" not in src


class TestTrapsEcosystem:
    def test_e01_no_imports(self) -> None:
        src = (FIXTURE_ROOT / "pages/reservas/index.vue").read_text(encoding="utf-8")
        bloque = src[src.index("<script"):src.index("</script>")]
        assert not re.search(r"^import\s+", bloque, re.MULTILINE)

    def test_e02_define_page_meta(self) -> None:
        for path in ["pages/reservas/index.vue", "pages/perfil/index.vue"]:
            src = (FIXTURE_ROOT / path).read_text(encoding="utf-8")
            assert "definePageMeta" in src

    def test_e03_provide(self) -> None:
        for path in ["plugins/0.api-base.ts", "plugins/1.i18n.ts"]:
            src = (FIXTURE_ROOT / path).read_text(encoding="utf-8")
            assert "provide:" in src

    def test_e04_server_api_by_name(self) -> None:
        api_dir = FIXTURE_ROOT / "server/api"
        # Buscamos en todo el arbol porque rglob no devuelve los paths
        # con [] correctamente.
        files = list(api_dir.rglob("*.ts"))
        names = {f.relative_to(api_dir).as_posix() for f in files}
        assert "reservas.get.ts" in names
        assert "reservas.post.ts" in names
        assert "reservas/[id].delete.ts" in names

    def test_e05_define_model_emits(self) -> None:
        src = (FIXTURE_ROOT / "components/ReservaForm.vue").read_text(encoding="utf-8")
        assert "defineModel" in src
        assert "defineEmits" in src
        assert "ev.preventDefault" in src or "preventDefault()" in src

    def test_e06_cross_store(self) -> None:
        src = (FIXTURE_ROOT / "stores/notifications.ts").read_text(encoding="utf-8")
        assert "useReservationsStore" in src
        assert re.search(r"\.cancelar\(", src)


class TestTrapsPackage:
    def test_p01_datefmt_unused(self) -> None:
        f = FIXTURE_ROOT / "composables/useDateFmt.ts"
        assert f.is_file()
        src = f.read_text(encoding="utf-8")
        assert "formatDate" in src
        # Comprobamos que no se invoca en pages/ ni components/.
        used = False
        for sub in ("pages", "components"):
            for path in (FIXTURE_ROOT / sub).rglob("*.vue"):
                if "useDateFmt" in path.read_text(encoding="utf-8", errors="replace"):
                    used = True
        assert not used

    def test_p02_i18n_silent_fallback(self) -> None:
        src = (FIXTURE_ROOT / "plugins/1.i18n.ts").read_text(encoding="utf-8")
        assert "return ''" in src
        assert "console.warn" not in src

    def test_p03_cancelar_no_owner(self) -> None:
        src = (FIXTURE_ROOT / "stores/reservations.ts").read_text(encoding="utf-8")
        # El cuerpo de la accion cancelar no debe incluir owner/permisos.
        m = re.search(r"async cancelar\(.*?\n\s*\}\s*\n", src, re.DOTALL)
        if m:
            body = m.group(0)
            assert "owner" not in body
            assert "permisos" not in body

    def test_p04_no_retry(self) -> None:
        src = (FIXTURE_ROOT / "composables/useReservas.ts").read_text(encoding="utf-8")
        assert "$fetch" in src
        assert "retry" not in src
        assert "timeout" not in src

    def test_p05_vmodel_string(self) -> None:
        form = (FIXTURE_ROOT / "components/ReservaForm.vue").read_text(encoding="utf-8")
        post = (FIXTURE_ROOT / "server/api/reservas.post.ts").read_text(encoding="utf-8")
        assert re.search(r"defineModel<string>\s*\(\s*['\"]fecha['\"]", form)
        assert "Date.parse" in post

    def test_p06_auth_loop(self) -> None:
        src = (FIXTURE_ROOT / "middleware/auth.global.ts").read_text(encoding="utf-8")
        assert "navigateTo('/login')" in src
        # No debe inspeccionar la ruta destino (eso lo haria no redirect cuando to.path=='/login').
        assert "to.path" not in src


class TestTrapsSuperficial:
    def test_s01_datefmt_exists(self) -> None:
        f = FIXTURE_ROOT / "composables/useDateFmt.ts"
        assert f.is_file()

    def test_s02_seed_extra_exists_no_app_use(self) -> None:
        db = (FIXTURE_ROOT / "server/utils/db.ts").read_text(encoding="utf-8")
        assert "export function seedExtra" in db
        # No se invoca en pages/, components/, stores/, etc.
        called = False
        skip_dirs = {"node_modules", ".nuxt", ".output", "dist"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.suffix not in (".ts", ".vue", ".js", ".mjs", ".cjs"):
                continue
            if path.name == "db.ts":
                continue
            t = path.read_text(encoding="utf-8", errors="replace")
            if re.search(r"seedExtra\s*\(", t):
                called = True
                break
        assert not called

    def test_s03_hidden_premium_explicit_import(self) -> None:
        src = (FIXTURE_ROOT / "pages/index.vue").read_text(encoding="utf-8")
        assert "import HiddenPremium" in src
        assert "~/components/HiddenPremium.vue" in src


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-vue-nuxt" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_package_json_has_nuxt(self) -> None:
        pkg = json.loads((FIXTURE_ROOT / "package.json").read_text(encoding="utf-8"))
        assert "nuxt" in pkg.get("dependencies", {}) or "nuxt" in pkg.get("devDependencies", {})

    def test_package_json_has_vitest(self) -> None:
        pkg = json.loads((FIXTURE_ROOT / "package.json").read_text(encoding="utf-8"))
        assert "vitest" in pkg.get("devDependencies", {})

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20
        for tok in tokens:
            assert tok.startswith("NPRGT-FXVUE-")
