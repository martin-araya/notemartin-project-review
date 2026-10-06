"""Catalogo de errores de la CLI `npr`.

Codigos estables NPR-Exxx con mensaje en espanol, causa y accion sugerida.
"""
from __future__ import annotations

ERRORS = {
    "NPR-E101": {
        "msg": "no se pudo resolver SKILL_DIR",
        "causa": "ninguna ruta candidata contiene scripts/.npr-marker",
        "accion": "verifica la instalacion o usa --skill-dir para apuntar a la carpeta de la skill",
    },
    "NPR-E102": {
        "msg": "subcomando desconocido",
        "causa": "el comando solicitado no esta registrado",
        "accion": "ejecuta 'npr --help' para ver los subcomandos disponibles",
    },
    "NPR-E103": {
        "msg": "argumento invalido",
        "causa": "el valor pasado no cumple el tipo o dominio esperado",
        "accion": "revisa la sintaxis con 'npr <comando> --help'",
    },
    "NPR-E104": {
        "msg": "workspace inexistente",
        "causa": "no hay state/state.json en la carpeta de analisis",
        "accion": "ejecuta 'npr init <repo>' primero",
    },
    "NPR-E105": {
        "msg": "workspace ya inicializado",
        "causa": "state/state.json existe y no se paso --force",
        "accion": "usa --force para reescribir o ejecuta otros comandos",
    },
    "NPR-E106": {
        "msg": "state.json corrupto",
        "causa": "el archivo no valida contra el esquema state",
        "accion": "borrar state/state.json y ejecutar 'npr init' de nuevo",
    },
    "NPR-E107": {
        "msg": "defaults.json no se pudo cargar",
        "causa": "el archivo config/defaults.json falta o no es JSON valido",
        "accion": "reinstala la skill o restaura config/defaults.json desde el repo",
    },
    "NPR-E108": {
        "msg": "state/config.json malformado",
        "causa": "el archivo no es JSON valido",
        "accion": "corrige state/config.json o borralo para regenerarlo",
    },
    "NPR-E109": {
        "msg": "--config apunta a archivo inexistente o ilegible",
        "causa": "el path no existe, no es archivo o no se puede leer",
        "accion": "verifica la ruta y los permisos",
    },
    "NPR-E110": {
        "msg": "sintaxis de --set incorrecta",
        "causa": "se esperaba clave=valor (sin espacios alrededor del =)",
        "accion": "usa --set clave=valor (un solo argumento por par)",
    },
    "NPR-E111": {
        "msg": "no se pudo escribir .git/info/exclude",
        "causa": "permiso denegado o .git no inicializado",
        "accion": "ejecuta dentro de un repo con .git accesible o sin git no se agrega exclude",
    },
    "NPR-E112": {
        "msg": "el repo indicado por --repo no existe",
        "causa": "el path no es un directorio",
        "accion": "pasa una ruta absoluta a un directorio valido",
    },
    "NPR-E113": {
        "msg": "comando no disponible en esta fase",
        "causa": "el subcomando esta registrado pero implementado en una fase futura",
        "accion": "consulta ROADMAP.md para ver en que fase se implementa",
    },
    "NPR-E114": {
        "msg": "error de E/S inesperado al escribir el workspace",
        "causa": "permiso denegado, disco lleno o path invalido",
        "accion": "verifica permisos y espacio en disco",
    },
    "NPR-E115": {
        "msg": "state.json sin campos obligatorios",
        "causa": "el archivo no tiene repo, commit, branch, created_at, skill_version, mode, stage o config",
        "accion": "regenera con 'npr init --force'",
    },
    "NPR-E116": {
        "msg": "repo sin git; HEAD no disponible",
        "causa": "no se ejecuto git rev-parse o no hay .git",
        "accion": "no es un error; el analisis continuara sin SHA de HEAD",
    },
}


def get(code: str) -> dict:
    if code not in ERRORS:
        raise KeyError(f"codigo de error desconocido: {code}")
    return ERRORS[code]


def format_error(code: str, **ctx: object) -> str:
    info = get(code)
    parts = [f"[{code}] {info['msg']}"]
    if ctx:
        rendered = ", ".join(f"{k}={v!r}" for k, v in ctx.items() if v is not None)
        if rendered:
            parts.append(f"detalle: {rendered}")
    parts.append(f"causa: {info['causa']}")
    parts.append(f"accion: {info['accion']}")
    return "\n".join(parts)