"""Tests del ground truth de fx-spring-boot (F06m)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-spring-boot"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-spring-boot"


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
        assert "cuentas" in names
        assert "transferencias" in names
        assert "auditoria" in names
        assert "notificaciones-asíncronas" in names or "notificaciones" in names

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
        assert "spring-boot-starter-data-jpa" in names
        assert "spring-boot-starter-security" in names
        assert "lombok" in names

    def test_surfaces_listed(self) -> None:
        gt = _load_gt()
        assert len(gt.get("surfaces", [])) >= 12


class TestUniqueTokensFile:
    def test_at_least_20_tokens(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20, f"only {len(tokens)} tokens"

    def test_tokens_have_correct_prefix(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        for tok in tokens:
            assert tok.startswith("NPRGT-FXSPRING-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"node_modules", "target", "dist", ".git", "build"}
        skip_files = {"unique_tokens.txt", "package-lock.json"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            if any(part in skip_dirs for part in path.relative_to(FIXTURE_ROOT).parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".java", ".sql", ".yml", ".yaml", ".xml",
                                    ".md", ".txt", ".sh"):
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


class TestSpringBootStructure:
    def test_pom_xml(self) -> None:
        assert (FIXTURE_ROOT / "pom.xml").is_file()

    def test_application_yml(self) -> None:
        assert (FIXTURE_ROOT / "src/main/resources/application.yml").is_file()

    def test_application_yml_test(self) -> None:
        assert (FIXTURE_ROOT / "src/test/resources/application-test.yml").is_file()

    def test_flyway_migration(self) -> None:
        assert (FIXTURE_ROOT / "src/main/resources/db/migration/V1__init.sql").is_file()

    def test_logback(self) -> None:
        assert (FIXTURE_ROOT / "src/main/resources/logback-spring.xml").is_file()

    def test_application_class(self) -> None:
        assert (FIXTURE_ROOT / "src/main/java/com/example/fxspring/FxSpringApplication.java").is_file()

    def test_security_config(self) -> None:
        assert (FIXTURE_ROOT / "src/main/java/com/example/fxspring/config/SecurityConfig.java").is_file()

    def test_database_config(self) -> None:
        assert (FIXTURE_ROOT / "src/main/java/com/example/fxspring/config/DatabaseConfig.java").is_file()

    def test_async_config(self) -> None:
        assert (FIXTURE_ROOT / "src/main/java/com/example/fxspring/config/AsyncConfig.java").is_file()

    def test_domain_entities(self) -> None:
        for e in ("Cuenta", "Transferencia", "Auditoria", "Notificacion"):
            assert (FIXTURE_ROOT / f"src/main/java/com/example/fxspring/domain/{e}.java").is_file(), f"missing {e}.java"

    def test_repositories(self) -> None:
        for r in ("CuentaRepository", "TransferenciaRepository", "NotificacionRepository", "AuditoriaRepository"):
            assert (FIXTURE_ROOT / f"src/main/java/com/example/fxspring/repository/{r}.java").is_file(), f"missing {r}.java"

    def test_services(self) -> None:
        for s in ("CuentaService", "TransferenciaService", "AuditoriaService", "NotificacionService"):
            assert (FIXTURE_ROOT / f"src/main/java/com/example/fxspring/service/{s}.java").is_file(), f"missing {s}.java"

    def test_controllers(self) -> None:
        for c in ("CuentaController", "TransferenciaController", "AuditoriaController"):
            assert (FIXTURE_ROOT / f"src/main/java/com/example/fxspring/controller/{c}.java").is_file(), f"missing {c}.java"

    def test_event_listener(self) -> None:
        assert (FIXTURE_ROOT / "src/main/java/com/example/fxspring/event/TransferenciaRealizadaEvent.java").is_file()
        assert (FIXTURE_ROOT / "src/main/java/com/example/fxspring/listener/NotificacionListener.java").is_file()

    def test_tests_dir(self) -> None:
        assert (FIXTURE_ROOT / "src/test/java").is_dir()


class TestSpringBootSource:
    def test_spring_boot_application_annotation(self) -> None:
        app = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/FxSpringApplication.java").read_text(encoding="utf-8")
        assert "@SpringBootApplication" in app

    def test_security_filter_chain_bean(self) -> None:
        sec = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/config/SecurityConfig.java").read_text(encoding="utf-8")
        assert "SecurityFilterChain" in sec
        assert "hasRole(\"ADMIN\")" in sec

    def test_conditional_on_property_postgres(self) -> None:
        db = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/config/DatabaseConfig.java").read_text(encoding="utf-8")
        assert "@ConditionalOnProperty" in db
        assert "havingValue = \"postgres\"" in db

    def test_lombok_data_on_entities(self) -> None:
        for e in ("Cuenta", "Transferencia", "Auditoria", "Notificacion"):
            text = (FIXTURE_ROOT / f"src/main/java/com/example/fxspring/domain/{e}.java").read_text(encoding="utf-8")
            assert "import lombok.Data" in text
            assert "@Data" in text

    def test_async_annotation_on_service(self) -> None:
        notif = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/service/NotificacionService.java").read_text(encoding="utf-8")
        assert "@Async" in notif

    def test_transactional_event_listener(self) -> None:
        listener = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/listener/NotificacionListener.java").read_text(encoding="utf-8")
        assert "@TransactionalEventListener" in listener
        assert "AFTER_COMMIT" in listener


class TestTrapsEcosystem:
    def test_e01_conditional_on_property(self) -> None:
        db = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/config/DatabaseConfig.java").read_text(encoding="utf-8")
        assert "@ConditionalOnProperty" in db
        assert "havingValue = \"postgres\"" in db

    def test_e02_aop_proxy_autoinvocation(self) -> None:
        svc = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/service/TransferenciaService.java").read_text(encoding="utf-8")
        assert "this.validarSaldo" in svc
        assert "@Transactional" in svc
        assert "REQUIRES_NEW" in svc

    def test_e03_derived_queries(self) -> None:
        repo = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/repository/CuentaRepository.java").read_text(encoding="utf-8")
        assert "findByEmail" in repo
        assert "findByEmailAndEstado" in repo
        assert "findByEstado" in repo
        # Los metodos son declaraciones (terminan en ;), no tienen body.
        assert "findByEmail(String email);" in repo

    def test_e04_security_filter_chain_single(self) -> None:
        sec = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/config/SecurityConfig.java").read_text(encoding="utf-8")
        assert sec.count("requestMatchers(") >= 4
        assert "/api/v1/logs/**" in sec  # usamos /logs para evitar CC-11

    def test_e05_transactional_event_listener(self) -> None:
        listener = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/listener/NotificacionListener.java").read_text(encoding="utf-8")
        assert "@TransactionalEventListener" in listener
        assert "AFTER_COMMIT" in listener

    def test_e06_lombok_data(self) -> None:
        cuenta = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/domain/Cuenta.java").read_text(encoding="utf-8")
        assert "import lombok.Data" in cuenta
        assert "@Data" in cuenta
        # El codigo fuente no contiene getters/setters explicitos.
        assert "public Long getId()" not in cuenta
        assert "public void setId" not in cuenta


class TestTrapsPackage:
    def test_p01_transactional_class_level(self) -> None:
        svc = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/service/CuentaService.java").read_text(encoding="utf-8")
        # @Transactional a nivel de clase (linea 21).
        assert "@Service\n@Transactional\npublic class" in svc

    def test_p02_cacheable_no_unless(self) -> None:
        svc = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/service/CuentaService.java").read_text(encoding="utf-8")
        assert "@Cacheable" in svc
        assert "unless" not in svc  # trampa

    def test_p03_async_no_enable_async(self) -> None:
        app = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/FxSpringApplication.java").read_text(encoding="utf-8")
        assert "@EnableAsync" not in app
        notif = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/service/NotificacionService.java").read_text(encoding="utf-8")
        assert "@Async" in notif

    def test_p04_preauthorize_incorrect_spel(self) -> None:
        ctrl = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/controller/TransferenciaController.java").read_text(encoding="utf-8")
        assert "@PreAuthorize" in ctrl
        assert "authentication.principal.id" in ctrl

    def test_p05_version_no_optimistic_handling(self) -> None:
        entity = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/domain/Transferencia.java").read_text(encoding="utf-8")
        assert "@Version" in entity
        svc = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/service/AuditoriaService.java").read_text(encoding="utf-8")
        assert "OptimisticLockException" not in svc

    def test_p06_listener_silent_fail(self) -> None:
        listener = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/listener/NotificacionListener.java").read_text(encoding="utf-8")
        assert "catch (" not in listener


class TestTrapsSuperficial:
    def test_s01_cuenta_controller_listAll_exists(self) -> None:
        ctrl = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/controller/CuentaController.java").read_text(encoding="utf-8")
        assert "public ResponseEntity<Page<Cuenta>> listAll" in ctrl

    def test_s02_auditoria_no_preauthorize(self) -> None:
        ctrl = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/controller/AuditoriaController.java").read_text(encoding="utf-8")
        # Buscamos la firma del metodo (sin la anotacion).
        idx = ctrl.index("public List<")
        assert idx > 0
        brace = ctrl.index("{", idx)
        sig = ctrl[idx:brace]
        assert "@PreAuthorize" not in sig

    def test_s03_async_config_no_yml_property(self) -> None:
        cfg = (FIXTURE_ROOT / "src/main/java/com/example/fxspring/config/AsyncConfig.java").read_text(encoding="utf-8")
        assert "@Bean" in cfg
        yml = (FIXTURE_ROOT / "src/main/resources/application.yml").read_text(encoding="utf-8")
        assert "spring.task.execution.pool" not in yml


class TestManifest:
    def test_manifest_yaml(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()
        content = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "fx-spring-boot" in content

    def test_dockerfile(self) -> None:
        assert (FIXTURE_ROOT / "Dockerfile.test").is_file()

    def test_makefile(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_build_history(self) -> None:
        assert (FIXTURE_ROOT / "build-history.sh").is_file()

    def test_pom_has_spring_boot(self) -> None:
        pom = (FIXTURE_ROOT / "pom.xml").read_text(encoding="utf-8")
        assert "spring-boot-starter-web" in pom
        assert "spring-boot-starter-data-jpa" in pom
        assert "lombok" in pom

    def test_pom_has_testcontainers(self) -> None:
        pom = (FIXTURE_ROOT / "pom.xml").read_text(encoding="utf-8")
        assert "testcontainers" in pom
        assert "postgresql" in pom

    def test_unique_tokens_have_prefix(self) -> None:
        tokens = (FIXTURE_ROOT / "unique_tokens.txt").read_text().split()
        assert len(tokens) >= 20
        for tok in tokens:
            assert tok.startswith("NPRGT-FXSPRING-")
