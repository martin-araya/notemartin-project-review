"""Tests del ground truth de fx-php-laravel (F06u)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-php-laravel"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-php-laravel"


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
        assert "inmuebles" in names
        assert "visitas" in names
        assert "contratos" in names

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
        assert "laravel/framework" in names
        assert "guzzlehttp/guzzle" in names
        assert "phpunit/phpunit" in names
        assert "mockery/mockery" in names

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
            assert tok.startswith("NPRGT-FXPLAR-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"vendor", "node_modules", ".git", ".phpunit.cache", "storage"}
        skip_files = {"unique_tokens.txt", "composer.lock"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(part in skip_dirs for part in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".php", ".md", ".txt", ".sh", ".yml", ".yaml",
                                    ".json", ".xml"):
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
        gt = _load_gt()
        errors = []
        for t in gt["traps"] + gt["package_traps"] + gt["superficial_traps"]:
            where = t.get("where", "")
            # Las trampas pueden tener varias ubicaciones separadas por + o comas.
            for location in [p.strip() for p in where.replace(",", "+").split("+")]:
                if not location:
                    continue
                # Extraer archivo:línea si esta presente.
                if ":" in location and not location.startswith("App\\") and not location.startswith("Schedule"):
                    # formato archivo:línea
                    file_part = location.split(":")[0].strip()
                    if file_part and "/" in file_part:
                        full = FIXTURE_ROOT / file_part
                        if not full.is_file():
                            errors.append(f"trap {t['id']}: missing file {file_part}")
                else:
                    # Es una clase/funcion sin ruta explicita; saltar.
                    pass
        assert not errors, "trap locations with missing files:\n" + "\n".join(errors)

    def test_all_surfaces_have_handler_file(self) -> None:
        gt = _load_gt()
        for s in gt.get("surfaces", []):
            f = s.get("file", "")
            if f and "/" in f:
                full = FIXTURE_ROOT / f
                assert full.is_file(), f"surface {s.get('id')} missing file {f}"


class TestPhpStructure:
    def test_artisan_exists(self) -> None:
        assert (FIXTURE_ROOT / "artisan").is_file()

    def test_composer_json_exists(self) -> None:
        assert (FIXTURE_ROOT / "composer.json").is_file()

    def test_phpunit_xml_exists(self) -> None:
        assert (FIXTURE_ROOT / "phpunit.xml").is_file()

    def test_bootstrap_app_exists(self) -> None:
        assert (FIXTURE_ROOT / "bootstrap/app.php").is_file()

    def test_http_kernel_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Http/Kernel.php").is_file()

    def test_console_kernel_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Console/Kernel.php").is_file()

    def test_bootstrap_providers_exists(self) -> None:
        assert (FIXTURE_ROOT / "bootstrap/providers.php").is_file()

    def test_config_app_exists(self) -> None:
        assert (FIXTURE_ROOT / "config/app.php").is_file()

    def test_config_database_exists(self) -> None:
        assert (FIXTURE_ROOT / "config/database.php").is_file()

    def test_config_queue_exists(self) -> None:
        assert (FIXTURE_ROOT / "config/queue.php").is_file()

    def test_property_model_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Models/Property.php").is_file()

    def test_visit_model_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Models/Visit.php").is_file()

    def test_contract_model_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Models/Contract.php").is_file()

    def test_property_controller_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Http/Controllers/PropertyController.php").is_file()

    def test_visit_controller_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Http/Controllers/VisitController.php").is_file()

    def test_contract_controller_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Http/Controllers/ContractController.php").is_file()

    def test_inmueble_provider_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Providers/InmuebleServiceProvider.php").is_file()

    def test_legacy_provider_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Providers/LegacyServiceProvider.php").is_file()

    def test_event_provider_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Providers/EventServiceProvider.php").is_file()

    def test_pricing_facade_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Facades/PricingFacade.php").is_file()

    def test_pricing_service_exists(self) -> None:
        assert (FIXTURE_ROOT / "app/Pricing/PricingService.php").is_file()

    def test_web_routes_exist(self) -> None:
        assert (FIXTURE_ROOT / "routes/web.php").is_file()

    def test_api_routes_exist(self) -> None:
        assert (FIXTURE_ROOT / "routes/api.php").is_file()

    def test_console_routes_exist(self) -> None:
        assert (FIXTURE_ROOT / "routes/console.php").is_file()

    def test_migrations_exist(self) -> None:
        migs = list((FIXTURE_ROOT / "database/migrations").glob("*.php"))
        assert len(migs) >= 4


class TestTrapsEcosystem:
    def test_e01_facade_alias(self) -> None:
        config = (FIXTURE_ROOT / "config/app.php").read_text(encoding="utf-8")
        facade = (FIXTURE_ROOT / "app/Facades/PricingFacade.php").read_text(encoding="utf-8")
        assert "'Pricing' => App\\Facades\\PricingFacade::class" in config
        assert "getFacadeAccessor" in facade
        assert "'pricing.service'" in facade

    def test_e02_eloquent_magic(self) -> None:
        prop = (FIXTURE_ROOT / "app/Models/Property.php").read_text(encoding="utf-8")
        assert "getPriceEurosAttribute" in prop
        assert "scopeAvailable" in prop
        assert "public function visits()" in prop
        assert "static::observe(PropertyObserver::class)" in prop

    def test_e03_service_provider_bindings(self) -> None:
        prov = (FIXTURE_ROOT / "app/Providers/InmuebleServiceProvider.php").read_text(encoding="utf-8")
        assert "VisitRepository::class, EloquentVisitRepository::class" in prov
        assert "singleton('pricing.service'" in prov

    def test_e04_event_listener(self) -> None:
        prov = (FIXTURE_ROOT / "app/Providers/EventServiceProvider.php").read_text(encoding="utf-8")
        assert "protected $listen = [" in prov
        assert "VisitScheduled::class" in prov
        assert "SendVisitConfirmation::class" in prov

    def test_e05_middleware_group(self) -> None:
        kernel = (FIXTURE_ROOT / "app/Http/Kernel.php").read_text(encoding="utf-8")
        web = (FIXTURE_ROOT / "routes/web.php").read_text(encoding="utf-8")
        assert "'web' => [" in kernel
        assert "EnsureTenant::class" in kernel
        assert "Route::get('/properties/{property}'" in web

    def test_e06_console_schedule(self) -> None:
        kernel = (FIXTURE_ROOT / "app/Console/Kernel.php").read_text(encoding="utf-8")
        assert "command(ExpireContracts::class)" in kernel
        assert "->dailyAt('00:00')" in kernel


class TestTrapsPackage:
    def test_p01_job_silent_retry(self) -> None:
        job = (FIXTURE_ROOT / "app/Jobs/SendVisitReminder.php").read_text(encoding="utf-8")
        assert "public int $tries = 3;" in job
        assert "public int $backoff = 10;" in job

    def test_p02_job_empty_catch(self) -> None:
        job = (FIXTURE_ROOT / "app/Jobs/GenerateContractPdf.php").read_text(encoding="utf-8")
        assert "public int $tries = 1;" in job
        assert "catch (\\Throwable $e)" in job
        assert "Log::error(" in job
        # Verifica que NO hay rethrow despues del catch.
        after = job[job.index("catch (\\Throwable $e)"):]
        assert "throw $e;" not in after

    def test_p03_facade_alias_typo(self) -> None:
        config = (FIXTURE_ROOT / "config/app.php").read_text(encoding="utf-8")
        assert "'Pricing' => App\\Facades\\PricingFacade::class" in config

    def test_p04_queue_driver_mismatch(self) -> None:
        phpunit = (FIXTURE_ROOT / "phpunit.xml").read_text(encoding="utf-8")
        queue = (FIXTURE_ROOT / "config/queue.php").read_text(encoding="utf-8")
        assert "name=\"QUEUE_CONNECTION\" value=\"database\"" in phpunit
        assert "'database'" in queue
        assert "'redis'" in queue

    def test_p05_eloquent_n_plus_one(self) -> None:
        ctrl = (FIXTURE_ROOT / "app/Http/Controllers/PropertyController.php").read_text(encoding="utf-8")
        assert "Property::query()" in ctrl
        assert "->limit(50)" in ctrl
        assert "withCount(" not in ctrl
        assert "$property->visits()->count()" in ctrl

    def test_p06_unused_middleware(self) -> None:
        kernel = (FIXTURE_ROOT / "app/Http/Kernel.php").read_text(encoding="utf-8")
        mw = (FIXTURE_ROOT / "app/Http/Middleware/EnsureTenant.php").read_text(encoding="utf-8")
        assert "EnsureTenant::class" in kernel
        assert "class EnsureTenant" in mw


class TestTrapsSuperficial:
    def test_s01_dead_legacy_provider(self) -> None:
        config = (FIXTURE_ROOT / "config/app.php").read_text(encoding="utf-8")
        legacy = (FIXTURE_ROOT / "app/Providers/LegacyServiceProvider.php").read_text(encoding="utf-8")
        assert "LegacyServiceProvider::class" in config
        assert "class LegacyServiceProvider" in legacy
        assert "// legacy only" in legacy

    def test_s02_dead_helper_reference(self) -> None:
        prov = (FIXTURE_ROOT / "app/Providers/InmuebleServiceProvider.php").read_text(encoding="utf-8")
        assert "App\\Pricing\\LegacyHelper" in prov
        assert not (FIXTURE_ROOT / "app/Pricing/LegacyHelper.php").exists()

    def test_s03_dead_route(self) -> None:
        web = (FIXTURE_ROOT / "routes/web.php").read_text(encoding="utf-8")
        assert "Route::get('/legacy'" in web
        assert "App\\Http\\Controllers\\LegacyController" in web
        assert not (FIXTURE_ROOT / "app/Http/Controllers/LegacyController.php").exists()


class TestManifest:
    def test_manifest_file_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name_is_fx_php_laravel(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "name: fx-php-laravel" in text

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
        assert "image_tag: npr-fx-php-laravel" in text

    def test_manifest_format_version_is_1(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "ground_truth_format_version: 1" in text
