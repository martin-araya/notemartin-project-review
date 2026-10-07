"""Tests del ground truth de fx-ruby-rails (F06v)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-ruby-rails"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-ruby-rails"


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
        assert "proyectos" in names
        assert "facturas" in names
        assert "recordatorios" in names

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
        assert "rails" in names
        assert "sqlite3" in names
        assert "sidekiq" in names
        assert "turbo-rails" in names

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
            assert tok.startswith("NPRGT-FXRAILS-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"vendor", "node_modules", ".git", ".bundle", "tmp", "log", "storage"}
        skip_files = {"unique_tokens.txt", "Gemfile.lock"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(part in skip_dirs for part in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".rb", ".md", ".txt", ".sh", ".yml", ".yaml",
                                    ".json", ".erb", ".html", ".css", ".js"):
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

    def test_all_traps_resolve(self) -> None:
        import re
        gt = _load_gt()
        errors = []
        for t in gt["traps"] + gt["package_traps"] + gt["superficial_traps"]:
            where = t.get("where", "")
            # Extraemos todas las rutas candidatas (texto tipo path/file.rb) del string `where`.
            candidates = re.findall(r"[\w/.\-]+\.rb", where)
            for file_part in candidates:
                if "/" not in file_part:
                    continue
                full = FIXTURE_ROOT / file_part
                if not full.is_file():
                    errors.append(f"trap {t['id']}: missing file {file_part}")
        assert not errors, "trap locations with missing files:\n" + "\n".join(errors)

    def test_all_surfaces_have_handler_file(self) -> None:
        gt = _load_gt()
        for s in gt.get("surfaces", []):
            f = s.get("file", "")
            if f and "/" in f:
                full = FIXTURE_ROOT / f
                assert full.is_file(), f"surface {s.get('id')} missing file {f}"


class TestRubyStructure:
    def test_gemfile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Gemfile").is_file()

    def test_rails_application_exists(self) -> None:
        assert (FIXTURE_ROOT / "config/application.rb").is_file()

    def test_routes_exists(self) -> None:
        assert (FIXTURE_ROOT / "config/routes.rb").is_file()

    def test_database_yml_exists(self) -> None:
        assert (FIXTURE_ROOT / "config/database.yml").is_file()

    def test_proyecto_model_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/models/proyecto.rb").is_file()

    def test_factura_model_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/models/factura.rb").is_file()

    def test_recordatorio_model_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/models/recordatorio.rb").is_file()

    def test_recordatorio_subclasses_exist(self) -> None:
        assert (FIXTURE_ROOT / "app/models/recordatorio/email.rb").is_file()
        assert (FIXTURE_ROOT / "app/models/recordatorio/sms.rb").is_file()
        assert (FIXTURE_ROOT / "app/models/recordatorio/push.rb").is_file()

    def test_proyectos_controller_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/controllers/proyectos_controller.rb").is_file()

    def test_facturas_controller_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/controllers/facturas_controller.rb").is_file()

    def test_recordatorios_controller_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/controllers/recordatorios_controller.rb").is_file()

    def test_enviar_recordatorio_job_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/jobs/enviar_recordatorio_job.rb").is_file()

    def test_generar_factura_pdf_job_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/jobs/generar_factura_pdf_job.rb").is_file()

    def test_trackable_concern_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/models/concerns/trackable.rb").is_file()

    def test_migrations_exist(self) -> None:
        migs = list((FIXTURE_ROOT / "db/migrate").glob("*.rb"))
        assert len(migs) >= 3

    def test_views_exist(self) -> None:
        views = list((FIXTURE_ROOT / "app/views").rglob("*.erb"))
        assert len(views) >= 5


class TestTrapsEcosystem:
    def test_e01_convention_routes(self) -> None:
        routes = (FIXTURE_ROOT / "config/routes.rb").read_text(encoding="utf-8")
        assert "resources :proyectos" in routes
        assert "resources :facturas" in routes
        assert "resources :recordatorios" in routes

    def test_e02_callbacks_proyecto(self) -> None:
        model = (FIXTURE_ROOT / "app/models/proyecto.rb").read_text(encoding="utf-8")
        assert "before_save :normaliza_codigo" in model
        assert "after_destroy :registrar_baja_en_log" in model

    def test_e02_callbacks_factura(self) -> None:
        model = (FIXTURE_ROOT / "app/models/factura.rb").read_text(encoding="utf-8")
        assert "after_commit :encolar_generacion_pdf" in model

    def test_e03_concern_included_do(self) -> None:
        concern = (FIXTURE_ROOT / "app/models/concerns/trackable.rb").read_text(encoding="utf-8")
        assert "included do" in concern
        assert "before_create :assign_tracking_id" in concern

    def test_e03_concern_in_proyecto_and_factura(self) -> None:
        proyecto = (FIXTURE_ROOT / "app/models/proyecto.rb").read_text(encoding="utf-8")
        factura = (FIXTURE_ROOT / "app/models/factura.rb").read_text(encoding="utf-8")
        assert "include Trackable" in proyecto
        assert "include Trackable" in factura

    def test_e04_legacy_constants_define_method(self) -> None:
        init = (FIXTURE_ROOT / "config/initializers/legacy_constants.rb").read_text(encoding="utf-8")
        assert "module LegacyConstants" in init
        assert "module Resolver" in init
        assert "define_method" in init
        assert "method_missing" in init

    def test_e05_sti_inheritance_column(self) -> None:
        model = (FIXTURE_ROOT / "app/models/recordatorio.rb").read_text(encoding="utf-8")
        assert "self.inheritance_column = :type" in model

    def test_e05_sti_subclasses_defined(self) -> None:
        email = (FIXTURE_ROOT / "app/models/recordatorio/email.rb").read_text(encoding="utf-8")
        sms = (FIXTURE_ROOT / "app/models/recordatorio/sms.rb").read_text(encoding="utf-8")
        push = (FIXTURE_ROOT / "app/models/recordatorio/push.rb").read_text(encoding="utf-8")
        assert "class Email < Recordatorio" in email
        assert "class Sms < Recordatorio" in sms
        assert "class Push < Recordatorio" in push

    def test_e05_sti_migration_column_type(self) -> None:
        mig = (FIXTURE_ROOT / "db/migrate/003_create_recordatorios.rb").read_text(encoding="utf-8")
        assert "t.string :type" in mig

    def test_e06_monkey_patch_array(self) -> None:
        init = (FIXTURE_ROOT / "config/initializers/patch_array.rb").read_text(encoding="utf-8")
        assert "class Array" in init
        assert "def sum_safe" in init


class TestTrapsPackage:
    def test_p01_silent_retry_enviar(self) -> None:
        job = (FIXTURE_ROOT / "app/jobs/enviar_recordatorio_job.rb").read_text(encoding="utf-8")
        assert "retry_on StandardError" in job
        assert "attempts: 3" in job

    def test_p01_silent_retry_generar(self) -> None:
        job = (FIXTURE_ROOT / "app/jobs/generar_factura_pdf_job.rb").read_text(encoding="utf-8")
        assert "retry_on StandardError" in job
        assert "attempts: 2" in job

    def test_p02_update_columns_to_skip_validation(self) -> None:
        job = (FIXTURE_ROOT / "app/jobs/enviar_recordatorio_job.rb").read_text(encoding="utf-8")
        assert "update_columns" in job
        assert "estado: \"caducado\"" in job

    def test_p03_concern_included_twice(self) -> None:
        proyecto = (FIXTURE_ROOT / "app/models/proyecto.rb").read_text(encoding="utf-8")
        factura = (FIXTURE_ROOT / "app/models/factura.rb").read_text(encoding="utf-8")
        assert "include Trackable" in proyecto
        assert "include Trackable" in factura

    def test_p04_sti_find_sti_class_silences(self) -> None:
        model = (FIXTURE_ROOT / "app/models/recordatorio.rb").read_text(encoding="utf-8")
        assert "def self.find_sti_class" in model
        assert "Recordatorio" in model  # returns Recordatorio base

    def test_p05_route_convention_override(self) -> None:
        routes = (FIXTURE_ROOT / "config/routes.rb").read_text(encoding="utf-8")
        assert "panel/legacy" in routes

    def test_p06_initializer_legacy_constants(self) -> None:
        init = (FIXTURE_ROOT / "config/initializers/legacy_constants.rb").is_file()
        assert init


class TestTrapsSuperficial:
    def test_s01_dead_legacy_formatter(self) -> None:
        service = (FIXTURE_ROOT / "app/services/legacy_text_formatter.rb").read_text(encoding="utf-8")
        assert "class LegacyTextFormatter" in service
        assert "def self.legacy_format" in service
        # Verificamos que no hay consumidores en app/ (excluyendo el propio archivo).
        consumers = []
        for f in (FIXTURE_ROOT / "app").rglob("*.rb"):
            if "legacy_text_formatter" in f.name:
                continue
            try:
                if "legacy_format" in f.read_text(encoding="utf-8", errors="replace"):
                    consumers.append(f.relative_to(FIXTURE_ROOT).as_posix())
            except Exception:
                continue
        assert consumers == [], f"LegacyTextFormatter.legacy_format no deberia tener consumidores pero aparece en: {consumers}"

    def test_s02_empty_concerns_dir(self) -> None:
        concerns = FIXTURE_ROOT / "app/controllers/concerns"
        assert concerns.is_dir()
        files = [f for f in concerns.iterdir() if f.name != ".keep"]
        assert files == [], f"app/controllers/concerns/ deberia estar vacio (solo .keep) pero contiene: {files}"

    def test_s03_unused_partial(self) -> None:
        assert (FIXTURE_ROOT / "app/views/recordatorios/_unused_partial.html.erb").is_file()


class TestManifest:
    def test_manifest_file_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name_is_fx_ruby_rails(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "name: fx-ruby-rails" in text

    def test_manifest_requires_linux_macos_windows(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "- linux" in text
        assert "- macos" in text
        assert "- windows" in text

    def test_manifest_test_cmd_starts_with_make(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "test_cmd: make test" in text

    def test_manifest_container_enabled(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "enabled: true" in text

    def test_manifest_image_tag_starts_with_npr(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "image_tag: npr-fx-ruby-rails" in text

    def test_manifest_format_version_is_1(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "ground_truth_format_version: 1" in text
