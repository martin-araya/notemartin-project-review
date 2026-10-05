"""Tests para `scripts/npr/schema.py` y los 19 esquemas del workspace (F04)."""
import ast
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
SKILL = ROOT / "skills" / "notemartin-project-review"
sys.path.insert(0, str(SKILL / "scripts"))

from npr.schema import load_schema, validate, check, SchemaError  # noqa: E402

SCHEMA_NAMES = [
    "state", "inventory-entry", "classification", "stack", "dependency",
    "edge", "symbol", "entrypoint", "surface", "config-item",
    "llm-artifact", "git-stats", "wu", "ledger-entry", "claim-check",
    "open-question", "feature", "flow", "knowledge",
]
EXAMPLES_DIR = ROOT / "dev" / "tests" / "schema_examples"


def _load(name: str, kind: str) -> dict:
    return json.loads((EXAMPLES_DIR / f"{name}-{kind}.json").read_text(encoding="utf-8"))


# ---- 01..19: cada esquema, ejemplo valido ------------------------------
@pytest.mark.parametrize("name", SCHEMA_NAMES)
def test_valid_example_passes(name):
    schema = load_schema(name)
    instance = _load(name, "valid")
    errors = validate(instance, schema)
    assert errors == [], f"{name}-valid no valida: {errors}"


# ---- 20..38: cada esquema, ejemplo invalido -----------------------------
@pytest.mark.parametrize("name", SCHEMA_NAMES)
def test_invalid_example_fails_with_field_name(name):
    schema = load_schema(name)
    instance = _load(name, "invalid")
    errors = validate(instance, schema)
    assert errors, f"{name}-invalid deberia fallar pero valido OK"
    joined = " | ".join(errors)
    assert any(re.search(r"\$[A-Za-z_.[\]]+", e) for e in errors), (
        f"errores no mencionan el path del campo: {errors}"
    )
    assert len(joined) > 0


# ---- 39: stdlib-only ----------------------------------------------------
def test_39_stdlib_only():
    src = (SKILL / "scripts" / "npr" / "schema.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    stdlib = {
        "json", "re", "sys", "pathlib", "typing", "argparse", "dataclasses",
        "enum", "__future__",
    }
    # los modulos locales se permiten
    imports = {i.split(".")[0] for i in imports}
    extras = imports - stdlib
    assert not extras, f"imports fuera de stdlib: {extras}"


# ---- 40: additionalProperties ------------------------------------------
def test_40_additional_properties_rejected():
    schema = load_schema("state")
    inst = json.loads((EXAMPLES_DIR / "state-valid.json").read_text(encoding="utf-8"))
    inst["extra_field"] = "boom"
    errors = validate(inst, schema)
    assert any("extra_field" in e for e in errors)


# ---- 41: enum ----------------------------------------------------------
def test_41_enum_rejects_outside_value():
    schema = load_schema("classification")
    inst = {"path": "src/x.py", "category": "code", "policy": "magic", "reason": "x"}
    errors = validate(inst, schema)
    assert any("policy" in e and "magic" in e for e in errors)


# ---- 42: pattern -------------------------------------------------------
def test_42_pattern_accepts_and_rejects():
    schema = load_schema("wu")
    inst_ok = {"id": "WU-001", "files": [], "priority": 1, "wave": 1}
    inst_bad = {"id": "wu-001", "files": [], "priority": 1, "wave": 1}
    assert validate(inst_ok, schema) == []
    assert any("WU-" in e for e in validate(inst_bad, schema))


# ---- 43: minimum / maximum ---------------------------------------------
def test_43_minimum_maximum():
    schema = load_schema("git-stats")
    inst_low = {"commits_total": -1, "first_commit": "abc1234", "last_commit": "def5678", "contributors": 0}
    inst_ok = {"commits_total": 0, "first_commit": "abc1234", "last_commit": "def5678", "contributors": 0}
    assert any("minimum" in e for e in validate(inst_low, schema))
    assert validate(inst_ok, schema) == []


# ---- 44: $ref local -----------------------------------------------------
def test_44_local_ref_resolves():
    schema = load_schema("feature")
    inst = {
        "id": "FEAT-001",
        "name": "x",
        "user_description": "x",
        "entrypoints": [],
        "modules": [],
        "flows": [],
        "config": [{"key": "X", "kind": "env", "source": "src/x.py"}],
        "status": "draft",
    }
    assert validate(inst, schema) == []


def test_44b_ref_to_missing_definition_raises():
    schema = {"$ref": "#/definitions/missing"}
    with pytest.raises(SchemaError):
        validate({}, schema)


# ---- 45: integer rechaza bool y float -----------------------------------
def test_45_integer_rejects_bool_and_float():
    schema = load_schema("git-stats")
    inst_bool = {"commits_total": True, "first_commit": "abc1234", "last_commit": "def5678", "contributors": 0}
    inst_float = {"commits_total": 1.5, "first_commit": "abc1234", "last_commit": "def5678", "contributors": 0}
    assert any("type=integer" in e for e in validate(inst_bool, schema))
    assert any("type=integer" in e for e in validate(inst_float, schema))


# ---- 46: required reporta el campo -------------------------------------
def test_46_required_reports_missing_field():
    schema = load_schema("state")
    inst = {"repo": "/x", "commit": "abc1234", "branch": "main"}
    errors = validate(inst, schema)
    missing = [f for f in ("created_at", "skill_version", "mode", "stage", "config")
               if any(f in e for e in errors)]
    assert len(missing) >= 3


# ---- 47: CLI -----------------------------------------------------------
def test_47_cli_valid(tmp_path):
    inst = _load("state", "valid")
    p = tmp_path / "inst.json"
    p.write_text(json.dumps(inst), encoding="utf-8")
    from npr.schema import main as schema_main
    saved = sys.argv
    sys.argv = ["schema.py", "state", str(p)]
    try:
        rc = schema_main()
    finally:
        sys.argv = saved
    assert rc == 0


def test_48_cli_invalid(tmp_path):
    inst = _load("state", "invalid")
    p = tmp_path / "inst.json"
    p.write_text(json.dumps(inst), encoding="utf-8")
    from npr.schema import main as schema_main
    saved = sys.argv
    sys.argv = ["schema.py", "state", str(p)]
    try:
        rc = schema_main()
    finally:
        sys.argv = saved
    assert rc == 2


# ---- 49: cada propiedad lleva description -------------------------------
def test_49_each_schema_has_descriptions_on_all_properties():
    for name in SCHEMA_NAMES:
        schema = load_schema(name)
        props = schema.get("properties", {})
        for prop_name, prop_schema in props.items():
            assert "description" in prop_schema, (
                f"{name}.properties.{prop_name} sin description"
            )
            assert isinstance(prop_schema["description"], str)
            assert len(prop_schema["description"]) > 0


# ---- 50: $ref no soportado fuera de mas de schema ----------------------
def test_50_external_ref_rejected():
    schema = {"$ref": "https://example.com/schema.json"}
    with pytest.raises(SchemaError):
        validate({}, schema)


# ---- 51: check() lanza SchemaError --------------------------------------
def test_51_check_raises():
    schema = load_schema("state")
    with pytest.raises(SchemaError):
        check({}, schema)


def test_52_check_passes():
    schema = load_schema("state")
    inst = _load("state", "valid")
    check(inst, schema)


# ---- 53: type=list dentro de properties ---------------------------------
def test_53_type_as_list_accepts_multiple():
    schema = {"type": "object", "properties": {"x": {"type": ["string", "null"]}}}
    assert validate({"x": "a"}, schema) == []
    assert validate({"x": None}, schema) == []


# ---- 54: enum en arrays -------------------------------------------------
def test_54_enum_in_array_items():
    schema = {
        "type": "object",
        "properties": {
            "tags": {"type": "array", "items": {"type": "string", "enum": ["a", "b", "c"]}}
        }
    }
    assert validate({"tags": ["a", "b"]}, schema) == []
    assert any("d" in e for e in validate({"tags": ["a", "d"]}, schema))