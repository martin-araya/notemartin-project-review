#!/usr/bin/env python3
"""Generador de la matriz de cobertura de fixtures (F06a2 T7).

Carga ``dev/fixtures/target_matrix.yml`` y compara contra el conjunto real de
fixtures en ``dev/fixtures/``. Para cada fixture hace un descubrimiento ligero
(extensiones, manifiestos de dependencias) y determina que entradas de la matriz
cubre.

CLI::

    python dev/tools/fixtures_matrix.py [--check] [--out <dir>]

Genera ``dev/fixtures/MATRIX.md`` con la tabla legible. Con ``--check``, sale
con codigo 2 si algun item del ``target_matrix.yml`` no esta cubierto (durante
F06a2..F06e esto se permite; el gate total se cierra en F06f).

Codigos de salida:
- 0 OK (cobertura completa o solo advertencia)
- 1 error de uso
- 2 cobertura incompleta (solo con --check)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = REPO_ROOT / "dev" / "fixtures"
TARGET_PATH = FIXTURES_DIR / "target_matrix.yml"
MATRIX_OUT = FIXTURES_DIR / "MATRIX.md"

# Asegura que ``import dev.tools...`` funcione cuando el script se ejecuta directo.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Extensiones -> lenguajes que cubren. ``.ts`` cubre tanto ``typescript``
# como ``javascript`` porque TypeScript compila a JS y un proyecto TS es
# un superset del ecosistema JS.
EXT_LANG: Dict[str, Set[str]] = {
    ".py": {"python"}, ".pyi": {"python"}, ".pyw": {"python"},
    ".js": {"javascript"}, ".mjs": {"javascript"}, ".cjs": {"javascript"},
    ".jsx": {"javascript"},
    ".ts": {"typescript", "javascript"}, ".tsx": {"typescript", "javascript"},
    ".java": {"java"},
    ".kt": {"kotlin"}, ".kts": {"kotlin"},
    ".go": {"go"},
    ".rs": {"rust"},
    ".sh": {"shell"}, ".bash": {"shell"}, ".zsh": {"shell"},
    ".dart": {"dart"},
    ".swift": {"swift"},
    ".cs": {"csharp"},
    ".rb": {"ruby"},
    ".ex": {"elixir"}, ".exs": {"elixir"},
}

# Manifiestos -> sistemas de build
MANIFEST_BUILD: Dict[str, Set[str]] = {
    "pyproject.toml": {"pyproject"},
    "pnpm-lock.yaml": {"pnpm"},
    "pnpm-workspace.yaml": {"pnpm"},
    "pom.xml": {"maven"},
    "build.gradle": {"gradle"}, "build.gradle.kts": {"gradle"},
    "Cargo.toml": {"cargo"},
    "go.mod": {"go-modules"},
    "Makefile": {"make"},
    "Dockerfile": {"docker"},
    "gulpfile.js": {"gulp"},
}

# Archivos clave de frameworks
FRAMEWORK_FILES: Dict[str, Set[str]] = {
    "angular.json": {"angular", "javascript"},
    "nest-cli.json": {"node-express"},
    "micronaut-cli.yml": {"micronaut"},
    "settings.gradle": {"gradle"}, "settings.gradle.kts": {"gradle"},
    ".vscode/extension.js": {"vscode-extension"},
    # electron: lo detectamos por package.json con dependencia electron
    "nx.json": {"pnpm-monorepo"},
    "turbo.json": {"pnpm-monorepo"},
    "pnpm-workspace.yaml": {"pnpm-monorepo"},
    # ``cargo`` y ``go-modules`` son a la vez build_systems y frameworks;
    # los cubrimos en build_systems desde MANIFEST_BUILD y los reusamos aqui
    # para que el eje frameworks los reporte como cubiertos.
    "Cargo.toml": {"cargo"},
    "go.mod": {"go-modules"},
    # Frameworks React SPA: cualquier `vite.config.ts` indica Vite; ``react``
    # como dep en package.json indica React. Tambien capturamos ``vite`` desde
    # el mismo archivo.
    "vite.config.ts": {"react-spa", "vite"},
    # Nuxt 3: la presencia de nuxt.config.ts indica una app Nuxt.
    "nuxt.config.ts": {"nuxt"},
    # SvelteKit: la presencia de svelte.config.js indica una app SvelteKit.
    "svelte.config.js": {"sveltekit"},
}

# Markers adicionales en package.json que indican el framework aunque el
# archivo no este presente (util para shims de VS Code, etc.).
PACKAGE_JSON_MARKERS: Dict[str, Set[str]] = {
    "contributes": {"vscode-extension"},
    # ``react`` como dep de runtime: SPA React (vite/react-spa).
    # ``vue``: SPA Vue. ``next``: Next.js. ``svelte``: SvelteKit.
    # ``@angular/core``: Angular standalone (ademas del angular.json).
    # ``@reduxjs/toolkit``: indicador de Redux Toolkit (comun en React SPA).
    "react": {"react-spa"},
    "vue": {"vue-spa"},
    "next": {"nextjs"},
    "svelte": {"svelte-spa"},
    "@reduxjs/toolkit": {"react-spa"},
    # Next.js App Router: ``next`` ya cubre nextjs; anadimos next-auth para
    # distinguir Next.js fullstack de SPA.
    "next-auth": {"nextjs"},
    # jQuery como dep de runtime: frontend legacy con jQuery (F06i).
    "jquery": {"jquery"},
    # Nuxt 3 como dep de runtime: app fullstack con auto-imports (F06j).
    "nuxt": {"nuxt"},
    # SvelteKit: la dep ``@sveltejs/kit`` indica SvelteKit (F06k).
    "@sveltejs/kit": {"sveltekit"},
}

# Dependencias que definen el ecosistema por si mismas.
DEPENDENCY_ECOSYSTEM: Dict[str, Set[str]] = {
    "@prisma/client": {"prisma"},
    "prisma": {"prisma"},
}

# Tipos de archivo
FILE_KIND_BY_EXT: Dict[str, Set[str]] = {
    ".min.js": {"minified-js"},
    ".bundle.js": {"minified-js", "bundle-without-sourcemap"},
    ".min.css": {"minified-js"},
    ".map": {"bundle-with-sourcemap"},
    ".asar": {"asar"},
    ".pyc": {"pyc"}, ".pyo": {"pyc"},
    ".ipynb": {"notebook-ipynb"},
    ".xml": {"xml-declarative"}, ".xaml": {"xml-declarative"},
    ".ui": {"xml-declarative"}, ".adf": {"xml-declarative"},
    ".unity": {"yaml-scene"}, ".tscn": {"yaml-scene"},
    ".helm.yaml": {"yaml-scene"},
}

CONTAINER_EXTS: Set[str] = {
    ".asar", ".jar", ".zip", ".apk", ".vsix", ".whl", ".egg",
}


def _yaml_load(text: str) -> Any:
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ImportError:
        from dev.tools.check_ground_truth import _minimal_yaml_load  # type: ignore
        return _minimal_yaml_load(text)


def _load_target() -> dict:
    if not TARGET_PATH.is_file():
        raise FileNotFoundError(f"falta {TARGET_PATH}")
    return _yaml_load(TARGET_PATH.read_text(encoding="utf-8"))


def _fixture_axes(fixture_dir: Path) -> Dict[str, Set[str]]:
    """Descubre ejes cubiertos por un fixture mediante extensiones y manifiestos."""
    covered: Dict[str, Set[str]] = {
        "languages": set(),
        "frameworks": set(),
        "build_systems": set(),
        "file_kinds": set(),
        "containers": set(),
    }
    if not fixture_dir.is_dir():
        return covered

    # Manifiestos en la raiz o recursivos (importante para fixtures con src/ subdirs).
    for manifest, builds in MANIFEST_BUILD.items():
        if (fixture_dir / manifest).is_file():
            covered["build_systems"] |= builds
        elif any(fixture_dir.rglob(manifest)):
            covered["build_systems"] |= builds

    # Archivos clave de frameworks en la raiz o un nivel (o recursivo si
    # es un monorepo: angular.json vive en apps/web/).
    for fname, frameworks in FRAMEWORK_FILES.items():
        if (fixture_dir / fname).is_file() or (fixture_dir.parent / fname).is_file():
            covered["frameworks"] |= frameworks
        # Para monorepos: buscar en cualquier subdirectorio.
        if any(fixture_dir.rglob(fname)):
            covered["frameworks"] |= frameworks

    # package.json -> electron y node-express y pnpm-monorepo
    pkg = fixture_dir / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}
        deps = {}
        deps.update(data.get("dependencies", {}) or {})
        deps.update(data.get("devDependencies", {}) or {})
        if "electron" in deps:
            covered["frameworks"].add("electron")
        if "express" in deps or "@nestjs/core" in deps:
            covered["frameworks"].add("node-express")
        if (fixture_dir / "pnpm-workspace.yaml").is_file():
            covered["frameworks"].add("pnpm-monorepo")
        # Markers adicionales (contributes -> vscode-extension).
        for marker, frameworks in PACKAGE_JSON_MARKERS.items():
            if marker in data:
                covered["frameworks"] |= frameworks
        # Dependencias de runtime que implican frameworks SPA: el marker del dict
        # puede ser tambien una dep de dependencies/devDependencies.
        for marker, frameworks in PACKAGE_JSON_MARKERS.items():
            if marker in deps:
                covered["frameworks"] |= frameworks
        # Ecosistemas definidos solo por su dep (no son frameworks SPA).
        for marker, ecosystems in DEPENDENCY_ECOSYSTEM.items():
            if marker in deps:
                covered["frameworks"] |= ecosystems

    # Detectar Micronaut via el plugin en build.gradle.kts.
    gradle_kts = fixture_dir / "build.gradle.kts"
    if gradle_kts.is_file():
        try:
            content = gradle_kts.read_text(encoding="utf-8")
            if "io.micronaut.application" in content or "io.micronaut" in content:
                covered["frameworks"].add("micronaut")
        except (OSError, UnicodeDecodeError):
            pass

    # Recorrido del arbol para extensiones
    for path in fixture_dir.rglob("*"):
        if not path.is_file():
            continue
        if any(part.startswith(".") and part not in (".vscode",) for part in path.parts):
            continue
        # ``artifacts/`` se inspecciona para detectar containers y binarios
        # aunque esten generados por el Dockerfile.test.
        if any(p in path.parts for p in ("node_modules", "__pycache__", "target", "build", "dist", ".git")):
            continue
        ext = path.suffix.lower()
        covered["languages"] |= EXT_LANG.get(ext, set())
        for specific, kinds in FILE_KIND_BY_EXT.items():
            if path.name.endswith(specific) or ext == specific:
                covered["file_kinds"] |= kinds
        if ext in CONTAINER_EXTS:
            covered["containers"].add(ext.lstrip("."))

    # ``artifacts/`` aporta containers y file_kinds aunque sea generado.
    artifacts_dir = fixture_dir / "artifacts"
    if artifacts_dir.is_dir():
        for path in artifacts_dir.rglob("*"):
            if not path.is_file():
                continue
            ext = path.suffix.lower()
            # Sin ``source-text`` desde artifacts/ (es generado).
            for specific, kinds in FILE_KIND_BY_EXT.items():
                if path.name.endswith(specific) or ext == specific:
                    covered["file_kinds"] |= kinds
            if ext in CONTAINER_EXTS:
                covered["containers"].add(ext.lstrip("."))
            # Binarios sin extension declarada por `containers` cuentan como ``binary``.
            stem = path.stem.lower()
            if (
                path.stat().st_size > 1024
                and ext not in CONTAINER_EXTS
                and not ext
                and any(stem.endswith(s) for s in ("bin", "exe"))
            ) or ext in (".elf", ".macho"):
                covered["file_kinds"].add("binary")

    # ``manifests/`` (convention usada por fx-minified) declara los artefactos
    # aunque no esten generados localmente. Inspeccionamos los nombres de
    # archivo JSON para derivar containers/file_kinds.
    manifests_dir = fixture_dir / "manifests"
    if manifests_dir.is_dir():
        import json as _json
        for path in manifests_dir.rglob("*.json*"):
            if not path.is_file():
                continue
            name = path.name.lower()
            for ext in CONTAINER_EXTS:
                if ext in name:
                    covered["containers"].add(ext.lstrip("."))
            for marker in ("min.js", "minified", "bundle.js", "sourcemap",
                          "tree-shak", "asar", "pyc", ".jar", "binary"):
                if marker in name:
                    if marker == "min":
                        covered["file_kinds"].add("minified-js")
                    elif marker in ("bundle.js", "sourcemap"):
                        covered["file_kinds"].add("bundle-with-sourcemap")
                    elif marker == "asar":
                        covered["file_kinds"].add("asar")
                    elif marker == "pyc":
                        covered["file_kinds"].add("pyc")
            try:
                data = _json.loads(path.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                continue
            artifact = (data.get("artifact") or "").lower() if isinstance(data, dict) else ""
            for marker in (".jar", ".asar", ".pyc", ".js.map", ".min.js", ".bundle.js"):
                if artifact.endswith(marker):
                    covered["file_kinds"].add(
                        "bundle-with-sourcemap" if marker == ".js.map" else
                        "minified-js" if marker in (".min.js", ".bundle.js") else
                        "asar" if marker == ".asar" else
                        "pyc" if marker == ".pyc" else
                        "jar" if marker == ".jar" else marker.lstrip(".")
                    )
                    if marker in CONTAINER_EXTS or marker in (".jar", ".asar", ".zip", ".apk",
                                                              ".vsix", ".whl", ".egg"):
                        covered["containers"].add(marker.lstrip("."))

    # Si el fixture tiene archivos de codigo fuente, implica ``source-text``.
    if covered["languages"]:
        covered["file_kinds"].add("source-text")

    return covered


def _discover_fixtures() -> List[Path]:
    """Lista los fixtures (subdirs de FIXTURES_DIR que no empiezan con ``_`` o ``.``)."""
    out: List[Path] = []
    if not FIXTURES_DIR.is_dir():
        return out
    for p in sorted(FIXTURES_DIR.iterdir()):
        if not p.is_dir():
            continue
        if p.name.startswith("_") or p.name.startswith("."):
            continue
        out.append(p)
    return out


def _format_md(
    target: dict,
    per_fixture: List[tuple],
    aggregate: Dict[str, Set[str]],
) -> str:
    axes = target.get("axes", {})
    lines: List[str] = []
    lines.append("# Matriz de cobertura de fixtures")
    lines.append("")
    lines.append(
        "Generada por `dev/tools/fixtures_matrix.py` a partir de "
        "`dev/fixtures/target_matrix.yml` y de los fixtures presentes en "
        "`dev/fixtures/`."
    )
    lines.append("")
    lines.append("## Fixtures detectados")
    if per_fixture:
        for fx, axes_covered in per_fixture:
            lines.append(f"- `{fx.name}`")
    else:
        lines.append("- _(ninguno)_")
    lines.append("")

    for axis_name in ("languages", "frameworks", "build_systems", "file_kinds", "containers"):
        wanted = list(axes.get(axis_name, []) or [])
        if not wanted:
            continue
        covered = aggregate.get(axis_name, set())
        lines.append(f"## Eje: {axis_name}")
        lines.append("")
        lines.append("| Item | Estado | Cubierto por |")
        lines.append("|---|---|---|")
        for item in wanted:
            if item in covered:
                who = [fx.name for fx, a in per_fixture if item in a.get(axis_name, set())]
                lines.append(f"| `{item}` | cubierto | {', '.join(who) if who else '—'} |")
            else:
                lines.append(f"| `{item}` | **falta** | _(ninguno)_ |")
        lines.append("")

    traps = axes.get("traps", {})
    min_super = (traps.get("min_per_fixture") or {}).get("superficial")
    min_pkg = (traps.get("min_per_fixture") or {}).get("package")
    if min_super is not None or min_pkg is not None:
        lines.append("## Trampas minimas por fixture")
        lines.append("")
        lines.append(f"- Superficiales: {min_super}")
        lines.append(f"- De paquete: {min_pkg}")
        lines.append("")

    return "\n".join(lines) + "\n"


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Genera la matriz de cobertura de fixtures")
    parser.add_argument("--check", action="store_true", help="Salir con codigo 2 si hay gaps.")
    parser.add_argument("--out", type=Path, default=MATRIX_OUT, help="Ruta del Markdown de salida.")
    args = parser.parse_args(argv)

    try:
        target = _load_target()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    fixtures = _discover_fixtures()
    per_fixture: List[tuple] = []
    aggregate: Dict[str, Set[str]] = {
        "languages": set(),
        "frameworks": set(),
        "build_systems": set(),
        "file_kinds": set(),
        "containers": set(),
    }
    for fx in fixtures:
        covered = _fixture_axes(fx)
        per_fixture.append((fx, covered))
        for k, v in covered.items():
            aggregate[k] |= v

    md = _format_md(target, per_fixture, aggregate)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(md, encoding="utf-8")
    print(f"OK: {args.out} escrito con {len(per_fixture)} fixture(s).")

    if args.check:
        axes = target.get("axes", {})
        gaps: List[str] = []
        for axis_name in ("languages", "frameworks", "build_systems", "file_kinds", "containers"):
            for item in axes.get(axis_name, []) or []:
                if item not in aggregate.get(axis_name, set()):
                    gaps.append(f"{axis_name}:{item}")
        if gaps:
            print(f"Cobertura incompleta ({len(gaps)} gaps). Use sin --check para ver el detalle.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
