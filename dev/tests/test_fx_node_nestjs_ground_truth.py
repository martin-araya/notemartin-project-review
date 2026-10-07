"""Tests del ground truth de fx-node-nestjs (F06r)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-node-nestjs"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-node-nestjs"


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
        assert "ordenes" in names
        assert "envios" in names
        assert "notificaciones" in names

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
        assert "@nestjs/core" in names
        assert "@nestjs/common" in names
        assert "typeorm" in names
        assert "bullmq" in names

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
            assert tok.startswith("NPRGT-FXNEST-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"node_modules", "dist", "coverage", ".git", "tests"}
        skip_files = {"unique_tokens.txt", "pytest.ini", "package.json",
                      "jest.config.js", "tsconfig.json", "tsconfig.build.json",
                      ".env.test", "nest-cli.json", "Dockerfile.test",
                      "conftest.ts"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".ts", ".md", ".txt", ".sh", ".yml", ".yaml",
                                    ".json", ".ini"):
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


class TestNestjsStructure:
    def test_main_ts(self) -> None:
        assert (FIXTURE_ROOT / "src/main.ts").is_file()

    def test_app_module(self) -> None:
        assert (FIXTURE_ROOT / "src/app.module.ts").is_file()

    def test_nest_cli_json(self) -> None:
        assert (FIXTURE_ROOT / "nest-cli.json").is_file()

    def test_package_json(self) -> None:
        assert (FIXTURE_ROOT / "package.json").is_file()

    def test_jest_config(self) -> None:
        assert (FIXTURE_ROOT / "jest.config.js").is_file()

    def test_tsconfig(self) -> None:
        assert (FIXTURE_ROOT / "tsconfig.json").is_file()

    def test_config_dir(self) -> None:
        for f in ("database.config.ts", "redis.config.ts", "app.config.ts",
                  "validation.schema.ts"):
            assert (FIXTURE_ROOT / "src/config" / f).is_file(), f"missing {f}"

    def test_common_dir(self) -> None:
        for f in ("guards/auth.guard.ts", "interceptors/timing.interceptor.ts",
                  "decorators/roles.decorator.ts", "decorators/log-execution.decorator.ts",
                  "decorators/current-user.decorator.ts", "filters/http-exception.filter.ts"):
            assert (FIXTURE_ROOT / "src/common" / f).is_file(), f"missing {f}"

    def test_messaging_dir(self) -> None:
        for f in ("message-queue.service.ts", "bullmq-message-queue.ts",
                  "in-memory-message-queue.ts", "microservice.controller.ts",
                  "order-event.handler.ts", "messaging.module.ts"):
            assert (FIXTURE_ROOT / "src/messaging" / f).is_file(), f"missing {f}"

    def test_orders_dir(self) -> None:
        for f in ("orders.module.ts", "orders.controller.ts", "orders.service.ts",
                  "entities/order.entity.ts", "dto/create-order.dto.ts"):
            assert (FIXTURE_ROOT / "src/orders" / f).is_file(), f"missing {f}"

    def test_shipments_dir(self) -> None:
        for f in ("shipments.module.ts", "shipments.controller.ts",
                  "shipments.service.ts", "entities/shipment.entity.ts"):
            assert (FIXTURE_ROOT / "src/shipments" / f).is_file(), f"missing {f}"

    def test_notifications_dir(self) -> None:
        for f in ("notifications.module.ts", "notifications.controller.ts",
                  "notifications.service.ts", "notifications.gateway.ts"):
            assert (FIXTURE_ROOT / "src/notifications" / f).is_file(), f"missing {f}"

    def test_health(self) -> None:
        assert (FIXTURE_ROOT / "src/health/health.controller.ts").is_file()

    def test_tests_dir(self) -> None:
        assert (FIXTURE_ROOT / "tests").is_dir()


class TestEcosystemTraps:
    def test_e01_modules_with_di_decorators(self) -> None:
        app = (FIXTURE_ROOT / "src/app.module.ts").read_text(encoding="utf-8")
        assert "@Module(" in app
        assert "imports:" in app
        assert "providers:" in app
        assert "controllers:" in app
        orders = (FIXTURE_ROOT / "src/orders/orders.module.ts").read_text(encoding="utf-8")
        assert "@Module(" in orders
        nest_cli = (FIXTURE_ROOT / "nest-cli.json").read_text(encoding="utf-8")
        assert "sourceRoot" in nest_cli

    def test_e02_app_guard_app_interceptor(self) -> None:
        app = (FIXTURE_ROOT / "src/app.module.ts").read_text(encoding="utf-8")
        assert "APP_GUARD" in app
        assert "APP_INTERCEPTOR" in app
        assert "APP_FILTER" in app
        assert "useClass: AuthGuard" in app
        assert "useClass: TimingInterceptor" in app

    def test_e03_custom_decorator_reflector(self) -> None:
        roles = (FIXTURE_ROOT / "src/common/decorators/roles.decorator.ts").read_text(encoding="utf-8")
        assert "SetMetadata" in roles
        guard = (FIXTURE_ROOT / "src/common/guards/auth.guard.ts").read_text(encoding="utf-8")
        assert "Reflector" in guard
        assert "getAllAndOverride" in guard
        timing = (FIXTURE_ROOT / "src/common/interceptors/timing.interceptor.ts").read_text(encoding="utf-8")
        assert "Reflector" in timing

    def test_e04_bullmq_producer_consumer_by_name(self) -> None:
        orders = (FIXTURE_ROOT / "src/orders/orders.service.ts").read_text(encoding="utf-8")
        assert "publish('order-queue'" in orders
        notif = (FIXTURE_ROOT / "src/notifications/notifications.service.ts").read_text(encoding="utf-8")
        assert "publish('order-queue'" in notif

    def test_e05_event_pattern_message_pattern(self) -> None:
        micro = (FIXTURE_ROOT / "src/messaging/microservice.controller.ts").read_text(encoding="utf-8")
        assert "@MessagePattern" in micro
        assert "order_created" in micro
        evt = (FIXTURE_ROOT / "src/messaging/order-event.handler.ts").read_text(encoding="utf-8")
        assert "@EventPattern" in evt
        main = (FIXTURE_ROOT / "src/main.ts").read_text(encoding="utf-8")
        assert "connectMicroservice" in main

    def test_e06_config_module_namespaces(self) -> None:
        db = (FIXTURE_ROOT / "src/config/database.config.ts").read_text(encoding="utf-8")
        assert "registerAs('database'" in db
        redis = (FIXTURE_ROOT / "src/config/redis.config.ts").read_text(encoding="utf-8")
        assert "registerAs('redis'" in redis
        app_c = (FIXTURE_ROOT / "src/config/app.config.ts").read_text(encoding="utf-8")
        assert "registerAs('app'" in app_c
        app_m = (FIXTURE_ROOT / "src/app.module.ts").read_text(encoding="utf-8")
        assert "load: [databaseConfig, redisConfig, appConfig]" in app_m
        assert "validationSchema" in app_m


class TestPackageTraps:
    def test_p01_circular_module_dependency(self) -> None:
        orders = (FIXTURE_ROOT / "src/orders/orders.module.ts").read_text(encoding="utf-8")
        assert "forwardRef" in orders

    def test_p02_global_guard_throws_on_missing_context(self) -> None:
        guard = (FIXTURE_ROOT / "src/common/guards/auth.guard.ts").read_text(encoding="utf-8")
        assert "InternalServerErrorException" in guard
        # Trampa: NO contiene la excepcion correcta de autenticacion.
        # Solo se valida que NO se usa un error apropiado.
        # La verificacion exacta se hace en el test de comportamiento.

    def test_p03_bullmq_producer_no_consumer_validation(self) -> None:
        notif = (FIXTURE_ROOT / "src/notifications/notifications.service.ts").read_text(encoding="utf-8")
        assert "publish(" in notif
        # Trampa: no hay verificacion de consumers.
        assert "subscribers.length" not in notif
        assert "hasHandlers" not in notif

    def test_p04_interceptor_breaks_streaming(self) -> None:
        timing = (FIXTURE_ROOT / "src/common/interceptors/timing.interceptor.ts").read_text(encoding="utf-8")
        assert "next.handle()" in timing
        assert "tap(" in timing

    def test_p05_custom_decorator_metadata_key_typo(self) -> None:
        decorator = (FIXTURE_ROOT / "src/common/decorators/log-execution.decorator.ts").read_text(encoding="utf-8")
        interceptor = (FIXTURE_ROOT / "src/common/interceptors/timing.interceptor.ts").read_text(encoding="utf-8")
        # Key del decorator es minusculas, key del interceptor es mayusculas.
        assert "'log_execution_time'" in decorator
        assert "'LogExecutionTime'" in interceptor

    def test_p06_microservice_transport_connected(self) -> None:
        main = (FIXTURE_ROOT / "src/main.ts").read_text(encoding="utf-8")
        assert "connectMicroservice" in main
        assert "startAllMicroservices" in main


class TestSuperficialTraps:
    def test_s01_dead_health_deep_endpoint(self) -> None:
        health = (FIXTURE_ROOT / "src/health/health.controller.ts").read_text(encoding="utf-8")
        assert "/deep" in health
        assert "@Get" in health

    def test_s02_dead_websocket_gateway(self) -> None:
        gateway = (FIXTURE_ROOT / "src/notifications/notifications.gateway.ts").read_text(encoding="utf-8")
        assert "WebSocketGateway" in gateway
        # NINGUN modulo importa NotificationsGateway.
        notif_module = (FIXTURE_ROOT / "src/notifications/notifications.module.ts").read_text(encoding="utf-8")
        assert "NotificationsGateway" not in notif_module

    def test_s03_dead_metrics_interceptor(self) -> None:
        metrics = (FIXTURE_ROOT / "src/common/interceptors/metrics.interceptor.ts").read_text(encoding="utf-8")
        assert "MetricsInterceptor" in metrics
        app_module = (FIXTURE_ROOT / "src/app.module.ts").read_text(encoding="utf-8")
        assert "MetricsInterceptor" not in app_module


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-node-nestjs" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_package_json_has_nestjs(self) -> None:
        pkg = (FIXTURE_ROOT / "package.json").read_text(encoding="utf-8")
        assert "@nestjs/core" in pkg
        assert "@nestjs/common" in pkg
        assert "typeorm" in pkg
        assert "bullmq" in pkg

    def test_jest_config(self) -> None:
        jest_c = (FIXTURE_ROOT / "jest.config.js").read_text(encoding="utf-8")
        assert "ts-jest" in jest_c

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 25
        for tok in tokens:
            assert tok.startswith("NPRGT-FXNEST-")