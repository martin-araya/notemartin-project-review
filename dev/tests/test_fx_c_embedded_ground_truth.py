"""Tests del ground truth de fx-c-embedded (F06y)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from dev.tools.check_ground_truth import check_cite


GT_DIR = Path(__file__).resolve().parents[1] / "ground-truth" / "fx-c-embedded"
FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "fx-c-embedded"


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
        assert "lectura-de-sensores" in names
        assert "protocolo-de-comandos-uart" in names
        assert "modo-bajo-consumo" in names

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
        assert "gcc" in names
        assert "make" in names
        assert "gnu-ld" in names
        assert "unity" in names

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
            assert tok.startswith("NPRGT-FXCEMB-"), f"bad prefix: {tok}"

    def test_tokens_not_in_fixture_source(self) -> None:
        tokens = (GT_DIR / "unique_tokens.txt").read_text().split()
        skip_dirs = {"build", "vendor", "node_modules", ".git", ".bundle", "tmp", "log", "storage"}
        skip_files = {"unique_tokens.txt", "build-history.sh"}
        for path in FIXTURE_ROOT.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(FIXTURE_ROOT).parts
            if any(part in skip_dirs for part in rel_parts):
                continue
            if path.name in skip_files:
                continue
            if path.suffix not in (".c", ".h", ".hpp", ".ld", ".py", ".sh", ".yml", ".yaml",
                                    ".json", ".md", ".txt"):
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
            candidates = re.findall(r"[\w/.\-]+\.(?:c|h|hpp|ld|md)", where)
            for file_part in candidates:
                if file_part and "/" in file_part and not file_part.startswith("."):
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


class TestCStructure:
    def test_cmakelists_or_makefile_exists(self) -> None:
        assert (FIXTURE_ROOT / "Makefile").is_file()

    def test_firmware_ld_exists(self) -> None:
        assert (FIXTURE_ROOT / "firmware.ld").is_file()

    def test_main_c_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/main.c").is_file()

    def test_startup_c_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/startup.c").is_file()

    def test_vector_table_h_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxemb/vector_table.h").is_file()

    def test_weak_handlers_h_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxemb/weak_handlers.h").is_file()

    def test_command_dispatch_h_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxemb/command_dispatch.h").is_file()

    def test_hal_h_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxemb/hal.h").is_file()

    def test_board_h_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxemb/board.h").is_file()

    def test_sensors_h_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxemb/sensors.h").is_file()

    def test_uart_protocol_h_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxemb/uart_protocol.h").is_file()

    def test_power_modes_h_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/fxemb/power_modes.h").is_file()

    def test_hal_host_c_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/hal/hal_host.c").is_file()

    def test_hal_stm32f4_c_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/hal/hal_stm32f4.c").is_file()

    def test_hal_nrf52_c_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/hal/hal_nrf52.c").is_file()

    def test_board_host_c_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/board/board_host.c").is_file()

    def test_board_stm32f4_c_exists(self) -> None:
        assert (FIXTURE_ROOT / "src/board/board_stm32f4.c").is_file()

    def test_test_runner_py_exists(self) -> None:
        assert (FIXTURE_ROOT / "tests/test_runner.py").is_file()

    def test_unity_h_exists(self) -> None:
        assert (FIXTURE_ROOT / "include/tests/unity.h").is_file()


class TestTrapsEcosystem:
    def test_e01_vector_table(self) -> None:
        startup = (FIXTURE_ROOT / "src/startup.c").read_text(encoding="utf-8")
        assert ".isr_vector" in startup
        assert "Reset_Handler" in startup
        h = (FIXTURE_ROOT / "include/fxemb/vector_table.h").read_text(encoding="utf-8")
        assert "vector_t" in h
        assert "FXEMB_VECTOR_TABLE_SIZE" in h

    def test_e02_weak_symbols(self) -> None:
        h = (FIXTURE_ROOT / "include/fxemb/weak_handlers.h").read_text(encoding="utf-8")
        assert "__attribute__((weak))" in h
        assert "Reset_Handler" in h
        assert "Default_Handler" in h

    def test_e03_command_dispatch(self) -> None:
        c = (FIXTURE_ROOT / "src/command_dispatch.c").read_text(encoding="utf-8")
        assert "cmd_table" in c
        assert "READ" in c
        assert "RESET" in c
        h = (FIXTURE_ROOT / "include/fxemb/command_dispatch.h").read_text(encoding="utf-8")
        assert "cmd_handler_t" in h
        assert "typedef int (*cmd_handler_t)" in h

    def test_e04_linker_script(self) -> None:
        ld = (FIXTURE_ROOT / "firmware.ld").read_text(encoding="utf-8")
        assert ".isr_vector" in ld
        assert ".text" in ld
        assert ".data" in ld
        assert ".bss" in ld
        assert "_estack" in ld
        assert "_sidata" in ld
        assert "_sbss" in ld
        assert "AT>" in ld

    def test_e05_board_ifdef(self) -> None:
        h = (FIXTURE_ROOT / "include/fxemb/board.h").read_text(encoding="utf-8")
        assert "STM32F4_DISCOVERY" in h
        assert "NRF52_DK" in h
        assert "BOARD_HOST" in h
        assert "#ifdef" in h
        assert "#elif" in h
        assert "#error" in h

    def test_e06_mmio_volatile(self) -> None:
        h = (FIXTURE_ROOT / "include/fxemb/hal.h").read_text(encoding="utf-8")
        assert "volatile uint32_t" in h
        assert "FXEMB_GPIOA_ODR" in h
        assert "FXEMB_RCC_AHB1ENR" in h


class TestTrapsPackage:
    def test_p01_race_sensores(self) -> None:
        c = (FIXTURE_ROOT / "src/sensors.c").read_text(encoding="utf-8")
        assert "g_sensor_head" in c
        # Sin mutex en read_all
        assert "fxemb_sensors_read_all" in c

    def test_p02_uart_handler_race(self) -> None:
        c = (FIXTURE_ROOT / "src/uart_protocol.c").read_text(encoding="utf-8")
        assert "g_rx_head" in c
        assert "fxemb_uart_rx_byte" in c

    def test_p03_consumo_stub(self) -> None:
        c = (FIXTURE_ROOT / "src/power_modes.c").read_text(encoding="utf-8")
        assert "fxemb_power_consumption_ua" in c
        # Verificar que el stub retorna 0
        body_start = c.find("int fxemb_power_consumption_ua")
        body = c[body_start:body_start + 200]
        assert "return 0" in body

    def test_p04_sleep_lock_olvidado(self) -> None:
        c = (FIXTURE_ROOT / "src/power_modes.c").read_text(encoding="utf-8")
        assert "fxemb_power_enter" in c
        # trampa: la discusion de "toma un mutex" esta en comentarios pero
        # no hay llamada real. Verificamos que el codigo no invoca
        # funciones de lock. Solo verificamos que el nombre no aparece
        # como una llamada de funcion o tipo.
        assert "pthread_mutex_lock" not in c
        assert "irq_lock" not in c
        assert "taskENTER_CRITICAL" not in c

    def test_p05_sensor_no_inicializado(self) -> None:
        c = (FIXTURE_ROOT / "src/sensors.c").read_text(encoding="utf-8")
        assert "fxemb_sensors_read" in c
        # trampa: el comentario documenta que read cae en basura sin check.
        assert "trampa paquete P05" in c
        # read_all si chequea inicializacion
        assert "g_sensor_initialized" in c

    def test_p06_weak_handler_loop(self) -> None:
        c = (FIXTURE_ROOT / "src/startup.c").read_text(encoding="utf-8")
        assert "Default_Handler" in c
        # Busca la definicion
        def_start = c.find("Default_Handler(void)")
        if def_start == -1:
            def_start = c.find("void Default_Handler")
        assert def_start != -1
        # Que tenga while(1)
        body_start = c.find("{", def_start)
        body_end = c.find("}", body_start)
        body = c[body_start:body_end]
        assert "while (1)" in body


class TestTrapsSuperficial:
    def test_s01_dead_legacy_helper(self) -> None:
        c = (FIXTURE_ROOT / "src/legacy_helpers.c").read_text(encoding="utf-8")
        assert "legacy_uart_send_byte" in c
        assert "legacy_crc16" in c

    def test_s02_unused_macro(self) -> None:
        h = (FIXTURE_ROOT / "include/fxemb/deprecated_macros.h").read_text(encoding="utf-8")
        assert "LEGACY_DELAY" in h
        assert "LEGACY_NOP" in h
        assert "LEGACY_BARRIER" in h
        # Trampa S02: no debe tener marca de deprecation
        assert "__attribute__((deprecated))" not in h

    def test_s03_commented_out_code(self) -> None:
        c = (FIXTURE_ROOT / "src/sensors.c").read_text(encoding="utf-8")
        assert "TODO: soporte para DMA" in c
        # Que haya al menos 4 lineas con //
        comment_count = c.count("//")
        assert comment_count >= 4


class TestManifest:
    def test_manifest_file_exists(self) -> None:
        assert (FIXTURE_ROOT / "manifest.yml").is_file()

    def test_manifest_name_is_fx_c_embedded(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "name: fx-c-embedded" in text

    def test_manifest_requires_linux_macos(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "- linux" in text
        assert "- macos" in text

    def test_manifest_test_cmd_starts_with_make(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "test_cmd: make test" in text

    def test_manifest_container_enabled(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "enabled: true" in text

    def test_manifest_image_tag_starts_with_npr(self) -> None:
        text = (FIXTURE_ROOT / "manifest.yml").read_text(encoding="utf-8")
        assert "image_tag: npr-fx-c-embedded" in text
