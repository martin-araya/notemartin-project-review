#!/usr/bin/env python3
"""Harness de ejecucion de tests de los fixtures (F06a2 T4).

Recorre ``dev/fixtures/fx-*/`` y, por cada uno que tenga ``manifest.yml``:

1. Si la plataforma actual no esta en ``requires:``, marca el fixture como
   ``skipped (requires: ...)`` y sigue.
2. Si el manifest define ``container:`` y la opcion ``--container`` esta activa,
   intenta construir la imagen Docker y correr el ``test_cmd`` dentro.
3. Si no, ejecuta ``test_cmd`` directamente con ``subprocess.run`` desde la
   carpeta del fixture (timeout 600 s por defecto).

CLI::

    python dev/tools/run_fixture_tests.py [--fixture fx-...] [--all]
        [--container] [--platform auto|linux|macos|windows] [--report archivo.json]

Codigos de salida:
- 0 todos los ejecutables pasaron (los skipped no son falla)
- 1 error de uso
- 2 alguno fallo
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = REPO_ROOT / "dev" / "fixtures"

# Asegura que ``import dev.tools...`` funcione cuando se ejecuta directo.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _yaml_load(text: str) -> Any:
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ImportError:
        from dev.tools.check_ground_truth import _minimal_yaml_load  # type: ignore

        return _minimal_yaml_load(text)


def _load_manifest(fixture_dir: Path) -> Optional[Dict[str, Any]]:
    manifest_path = fixture_dir / "manifest.yml"
    if not manifest_path.is_file():
        return None
    try:
        data = _yaml_load(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensivo
        return {"_error": f"manifest no parseable: {exc}"}
    if not isinstance(data, dict):
        return {"_error": "manifest no es un mapa"}
    return data


def _discover_fixtures(only: Optional[str]) -> List[Path]:
    out: List[Path] = []
    if not FIXTURES_DIR.is_dir():
        return out
    for p in sorted(FIXTURES_DIR.iterdir()):
        if not p.is_dir():
            continue
        if p.name.startswith("_") or p.name.startswith("."):
            continue
        if only and p.name != only:
            continue
        out.append(p)
    return out


def _current_platform() -> str:
    s = sys.platform
    if s.startswith("linux"):
        return "linux"
    if s.startswith("darwin"):
        return "macos"
    if s.startswith(("win32", "cygwin")):
        return "windows"
    return s


def _supports_platform(manifest: Dict[str, Any], current: str) -> bool:
    if current == "auto":
        current = _current_platform()
    requires = manifest.get("requires") or ["linux", "macos", "windows"]
    if not isinstance(requires, list):
        requires = [requires]
    return current in requires


def _run_subprocess(cmd: List[str], cwd: Path, timeout: float) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", (exc.stderr or "") + f"\n[timeout after {timeout}s]"
    except FileNotFoundError as exc:
        return 127, "", f"command not found: {exc}"


def _run_in_container(
    manifest: Dict[str, Any], fixture_dir: Path, timeout: float
) -> Tuple[int, str, str, str]:
    container = manifest.get("container") or {}
    dockerfile = container.get("dockerfile") or "Dockerfile.test"
    image_tag = container.get("image_tag") or f"npr-fx-{fixture_dir.name}"
    dockerfile_path = fixture_dir / dockerfile
    if not dockerfile_path.is_file():
        return 2, "", "", f"Dockerfile no encontrado: {dockerfile_path}"
    if shutil.which("docker") is None:
        return 0, "", "", "skipped (no docker)"
    test_cmd = (manifest.get("test_cmd") or "make test").split()
    build_rc, build_out, build_err = _run_subprocess(
        ["docker", "build", "-f", str(dockerfile_path), "-t", image_tag, str(fixture_dir)],
        cwd=fixture_dir,
        timeout=timeout,
    )
    if build_rc != 0:
        return build_rc, build_out, build_err, f"docker build fallo ({build_rc})"
    run_rc, run_out, run_err = _run_subprocess(
        ["docker", "run", "--rm", image_tag, *test_cmd],
        cwd=fixture_dir,
        timeout=timeout,
    )
    return run_rc, run_out, run_err, "ran in container"


def _run_one(
    fixture_dir: Path, use_container: bool, platform_arg: str, timeout: float
) -> Dict[str, Any]:
    manifest = _load_manifest(fixture_dir)
    name = fixture_dir.name
    if manifest is None:
        return {"fixture": name, "status": "error", "reason": "no manifest"}
    if "_error" in manifest:
        return {"fixture": name, "status": "error", "reason": manifest["_error"]}
    if not _supports_platform(manifest, platform_arg):
        return {
            "fixture": name,
            "status": "skipped",
            "reason": f"requires: {manifest.get('requires')}",
        }
    test_cmd_str = manifest.get("test_cmd") or "make test"
    if not isinstance(test_cmd_str, str):
        test_cmd_str = str(test_cmd_str)
    if use_container:
        rc, out, err, note = _run_in_container(manifest, fixture_dir, timeout)
        if note.startswith("skipped"):
            return {
                "fixture": name,
                "status": "skipped",
                "reason": note,
                "command": test_cmd_str,
            }
        return {
            "fixture": name,
            "status": "passed" if rc == 0 else "failed",
            "returncode": rc,
            "stdout_tail": out[-500:],
            "stderr_tail": err[-500:],
            "note": note,
            "command": test_cmd_str,
        }
    test_cmd = test_cmd_str.split()
    rc, out, err = _run_subprocess(test_cmd, fixture_dir, timeout)
    return {
        "fixture": name,
        "status": "passed" if rc == 0 else "failed",
        "returncode": rc,
        "stdout_tail": out[-500:],
        "stderr_tail": err[-500:],
        "command": test_cmd_str,
    }


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ejecuta los tests de los fixtures")
    parser.add_argument("--fixture", help="Nombre del fixture (ej. fx-python-cli)")
    parser.add_argument("--all", action="store_true", help="Ejecuta todos los fixtures")
    parser.add_argument("--container", action="store_true", help="Intentar usar Docker")
    parser.add_argument(
        "--platform",
        default="auto",
        choices=["auto", "linux", "macos", "windows"],
        help="Plataforma actual",
    )
    parser.add_argument("--report", type=Path, help="Archivo JSON de reporte")
    parser.add_argument("--timeout", type=float, default=600.0, help="Timeout en segundos")
    args = parser.parse_args(argv)

    if not args.all and not args.fixture:
        print("ERROR: especifique --fixture o --all", file=sys.stderr)
        return 1

    only = args.fixture
    fixtures = _discover_fixtures(only)
    if not fixtures:
        print(f"ERROR: no se encontraron fixtures (filter={only!r})", file=sys.stderr)
        return 1

    results: List[Dict[str, Any]] = []
    for fx in fixtures:
        result = _run_one(fx, args.container, args.platform, args.timeout)
        results.append(result)
        status = result["status"]
        cmd = result.get("command", "")
        reason = result.get("reason", "")
        line = f"  {fx.name}: {status}"
        if cmd:
            line += f"  ({cmd})"
        if reason:
            line += f"  -- {reason}"
        if status == "failed":
            line += f"  rc={result.get('returncode')}"
        print(line)

    # Resumen
    counts = {"passed": 0, "failed": 0, "skipped": 0, "error": 0}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("")
    print(
        f"Resumen: {counts.get('passed', 0)} passed, "
        f"{counts.get('failed', 0)} failed, "
        f"{counts.get('skipped', 0)} skipped, "
        f"{counts.get('error', 0)} error"
    )

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(
                {
                    "platform": _current_platform(),
                    "results": results,
                    "summary": counts,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    # Salida: 0 si no hay failed ni error, 2 si hay.
    if counts.get("failed", 0) > 0 or counts.get("error", 0) > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
