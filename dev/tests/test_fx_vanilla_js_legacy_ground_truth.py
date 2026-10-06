"""Tests del ground truth de fx-vanilla-js-legacy (F06i)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-vanilla-js-legacy"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-vanilla-js-legacy"


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
        assert "busqueda" in names
        assert "formulario-de-contacto" in names
        assert "galeria" in names

    def test_each_feature_has_min_6_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n >= 6, f"{f['id']}: only {n} outcomes"

    def test_each_feature_has_7_outcomes(self) -> None:
        gt = _load_gt()
        for f in gt["features"]:
            n = len(f.get("outcomes", []))
            assert n == 7, f"{f['id']}: expected 7 outcomes, got {n}"

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
                assert o.get("user_sees"), (
                    f"{f['id']}/{o['id']} missing user_sees"
                )

    def test_dependencies_listed(self) -> None:
        gt = _load_gt()
        names = {d["name"] for d in gt.get("dependencies", [])}
        assert "express" in names
        assert "jquery" in names
        assert "multer" in names
        assert "lodash" in names

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
            assert tok.startswith("NPRGT-FXVANILLA-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        # Escaneamos solo los archivos de codigo (excluyendo node_modules y dist).
        skip_dirs = {"node_modules", "dist", "coverage", ".git"}
        skip_files = {"unique_tokens.txt", "package-lock.json"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".js", ".jsx", ".mjs", ".cjs", ".html",
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


class TestJqueryStructure:
    def test_index_html_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/index.html").is_file()

    def test_search_html_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/search.html").is_file()

    def test_contact_html_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/contact.html").is_file()

    def test_gallery_html_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/gallery.html").is_file()

    def test_jquery_real_file_exists(self) -> None:
        f = FIXTURE_ROOT / "public/js/jquery-3.7.1.min.js"
        assert f.is_file()
        # Tamano minimo razonable para un jQuery minificado.
        assert f.stat().st_size > 50_000

    def test_app_js_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/js/app.js").is_file()

    def test_search_js_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/js/search.js").is_file()

    def test_contact_js_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/js/contact.js").is_file()

    def test_gallery_js_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/js/gallery.js").is_file()

    def test_dispatch_js_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/js/dispatch.js").is_file()

    def test_colorbox_plugin_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/js/plugins/jquery.colorbox.js").is_file()

    def test_debounce_plugin_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/js/plugins/jquery.debounce.js").is_file()

    def test_scss_main_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/scss/main.scss").is_file()

    def test_scss_hidden_exists(self) -> None:
        assert (FIXTURE_ROOT / "public/scss/_hidden.scss").is_file()

    def test_server_index_exists(self) -> None:
        assert (FIXTURE_ROOT / "server/index.js").is_file()

    def test_routes_exist(self) -> None:
        for r in ("search", "contact", "gallery"):
            assert (FIXTURE_ROOT / f"server/routes/{r}.js").is_file(), f"missing routes/{r}.js"

    def test_registry_exists(self) -> None:
        assert (FIXTURE_ROOT / "server/plugins/registry.js").is_file()

    def test_data_files_exist(self) -> None:
        assert (FIXTURE_ROOT / "server/data/items.js").is_file()
        assert (FIXTURE_ROOT / "server/data/gallery.js").is_file()

    def test_lib_files_exist(self) -> None:
        assert (FIXTURE_ROOT / "server/lib/sanitize.js").is_file()
        assert (FIXTURE_ROOT / "server/lib/deadCode.js").is_file()


class TestJquerySource:
    def test_jquery_minified_starts_with_banner(self) -> None:
        text = (FIXTURE_ROOT / "public/js/jquery-3.7.1.min.js").read_text(encoding="utf-8", errors="replace")
        assert text.lstrip().startswith("/*! jQuery")

    def test_app_js_has_whitelist_camelcase(self) -> None:
        src = (FIXTURE_ROOT / "public/js/app.js").read_text(encoding="utf-8")
        assert "'openSearch'" in src
        assert "'loadGallery'" in src
        assert "'submitContact'" in src

    def test_app_js_returns_unknown_action(self) -> None:
        src = (FIXTURE_ROOT / "public/js/app.js").read_text(encoding="utf-8")
        assert "'unknown_action'" in src

    def test_search_js_delegates_to_document(self) -> None:
        src = (FIXTURE_ROOT / "public/js/search.js").read_text(encoding="utf-8")
        assert "$(document).on('submit', '#fx-search-form'" in src
        assert "$.getJSON('/api/search'" in src

    def test_gallery_js_validates_colorbox(self) -> None:
        src = (FIXTURE_ROOT / "public/js/gallery.js").read_text(encoding="utf-8")
        assert "Gallery no disponible" in src
        assert "$.fn.colorbox" in src

    def test_colorbox_plugin_uses_prototype(self) -> None:
        src = (FIXTURE_ROOT / "public/js/plugins/jquery.colorbox.js").read_text(encoding="utf-8")
        assert "Array.prototype.shuffle" in src
        assert "$.fn.colorbox" in src

    def test_colorbox_plugin_dispatches_custom_event(self) -> None:
        src = (FIXTURE_ROOT / "public/js/plugins/jquery.colorbox.js").read_text(encoding="utf-8")
        assert "fxcolorbox:open" in src

    def test_dispatch_js_has_whitelist(self) -> None:
        src = (FIXTURE_ROOT / "public/js/dispatch.js").read_text(encoding="utf-8")
        assert "knownActions" in src
        assert "window[name]" in src

    def test_scss_hidden_defines_is_premium(self) -> None:
        src = (FIXTURE_ROOT / "public/scss/_hidden.scss").read_text(encoding="utf-8")
        assert ".is-premium" in src
        assert "display: none" in src


class TestServerSource:
    def test_search_route_has_full_and_partial(self) -> None:
        src = (FIXTURE_ROOT / "server/routes/search.js").read_text(encoding="utf-8")
        assert "lower.length < 3" in src
        assert "mode: 'partial'" in src
        assert "mode: 'full'" in src
        assert "sanitize.escapeHtml" in src
        # La rama partial no usa escapeHtml (concatenacion directa).
        # Lo verificamos con el test runtime.

    def test_contact_route_uses_multer(self) -> None:
        src = (FIXTURE_ROOT / "server/routes/contact.js").read_text(encoding="utf-8")
        assert "multer" in src
        assert "validator.isEmail" in src
        assert "1024 * 1024" in src
        assert "500 * 1024" in src
        assert "registry.get('sendEmail')" in src
        assert "handler_not_found" in src

    def test_gallery_route_has_csv_endpoint(self) -> None:
        src = (FIXTURE_ROOT / "server/routes/gallery.js").read_text(encoding="utf-8")
        assert "getGalleryAsCSV" in src
        assert "/csv" in src

    def test_registry_uses_kebab_case(self) -> None:
        src = (FIXTURE_ROOT / "server/plugins/registry.js").read_text(encoding="utf-8")
        assert "handlers['send-email']" in src
        assert "handlers['list-gallery']" in src


class TestTrapsEcosystem:
    def test_script_order_in_html(self) -> None:
        html = (FIXTURE_ROOT / "public/index.html").read_text(encoding="utf-8")
        jq = html.index("jquery-3.7.1.min.js")
        cb = html.index("jquery.colorbox.js")
        ap = html.index("/js/app.js")
        ga = html.index("gallery.js")
        assert jq < cb < ap < ga

    def test_inline_onclick_in_html(self) -> None:
        html = (FIXTURE_ROOT / "public/index.html").read_text(encoding="utf-8")
        assert re.search(r"onclick=[\"']window\.App\.run\(", html)

    def test_data_action_kebab_in_html(self) -> None:
        html = (FIXTURE_ROOT / "public/index.html").read_text(encoding="utf-8")
        assert re.search(r"data-action=[\"']open-search[\"']", html)

    def test_search_uses_document_delegation(self) -> None:
        src = (FIXTURE_ROOT / "public/js/search.js").read_text(encoding="utf-8")
        assert "$(document).on('submit', '#fx-search-form'" in src

    def test_gallery_uses_document_delegation(self) -> None:
        src = (FIXTURE_ROOT / "public/js/gallery.js").read_text(encoding="utf-8")
        assert "$(document).on('change', '#fx-gallery-filter'" in src

    def test_colorbox_monkey_patches(self) -> None:
        src = (FIXTURE_ROOT / "public/js/plugins/jquery.colorbox.js").read_text(encoding="utf-8")
        assert "Array.prototype.shuffle" in src
        assert "$.fn.colorbox" in src

    def test_dispatch_uses_window_name(self) -> None:
        src = (FIXTURE_ROOT / "public/js/dispatch.js").read_text(encoding="utf-8")
        assert "window[name]" in src


class TestTrapsPackage:
    def test_registry_kebab_vs_route_camel(self) -> None:
        reg = (FIXTURE_ROOT / "server/plugins/registry.js").read_text(encoding="utf-8")
        contact = (FIXTURE_ROOT / "server/routes/contact.js").read_text(encoding="utf-8")
        assert "handlers['send-email']" in reg
        assert "registry.get('sendEmail')" in contact

    def test_search_partial_no_escape(self) -> None:
        contact = (FIXTURE_ROOT / "server/routes/search.js").read_text(encoding="utf-8")
        # Quitamos comentarios para no falsear el match.
        no_comments = re.sub(r"//.*$", "", contact, flags=re.MULTILINE)
        # En la rama 'if (lower.length < 3)' no debe aparecer sanitize.
        m = re.search(r"if \(lower\.length < 3\) \{", no_comments)
        assert m is not None
        # Tomamos 600 chars tras el match (cubre el cuerpo del if).
        body = no_comments[m.start():m.start() + 600]
        assert "sanitize" not in body

    def test_whitelist_camelcase_kebab_in_html(self) -> None:
        app = (FIXTURE_ROOT / "public/js/app.js").read_text(encoding="utf-8")
        html = (FIXTURE_ROOT / "public/index.html").read_text(encoding="utf-8")
        assert "'openSearch'" in app
        assert "data-action=\"open-search\"" in html

    def test_colorbox_validation_in_gallery(self) -> None:
        gal = (FIXTURE_ROOT / "public/js/gallery.js").read_text(encoding="utf-8")
        assert "typeof $.fn.colorbox !== 'function'" in gal

    def test_multer_threshold_mismatch(self) -> None:
        contact = (FIXTURE_ROOT / "server/routes/contact.js").read_text(encoding="utf-8")
        # 1 MB (1024*1024) y 500 KB (500*1024) en el mismo archivo.
        assert "1024 * 1024" in contact
        assert "500 * 1024" in contact


class TestTrapsSuperficial:
    def test_deadcode_exports_lodash(self) -> None:
        src = (FIXTURE_ROOT / "server/lib/deadCode.js").read_text(encoding="utf-8")
        assert "uniqueId" in src
        assert "deburr" in src
        assert "template" in src
        assert "shuffle" in src

    def test_debounce_plugin_exists_and_unused(self) -> None:
        f = FIXTURE_ROOT / "public/js/plugins/jquery.debounce.js"
        assert f.is_file()
        src = f.read_text(encoding="utf-8")
        assert "$.fn.debounce" in src
        # Verificamos que el resto de public/ no usa $.fn.debounce.
        for p in (FIXTURE_ROOT / "public").rglob("*.js"):
            if p.name == "jquery.debounce.js":
                continue
            t = p.read_text(encoding="utf-8", errors="replace")
            assert "$.fn.debounce" not in t, f"$.fn.debounce used in {p.name}"

    def test_getGalleryAsCSV_exported_but_unused_in_index(self) -> None:
        gal = (FIXTURE_ROOT / "server/routes/gallery.js").read_text(encoding="utf-8")
        idx = (FIXTURE_ROOT / "server/index.js").read_text(encoding="utf-8")
        assert "getGalleryAsCSV" in gal
        assert "getGalleryAsCSV" not in idx


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-vanilla-js-legacy" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_package_json_has_jest(self) -> None:
        pkg = json.loads((FIXTURE_ROOT / "package.json").read_text(encoding="utf-8"))
        assert "jest" in pkg.get("devDependencies", {}) or "jest" in pkg.get("dependencies", {})

    def test_package_json_has_supertest(self) -> None:
        pkg = json.loads((FIXTURE_ROOT / "package.json").read_text(encoding="utf-8"))
        assert "supertest" in pkg.get("devDependencies", {})

    def test_gulpfile_exists(self) -> None:
        assert (FIXTURE_ROOT / "gulpfile.js").is_file()


class TestGroundTruthDocs:
    def test_ground_truth_md_exists(self) -> None:
        assert (GT_DIR / "GROUND_TRUTH.md").is_file()

    def test_ground_truth_md_mentions_3_features(self) -> None:
        text = (GT_DIR / "GROUND_TRUTH.md").read_text(encoding="utf-8")
        assert "FEAT-001" in text
        assert "FEAT-002" in text
        assert "FEAT-003" in text

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20
        for tok in tokens:
            assert tok.startswith("NPRGT-FXVANILLA-")
