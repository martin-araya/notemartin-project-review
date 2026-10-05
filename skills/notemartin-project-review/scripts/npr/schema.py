"""Validador JSON Schema (subconjunto) en stdlib puro.

Soporta las 10 keywords que el roadmap de F04 fija:
- type, required, properties, additionalProperties, items, enum,
  pattern, minimum, maximum, $ref (local #/definitions/X).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMAS_DIR = SKILL_ROOT / "schemas"


class SchemaError(ValueError):
    """Levantada por `check` cuando la instancia no cumple el esquema."""


def load_schema(name: str) -> dict:
    """Carga `schemas/<name>.json` relativo a la raíz de la skill."""
    path = SCHEMAS_DIR / f"{name}.json"
    if not path.is_file():
        raise FileNotFoundError(f"no existe esquema: {path}")
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _type_match(value: Any, expected: Any) -> bool:
    if isinstance(expected, list):
        return any(_type_match(value, t) for t in expected)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, _JSON_TYPE_MAP[expected])


_JSON_TYPE_MAP = {
    "string": str,
    "boolean": bool,
    "array": list,
    "object": dict,
    "null": type(None),
}


def _resolve_ref(ref: str, schema: dict, definitions: dict | None) -> dict:
    if not ref.startswith("#/definitions/"):
        raise SchemaError(f"$ref no soportado (solo local): {ref}")
    key = ref[len("#/definitions/"):]
    defs = definitions if definitions is not None else schema.get("definitions", {})
    if key not in defs:
        raise SchemaError(f"$ref apunta a definicion inexistente: {ref}")
    return defs[key]


def validate(instance: Any, schema: dict, path: str = "$", definitions: dict | None = None) -> list:
    """Devuelve la lista de mensajes de error; vacia si todo OK."""
    errors: list = []
    definitions = definitions if definitions is not None else schema.get("definitions", {})

    if "$ref" in schema:
        return validate(instance, _resolve_ref(schema["$ref"], schema, definitions), path, definitions)

    if "type" in schema:
        if not _type_match(instance, schema["type"]):
            errors.append(f"{path}: se esperaba type={schema['type']}, se obtuvo {type(instance).__name__}")
            return errors

    if "enum" in schema:
        if instance not in schema["enum"]:
            errors.append(f"{path}: valor {instance!r} no esta en enum {schema['enum']}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: valor {instance} menor que minimum={schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: valor {instance} mayor que maximum={schema['maximum']}")

    if "pattern" in schema and isinstance(instance, str):
        if not re.search(schema["pattern"], instance):
            errors.append(f"{path}: valor {instance!r} no cumple pattern={schema['pattern']!r}")

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}.{req}: campo requerido ausente")

        for key, sub in schema.get("properties", {}).items():
            if key in instance:
                errors.extend(validate(instance[key], sub, f"{path}.{key}", definitions))

        if schema.get("additionalProperties") is False:
            allowed = set(schema.get("properties", {}).keys())
            extra = [k for k in instance.keys() if k not in allowed]
            for k in extra:
                errors.append(f"{path}.{k}: campo no permitido (additionalProperties=false)")

    if isinstance(instance, list) and "items" in schema:
        for i, item in enumerate(instance):
            errors.extend(validate(item, schema["items"], f"{path}[{i}]", definitions))

    return errors


def check(instance: Any, schema: dict) -> None:
    """Lanza SchemaError con todos los errores si la instancia no cumple."""
    errors = validate(instance, schema)
    if errors:
        raise SchemaError("; ".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida un JSON contra un esquema de la skill")
    parser.add_argument("schema_name", help="Nombre del esquema (sin .json)")
    parser.add_argument("instance", type=Path, help="Archivo JSON a validar")
    args = parser.parse_args()

    schema = load_schema(args.schema_name)
    instance = json.loads(args.instance.read_text(encoding="utf-8"))
    errors = validate(instance, schema)
    if errors:
        print("FALLO", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 2
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())