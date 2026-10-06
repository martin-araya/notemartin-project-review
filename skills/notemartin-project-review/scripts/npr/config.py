"""Carga y merge de configuracion de la CLI `npr`.

Precedencia (de menor a mayor):
- defaults.json
- state/config.json del workspace
- archivo --config
- argumentos --set

Devuelve (effective_dict, origin_dict) donde origin_dict mapea cada clave
a 'default' | 'workspace' | 'cli_file' | 'cli_set'.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from . import errors_catalog


def _read_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        print(errors_catalog.format_error("NPR-E108", path=str(path), error=str(exc)), file=sys.stderr)
        sys.exit(2)
    except OSError as exc:
        print(errors_catalog.format_error("NPR-E109", path=str(path), error=str(exc)), file=sys.stderr)
        sys.exit(2)


def load_defaults(skill_dir: Path) -> dict:
    path = skill_dir / "config" / "defaults.json"
    if not path.is_file():
        print(errors_catalog.format_error("NPR-E107", path=str(path)), file=sys.stderr)
        sys.exit(2)
    return _read_json(path)


def load_workspace_config(workspace: Path) -> dict:
    path = workspace / "state" / "config.json"
    if not path.is_file():
        return {}
    return _read_json(path)


def load_cli_config(path_str: str | None) -> dict:
    if not path_str:
        return {}
    path = Path(path_str)
    if not path.is_file():
        print(errors_catalog.format_error("NPR-E109", path=str(path)), file=sys.stderr)
        sys.exit(2)
    return _read_json(path)


def _parse_value(raw: str) -> object:
    """Intenta JSON; si falla, devuelve el string tal cual."""
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def apply_set(base: dict, set_args: list[str]) -> tuple[dict, list]:
    """Aplica cada 'clave=valor' sobre `base`. Devuelve (nuevo_dict, claves_modificadas)."""
    modified: list = []
    out = dict(base)
    for pair in set_args or []:
        if "=" not in pair:
            print(errors_catalog.format_error("NPR-E110", set=pair), file=sys.stderr)
            sys.exit(2)
        key, _, value = pair.partition("=")
        key = key.strip()
        if not key:
            print(errors_catalog.format_error("NPR-E110", set=pair), file=sys.stderr)
            sys.exit(2)
        out[key] = _parse_value(value)
        modified.append(key)
    return out, modified


def load_effective(skill_dir: Path, workspace: Path | None, cli_config_path: str | None, set_args: list[str]) -> tuple[dict, dict]:
    """Aplica la precedencia y devuelve (effective, origin)."""
    defaults = load_defaults(skill_dir)
    effective = dict(defaults)
    origin = {k: "default" for k in effective}

    if workspace:
        wc = load_workspace_config(workspace)
        for k, v in wc.items():
            effective[k] = v
            origin[k] = "workspace"

    cli = load_cli_config(cli_config_path)
    for k, v in cli.items():
        effective[k] = v
        origin[k] = "cli_file"

    effective, set_applied = apply_set(effective, set_args)
    for k in set_applied:
        origin[k] = "cli_set"

    return effective, origin


def write_to_state(workspace: Path, effective: dict) -> Path:
    path = workspace / "state" / "config.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(effective, fh, ensure_ascii=False, indent=2, sort_keys=True)
    return path