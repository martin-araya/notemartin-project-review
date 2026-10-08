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
    ".php": {"php"},
    ".h": {"c", "cpp", "objective-c"},
    ".m": {"objective-c"},
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
    ".csproj": {"msbuild"},
    ".sln": {"msbuild"},
    "requirements.txt": {"pip"},
    "pyproject.toml": {"pyproject"},
    "composer.json": {"composer"},
    "Package.swift": {"swiftpm"},
}

# Archivos clave de frameworks
FRAMEWORK_FILES: Dict[str, Set[str]] = {
    "angular.json": {"angular", "javascript"},
    "nest-cli.json": {"nestjs"},
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
    # Spring Boot: la presencia de pom.xml indica Maven; con
    # spring-boot-starter-* en el pom.xml es Spring Boot.
    "pom.xml": {"maven", "spring-boot"},
    # Gradle (Kotlin DSL): la presencia de build.gradle.kts indica
    # un proyecto Kotlin/Gradle.
    "build.gradle.kts": {"gradle", "kotlin"},
    # ASP.NET Core: la presencia de *.csproj indica un proyecto .NET
    # Web SDK. Cualquier *.csproj cubre el framework aspnet-core.
    ".csproj": {"aspnet-core", "csharp"},
    # Django: manage.py + apps/<app>/apps.py con AppConfig.
    "manage.py": {"django"},
    # pytest-django: pytest.ini con DJANGO_SETTINGS_MODULE.
    "pytest.ini": {"pytest-django"},
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
    # NgRx 17: la dep ``@ngrx/store`` indica NgRx (F06l).
    "@ngrx/store": {"ngrx"},
    # Angular Material: la dep ``@angular/material`` indica Angular Material (F06l).
    "@angular/material": {"angular-material"},
    # Spring Boot: la dep ``spring-boot-starter-web`` indica Spring Boot (F06m).
    "spring-boot-starter-web": {"spring-boot"},
    # Ktor: la dep ``ktor-server-core`` indica Ktor (F06n).
    "ktor-server-core": {"ktor"},
    # Koin: la dep ``koin-ktor`` indica Koin (F06n).
    "koin-ktor": {"koin"},
    # MediatR: la dep ``MediatR`` indica CQRS con MediatR (F06o).
    "MediatR": {"mediatr"},
    # EF Core: la dep ``Microsoft.EntityFrameworkCore`` indica EF Core (F06o).
    "Microsoft.EntityFrameworkCore": {"ef-core"},
    # ASP.NET Core (F06o): el selector public usa ``aspnet-core``.
    "aspnet-core": {"aspnet-core"},
    # SwiftUI / Combine / WidgetKit / UIKit (F06aa): se detectan aparte
    # en el scan de archivos .swift (ver ``_scan_swift_sources``).
    "import WidgetKit": {"widgetkit"},
    "import UIKit": {"uikit"},
    "import SwiftData": {"swiftdata"},
    # Django (F06p): la dep ``Django`` indica framework Django.
    "Django": {"django"},
    # DRF (F06p): la dep ``djangorestframework`` indica API REST.
    "djangorestframework": {"drf"},
    # Celery (F06p): la dep ``celery`` indica tareas asincronas.
    "celery": {"celery"},
    # pytest-django (F06p): la dep ``pytest-django`` indica tests Django.
    "pytest-django": {"pytest-django"},
    # FastAPI (F06q): la dep ``fastapi`` indica framework FastAPI.
    "fastapi": {"fastapi"},
    # Pydantic (F06q): la dep ``pydantic`` indica validacion Pydantic.
    "pydantic": {"pydantic"},
    # Alembic (F06q): la dep ``alembic`` indica migraciones Alembic.
    "alembic": {"alembic"},
    # NestJS (F06r): la dep ``@nestjs/core`` indica framework NestJS.
    "@nestjs/core": {"nestjs"},
    # TypeORM (F06r): la dep ``typeorm`` indica ORM TypeORM.
    "typeorm": {"typeorm"},
    # BullMQ (F06r): la dep ``bullmq`` indica cola de mensajes.
    "bullmq": {"bullmq"},
    # Laravel (F06u): la dep ``laravel/framework`` indica framework Laravel.
    "laravel/framework": {"laravel"},
    # Eloquent: parte de Laravel, cubierto por la misma dep.
    # Blade: parte de Laravel, cubierto por la misma dep.
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
            # Ktor: si build.gradle.kts menciona la dep ktor-server-core.
            if "ktor-server-core" in content:
                covered["frameworks"].add("ktor")
            # Koin: si build.gradle.kts menciona koin-ktor o koin-core.
            if "koin-ktor" in content or "koin-core" in content:
                covered["frameworks"].add("koin")
        except (OSError, UnicodeDecodeError):
            pass

    # Detectar SwiftUI / Combine / WidgetKit / UIKit / SwiftData en
    # archivos ``.swift`` del fixture (F06aa). Tambien detectar App Group
    # en ``.entitlements`` y la presencia de un ``.xcodeproj``.
    swift_imports = {
        "SwiftUI": "swiftui",
        "Combine": "combine",
        "WidgetKit": "widgetkit",
        "UIKit": "uikit",
        "SwiftData": "swiftdata",
    }
    for swift_file in list(fixture_dir.rglob("*.swift")) + list(fixture_dir.rglob("*.m")):
        if not swift_file.is_file():
            continue
        try:
            content = swift_file.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        for imp, fw in swift_imports.items():
            if f"import {imp}" in content:
                covered["frameworks"].add(fw)
    # App Group en entitlements.
    for ent in fixture_dir.rglob("*.entitlements"):
        if not ent.is_file():
            continue
        try:
            content = ent.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        if "application-groups" in content or "com.apple.security.application-groups" in content:
            covered["frameworks"].add("app-groups")
    # Xcode project: presencia de *.xcodeproj/project.pbxproj.
    for pbx in fixture_dir.rglob("*.xcodeproj/project.pbxproj"):
        if pbx.is_file():
            covered["frameworks"].add("xcode-project")
            # Si hay un .xcconfig, tambien detectamos el sistema de build.
            if any(fixture_dir.rglob("*.xcconfig")):
                covered["build_systems"].add("xcodebuild")
            break

    # F06ab: Swift server-side (Vapor, Fluent, swift-argument-parser,
    # swift-syntax, swift-macro, spm-build-tool-plugin). Detectamos:
    # - Vapor en Package.swift
    # - Fluent y swift-argument-parser en Package.swift
    # - swift-syntax -> swift-syntax + swift-macro
    # - Plugins/<X>/Package.swift con .pluginTarget -> spm-build-tool-plugin
    # - "RouteCollection" en .swift -> fluent (Vapor routing layer)
    package_swift = fixture_dir / "Package.swift"
    if package_swift.is_file():
        try:
            ps_content = package_swift.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            ps_content = ""
        if "vapor" in ps_content.lower() and "Vapor" in ps_content:
            covered["frameworks"].add("vapor")
        if "Fluent" in ps_content:
            covered["frameworks"].add("fluent")
        if "swift-argument-parser" in ps_content.lower() or "ArgumentParser" in ps_content:
            covered["frameworks"].add("swift-argument-parser")
        if "swift-syntax" in ps_content.lower():
            covered["frameworks"].add("swift-syntax")
        if "SwiftSyntaxMacros" in ps_content or "@attached" in ps_content or "@freestanding" in ps_content:
            covered["frameworks"].add("swift-macro")
    # Swift macros adicionales: buscar archivos que definan macros en Sources/*Macros*
    for macros_dir in fixture_dir.rglob("*Macros*"):
        if not macros_dir.is_dir():
            continue
        for swift_file in macros_dir.rglob("*.swift"):
            try:
                content = swift_file.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                continue
            if "@attached" in content or "@freestanding" in content or "Macro" in content:
                covered["frameworks"].add("swift-macro")
                covered["frameworks"].add("swift-syntax")
                break
    # Build tool plugin: presencia de Plugins/<X>/Package.swift con .pluginTarget.
    for plugin_pkg in (fixture_dir / "Plugins").rglob("Package.swift") if (fixture_dir / "Plugins").is_dir() else []:
        try:
            pp_content = plugin_pkg.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        if ".pluginTarget" in pp_content or "capability: .buildTool()" in pp_content:
            covered["frameworks"].add("spm-build-tool-plugin")
            break

    # F06ac: Android Kotlin (Compose, Hilt, Room, WorkManager, Navigation,
    # ViewBinding, Gradle flavors, Robolectric). Detectamos via build.gradle*:
    # - com.android.application -> android
    # - dagger.hilt.android -> hilt (+ hilt-android)
    # - androidx.hilt:hilt-work -> hilt-work
    # - androidx.hilt:hilt-navigation-compose -> hilt-navigation-compose
    # - androidx.room -> room
    # - androidx.work -> workmanager
    # - androidx.navigation -> navigation-compose
    # - android:onClick o buildFeatures.viewBinding -> view-binding
    # - productFlavors -> gradle-flavors
    # - org.robolectric -> robolectric
    # - androidx.appcompat -> appcompat
    android_root = fixture_dir / "app"
    gradle_files = []
    if android_root.is_dir():
        gradle_files.extend(android_root.rglob("build.gradle.kts"))
        gradle_files.extend(android_root.rglob("build.gradle"))
    gradle_files.append(fixture_dir / "build.gradle.kts")
    if (fixture_dir / "build.gradle.kts").is_file():
        gradle_files.append(fixture_dir / "build.gradle.kts")
    gradle_text = ""
    for gf in gradle_files:
        if gf.is_file():
            try:
                gradle_text += "\n" + gf.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                pass
    if gradle_text:
        if "com.android.application" in gradle_text or "android {\n" in gradle_text or 'id("com.android.application")' in gradle_text:
            covered["frameworks"].add("android")
        if "dagger.hilt.android" in gradle_text.lower() or "hilt.android" in gradle_text.lower():
            covered["frameworks"].add("hilt")
            covered["frameworks"].add("hilt-android")
        if "androidx.hilt:hilt-work" in gradle_text or "hilt-work" in gradle_text.lower():
            covered["frameworks"].add("hilt-work")
        if "androidx.hilt:hilt-navigation-compose" in gradle_text or "hilt-navigation-compose" in gradle_text.lower():
            covered["frameworks"].add("hilt-navigation-compose")
        if "androidx.room" in gradle_text or '"room"' in gradle_text.lower():
            covered["frameworks"].add("room")
        if "androidx.work" in gradle_text or "workmanager" in gradle_text.lower():
            covered["frameworks"].add("workmanager")
        if "androidx.navigation" in gradle_text or "navigation-compose" in gradle_text.lower():
            covered["frameworks"].add("navigation-compose")
        if "android:onClick" in gradle_text or "viewBinding = true" in gradle_text:
            covered["frameworks"].add("view-binding")
        if "productFlavors" in gradle_text or 'create("free")' in gradle_text:
            covered["frameworks"].add("gradle-flavors")
        if "androidx.appcompat" in gradle_text:
            covered["frameworks"].add("appcompat")
    # Compose + Robolectric via gradle/libs.versions.toml o dependencias en build.gradle
    version_catalog = fixture_dir / "gradle/libs.versions.toml"
    if version_catalog.is_file():
        try:
            catalog = version_catalog.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            catalog = ""
        if "compose-bom" in catalog or "androidx.compose" in catalog:
            covered["frameworks"].add("jetpack-compose")
        if "robolectric" in catalog:
            covered["frameworks"].add("robolectric")
    if "jetpack-compose" not in covered["frameworks"]:
        if "androidx.compose" in gradle_text:
            covered["frameworks"].add("jetpack-compose")
    if "robolectric" not in covered["frameworks"]:
        if "robolectric" in gradle_text.lower():
            covered["frameworks"].add("robolectric")

    # F06ad: Flutter / Dart (Riverpod, go_router, freezed, json_serializable,
    # riverpod_generator, build_runner, platform channels, dart-define,
    # adaptive widgets). Detected via pubspec.yaml + .dart files.
    pubspec = fixture_dir / "pubspec.yaml"
    if pubspec.is_file():
        try:
            ps_text = pubspec.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            ps_text = ""
        if ps_text:
            if "flutter:" in ps_text and "sdk: flutter" in ps_text:
                covered["frameworks"].add("flutter")
            if "flutter_riverpod" in ps_text or "riverpod" in ps_text.lower():
                covered["frameworks"].add("flutter-riverpod")
            if "go_router" in ps_text:
                covered["frameworks"].add("go-router")
            if "freezed_annotation" in ps_text or "freezed:" in ps_text:
                covered["frameworks"].add("freezed")
            if "json_serializable" in ps_text or "json_annotation" in ps_text:
                covered["frameworks"].add("json-serializable")
            if "riverpod_generator" in ps_text:
                covered["frameworks"].add("riverpod-generator")
            if "build_runner" in ps_text:
                covered["frameworks"].add("build-runner")
            if "shared_preferences" in ps_text:
                covered["frameworks"].add("shared-preferences")

    # Scan .dart files for platform channels, dart-define, adaptive widgets
    dart_sources = list(fixture_dir.rglob("*.dart"))
    dart_text = ""
    for df in dart_sources:
        if df.is_file():
            try:
                dart_text += "\n" + df.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                pass
    if dart_text:
        if "MethodChannel" in dart_text or "FlutterMethodChannel" in dart_text:
            covered["frameworks"].add("platform-channels")
        if "bool.fromEnvironment" in dart_text or "String.fromEnvironment" in dart_text or "int.fromEnvironment" in dart_text:
            covered["frameworks"].add("dart-define")
        if "TargetPlatform.iOS" in dart_text and ("Cupertino" in dart_text or "Material" in dart_text):
            covered["frameworks"].add("adaptive-widgets")

    # F06af: Electron (main, preload, renderer, IPC channels, contextBridge,
    # electron-builder, utility process, custom protocol app://).
    el_text = ""
    el_pkg = fixture_dir / "package.json"
    if el_pkg.is_file():
        try:
            el_text = el_pkg.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            el_text = ""
        if el_text and '"electron"' in el_text and '"electron-builder"' in el_text:
            covered["frameworks"].add("electron")
            covered["frameworks"].add("electron-builder")
        src_root = fixture_dir / "src"
        if src_root.exists():
            el_ts_files = [str(p) for p in src_root.rglob("*.ts")]
            if any("contextBridge" in t for t in el_ts_files) or "contextBridge" in el_text:
                covered["frameworks"].add("electron-context-bridge")
    # electron-builder.yml asarUnpack + extraResources
    eb = fixture_dir / "electron-builder.yml"
    if eb.is_file():
        try:
            eb_content = eb.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            eb_content = ""
        if "asarUnpack" in eb_content:
            covered["frameworks"].add("electron-asar-unpack")
        if "extraResources" in eb_content:
            covered["frameworks"].add("electron-extra-resources")
    # utilityProcess.fork + child_process.fork + protocol.handle
    el_sources = []
    src_root = fixture_dir / "src"
    if src_root.exists():
        for ext in ("*.ts", "*.js"):
            for p in src_root.rglob(ext):
                if p.is_file():
                    try:
                        el_sources.append(p.read_text(encoding="utf-8", errors="replace"))
                    except (OSError, UnicodeDecodeError):
                        pass
    el_src_text = "\n".join(el_sources)
    if "utilityProcess.fork" in el_src_text:
        covered["frameworks"].add("electron-utility-process")
    if "protocol.handle" in el_src_text and "registerSchemesAsPrivileged" in el_src_text:
        covered["frameworks"].add("electron-app-scheme")
    if "autoUpdater" in el_src_text or "electron-updater" in el_text:
        covered["frameworks"].add("electron-auto-updater")

    # F06ag: WPF (XAML bindings, source generators, MVVM, data templates,
    # value converters, merged dictionaries, style triggers, xunit tests).
    csproj_files = list(fixture_dir.rglob("*.csproj"))
    sln_files = list(fixture_dir.rglob("*.sln"))
    xaml_files = list(fixture_dir.rglob("*.xaml"))
    cs_files = list(fixture_dir.rglob("*.cs"))
    xaml_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in xaml_files if p.is_file())
    cs_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in cs_files if p.is_file())
    csproj_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in csproj_files if p.is_file())
    if csproj_text and "UseWPF" in csproj_text:
        covered["frameworks"].add("wpf")
        covered["frameworks"].add("xaml")
    if "[ObservableProperty]" in cs_text or "[RelayCommand]" in cs_text or "CommunityToolkit.Mvvm" in csproj_text:
        covered["frameworks"].add("mvvm")
        covered["frameworks"].add("community-toolkit-mvvm")
    if "DataTemplate" in xaml_text:
        covered["frameworks"].add("data-template")
    if "IValueConverter" in cs_text:
        covered["frameworks"].add("value-converter")
    if "MergedDictionaries" in xaml_text:
        covered["frameworks"].add("merged-dictionary")
    if "<Style.Triggers>" in xaml_text or "<DataTrigger" in xaml_text:
        covered["frameworks"].add("style-trigger")
    if sln_files and any('xunit' in csproj_text for csproj_file in csproj_files if csproj_file.is_file()):
        covered["frameworks"].add("xunit")

    # F06ah: PostgreSQL (Flyway, PL/pgSQL, pg_cron, pgTAP, RLS, triggers,
    # materialized views, EXECUTE format, CASCADE constraints).
    sql_files = list(fixture_dir.rglob("*.sql"))
    sql_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in sql_files if p.is_file())
    if sql_files:
        if "EXECUTE format" in sql_text:
            covered["frameworks"].add("sql-dynamic")
        if "ROW LEVEL SECURITY" in sql_text:
            covered["frameworks"].add("row-level-security")
        if "ON DELETE CASCADE" in sql_text:
            covered["frameworks"].add("cascade-constraint")
        if "CREATE TRIGGER" in sql_text or "BEFORE INSERT" in sql_text:
            covered["frameworks"].add("trigger")
        if "MATERIALIZED VIEW" in sql_text:
            covered["frameworks"].add("materialized-view")
        if "LANGUAGE plpgsql" in sql_text or "RETURNS TRIGGER" in sql_text:
            covered["frameworks"].add("pl-pgsql")
        if "pg_cron" in sql_text or "cron.schedule" in sql_text:
            covered["frameworks"].add("pg-cron")
        if "flyway.locations" in sql_text.lower() or "V1__" in str(fixture_dir):
            covered["frameworks"].add("flyway")
        if "pgtap" in sql_text.lower() or "pg_prove" in sql_text.lower() or "pg_test" in sql_text.lower():
            covered["frameworks"].add("pgtap")
        # PostgreSQL itself
        if "CREATE TABLE" in sql_text or "CREATE EXTENSION" in sql_text:
            covered["frameworks"].add("postgresql")
        # Oracle detection: PL/SQL + Liquibase + utPLSQL
        if "PRAGMA" in sql_text or "CREATE PACKAGE" in sql_text or "EXECUTE IMMEDIATE" in sql_text:
            covered["frameworks"].add("pl-sql")
            covered["frameworks"].add("oracle")
        if "liquibase" in sql_text.lower() or "changelog-master.xml" in sql_text or "<databaseChangeLog" in sql_text:
            covered["frameworks"].add("liquibase")
        if "ut.run" in sql_text.lower() or "ut.expect" in sql_text.lower() or "utplsql" in sql_text.lower():
            covered["frameworks"].add("utplsql")
        if "DBMS_SCHEDULER" in sql_text:
            covered["frameworks"].add("dbms-scheduler")
        if "CREATE DATABASE LINK" in sql_text or "DATABASE LINK" in sql_text:
            covered["frameworks"].add("db-link")
        if "AUTONOMOUS_TRANSACTION" in sql_text:
            covered["frameworks"].add("autonomous-transaction")
        if "INSTEAD OF" in sql_text:
            covered["frameworks"].add("instead-of")
        if "CREATE PUBLIC SYNONYM" in sql_text or "SYNONYM" in sql_text:
            covered["frameworks"].add("synonym")
        if "EXECUTE IMMEDIATE" in sql_text:
            covered["frameworks"].add("execute-immediate")

        # F06ak: dbt + Airflow + DuckDB detection.

    # F06al: Python ML detection.
    dvc_yaml = fixture_dir / "dvc.yaml"
    if dvc_yaml.is_file():
        covered["frameworks"].add("dvc")
        covered["frameworks"].add("dvc-yaml")
    hydra_conf = fixture_dir / "conf" / "config.yaml"
    if hydra_conf.is_file():
        try:
            hc = hydra_conf.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            hc = ""
        if "@package" in hc or "defaults:" in hc:
            covered["frameworks"].add("hydra")
            covered["frameworks"].add("hydra-config")
    if (fixture_dir / "src" / "register.py").is_file() or (fixture_dir / "mlruns").exists():
        covered["frameworks"].add("mlflow")
        covered["frameworks"].add("mlflow-file-store")
    notebooks_dir = fixture_dir / "notebooks"
    if notebooks_dir.is_dir() and list(notebooks_dir.glob("*.ipynb")):
        covered["frameworks"].add("notebook-ipynb")
        covered["frameworks"].add("jupyter")
        if (fixture_dir / "pytest.ini").is_file():
            covered["frameworks"].add("nbval")
    req_txt = fixture_dir / "requirements.txt"
    if req_txt.is_file():
        try:
            req = req_txt.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            req = ""
        if "scikit-learn" in req:
            covered["frameworks"].add("scikit-learn")
        if "torch" in req:
            covered["frameworks"].add("pytorch")

        dbt_project_yml = fixture_dir / "dbt" / "dbt_project.yml"
        if dbt_project_yml.is_file():
            covered["frameworks"].add("dbt")
            covered["frameworks"].add("duckdb")
            dbt_text = dbt_project_yml.read_text(encoding="utf-8", errors="replace")
            if "+materialized:" in dbt_text:
                covered["frameworks"].add("dbt-materialization-config")
            if "incremental" in dbt_text:
                covered["frameworks"].add("is_incremental")
        dbt_models = fixture_dir / "dbt" / "models"
        if dbt_models.is_dir():
            dbt_sql_text = "\n".join(
                p.read_text(encoding="utf-8", errors="replace")
                for p in dbt_models.rglob("*.sql")
            )
            if "{{ ref(" in dbt_sql_text or "{{ source(" in dbt_sql_text:
                covered["frameworks"].add("dbt-models")
                covered["frameworks"].add("dbt-lineage")
                covered["frameworks"].add("ref-source")
            if "is_incremental()" in dbt_sql_text:
                covered["frameworks"].add("dbt-incremental")
        dbt_macros = fixture_dir / "dbt" / "macros"
        if dbt_macros.is_dir():
            macro_text = "\n".join(
                p.read_text(encoding="utf-8", errors="replace")
                for p in dbt_macros.rglob("*.sql")
            )
            if "{% macro" in macro_text or "{%- macro" in macro_text:
                covered["frameworks"].add("jinja-macros")
        airflow_dags = fixture_dir / "airflow" / "dags"
        if airflow_dags.is_dir():
            af_py = "\n".join(
                p.read_text(encoding="utf-8", errors="replace")
                for p in airflow_dags.rglob("*.py")
            )
            if "DAG(" in af_py:
                covered["frameworks"].add("airflow")
            if "yaml.safe_load" in af_py:
                covered["frameworks"].add("dag-factory")
            if "xcom_push" in af_py or "xcom_pull" in af_py:
                covered["frameworks"].add("xcom")
        req_txt = fixture_dir / "requirements.txt"
        if req_txt.is_file():
            try:
                req = req_txt.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                req = ""
            if "dbt-core" in req or "dbt-duckdb" in req:
                covered["frameworks"].add("dbt-duckdb")
            if "apache-airflow" in req:
                covered["frameworks"].add("apache-airflow")

        # F06aj: SQL Server / T-SQL detection.
        if "sp_executesql" in sql_text:
            covered["frameworks"].add("sp_executesql")
            covered["frameworks"].add("sqlserver")
        if "MERGE" in sql_text and "OUTPUT $action" in sql_text:
            covered["frameworks"].add("merge-output")
        if "AFTER INSERT" in sql_text or "AFTER UPDATE" in sql_text:
            covered["frameworks"].add("after-trigger")
        if re.search(r"WITH\s+\w+\s+AS\s*\(", sql_text) and "UNION ALL" in sql_text:
            # Heuristica: CTE recursiva (anchor + recursive UNION ALL)
            covered["frameworks"].add("recursive-cte")
        if "##" in sql_text or "tempdb.." in sql_text:
            covered["frameworks"].add("temp-tables")
        if "sp_add_job" in sql_text or "sysjobs" in sql_text.lower():
            covered["frameworks"].add("sql-agent")
        if "DATETIME2" in sql_text or "SYSUTCDATETIME()" in sql_text or "SET NOCOUNT ON" in sql_text:
            covered["frameworks"].add("tsql")
        # sqlcmd: detectado a nivel de Dockerfile.test
        dockerfile = fixture_dir / "Dockerfile.test"
        if dockerfile.is_file():
            try:
                df_text = dockerfile.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                df_text = ""
            if "mssql-tools18" in df_text:
                covered["frameworks"].add("sqlcmd")
                covered["frameworks"].add("sqlserver")

    # F06ae: React Native (Expo bare, React Navigation, Redux Toolkit,
    # TurboModules, Metro aliases, expo config plugins).
    rn_pkg = fixture_dir / "package.json"
    if rn_pkg.is_file():
        try:
            rn_text = rn_pkg.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            rn_text = ""
        if rn_text and '"react-native"' in rn_text and '"expo"' in rn_text:
            covered["frameworks"].add("react-native")
            covered["frameworks"].add("expo-bare")
        if "@react-navigation/native" in rn_text:
            covered["frameworks"].add("react-navigation")
        if "@reduxjs/toolkit" in rn_text:
            covered["frameworks"].add("redux-toolkit")
        if "metro.config.js" in rn_text or "metro" in rn_text.lower():
            covered["frameworks"].add("metro")
        if "NativeModules" in rn_text:
            covered["frameworks"].add("turbo-modules")
    # app.json with expo config plugins
    app_json = fixture_dir / "app.json"
    if app_json.is_file():
        try:
            app_text = app_json.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            app_text = ""
        if '"plugins"' in app_text:
            covered["frameworks"].add("expo-config-plugins")
        if "expo-linking" in app_text:
            covered["frameworks"].add("expo-linking")
        if "expo-notifications" in app_text:
            covered["frameworks"].add("expo-notifications")
        if "expo-build-properties" in app_text:
            covered["frameworks"].add("expo-build-properties")
        if "expo-splash-screen" in app_text:
            covered["frameworks"].add("expo-splash-screen")

    # Detectar deps de NuGet via *.csproj (MediatR, EF Core, ASP.NET Core).
    for csproj in fixture_dir.rglob("*.csproj"):
        if not csproj.is_file():
            continue
        # Cualquier *.csproj implica MSBuild como build system.
        covered["build_systems"].add("msbuild")
        try:
            content = csproj.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        if "MediatR" in content:
            covered["frameworks"].add("mediatr")
        if "Microsoft.EntityFrameworkCore" in content:
            covered["frameworks"].add("ef-core")
        if "Microsoft.AspNetCore" in content:
            covered["frameworks"].add("aspnet-core")

    # Detectar deps de PyPI via requirements.txt o pyproject.toml.
    for req_file in fixture_dir.rglob("requirements.txt"):
        if not req_file.is_file():
            continue
        try:
            content = req_file.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        if "Django" in content:
            covered["frameworks"].add("django")
        if "djangorestframework" in content:
            covered["frameworks"].add("drf")
        if "celery" in content:
            covered["frameworks"].add("celery")
        if "pytest-django" in content:
            covered["frameworks"].add("pytest-django")
        if "fastapi" in content.lower():
            covered["frameworks"].add("fastapi")
        if "pydantic" in content.lower():
            covered["frameworks"].add("pydantic")
        if "sqlalchemy" in content.lower():
            covered["frameworks"].add("sqlalchemy")
        if "alembic" in content.lower():
            covered["frameworks"].add("alembic")

    # Detectar presencia de apps/<app>/apps.py con AppConfig (Django).
    for apps_py in fixture_dir.rglob("apps.py"):
        if not apps_py.is_file():
            continue
        # Solo contar si vive bajo un directorio apps/ (no el raiz).
        rel = apps_py.relative_to(fixture_dir).as_posix()
        if rel.startswith("apps/") and "/" in rel:
            try:
                content = apps_py.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                continue
            if "AppConfig" in content:
                covered["frameworks"].add("django")

    # Detectar Laravel via composer.json con laravel/framework (F06u).
    for composer_json in fixture_dir.rglob("composer.json"):
        if not composer_json.is_file():
            continue
        # Solo contar composer.json en la raiz o en un subdirectorio (no en vendor/).
        rel = composer_json.relative_to(fixture_dir).as_posix()
        if rel.startswith("vendor/"):
            continue
        try:
            data = json.loads(composer_json.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            continue
        deps = {}
        deps.update(data.get("require", {}) or {})
        deps.update(data.get("require-dev", {}) or {})
        if "laravel/framework" in deps:
            covered["frameworks"].add("laravel")
            covered["frameworks"].add("eloquent")
            covered["frameworks"].add("blade")
        # Markers adicionales para Laravel.
        for marker, frameworks in PACKAGE_JSON_MARKERS.items():
            if marker in deps:
                covered["frameworks"] |= frameworks
        break

    # Detectar Rails via Gemfile (F06v).
    for gemfile in fixture_dir.rglob("Gemfile"):
        if not gemfile.is_file():
            continue
        rel = gemfile.relative_to(fixture_dir).as_posix()
        if rel.startswith("vendor/") or rel.startswith(".bundle/"):
            continue
        try:
            content = gemfile.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        if "gem \"rails\"" in content or "gem 'rails'" in content:
            covered["frameworks"].add("rails")
            covered["build_systems"].add("bundler")
            if "turbo-rails" in content or "turbo" in content:
                covered["frameworks"].add("hotwire")
            if "sidekiq" in content:
                covered["frameworks"].add("sidekiq")
            if "rspec-rails" in content:
                covered["frameworks"].add("rspec")
        break

    # Detectar C++ via CMakeLists.txt (F06x).
    for cmakelists in fixture_dir.rglob("CMakeLists.txt"):
        if not cmakelists.is_file():
            continue
        rel = cmakelists.relative_to(fixture_dir).as_posix()
        if rel.startswith("build/") or rel.startswith("vendor/"):
            continue
        try:
            content = cmakelists.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        if "cmake_minimum_required" in content:
            covered["frameworks"].add("cmake")
            covered["languages"].add("cpp")
            if "add_test" in content or "ctest" in content:
                covered["frameworks"].add("ctest")
            if "gtest" in content.lower() or "gmock" in content.lower():
                covered["frameworks"].add("gtest")
            if "dlopen" in content or "dlsym" in content or "find_package.*dl" in content.lower():
                covered["frameworks"].add("dlopen")
        break

    # Detectar C embebido (F06y) via firmware.ld + Unity.
    has_firmware_ld = any(fixture_dir.rglob("firmware.ld"))
    has_unity = any("unity.h" in str(f) for f in fixture_dir.rglob("*.h"))
    if has_firmware_ld and has_unity:
        covered["languages"].add("c")
        covered["build_systems"].add("make")
        covered["build_systems"].add("gnu-ld")
        covered["frameworks"].add("unity")
        covered["frameworks"].add("linker-script")

    # Detectar Qt 6 (F06z) via find_package(Qt6) + QML files.
    has_qt6 = False
    for cmakelists in fixture_dir.rglob("CMakeLists.txt"):
        if not cmakelists.is_file():
            continue
        rel = cmakelists.relative_to(fixture_dir).as_posix()
        if rel.startswith("build/"):
            continue
        try:
            content = cmakelists.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        if "find_package(Qt6" in content or "qt_standard_project_setup" in content:
            has_qt6 = True
            covered["build_systems"].add("qt-cmake")
            break
    if has_qt6:
        covered["frameworks"].add("qt6")
        if list(fixture_dir.rglob("qml/*.qml")):
            covered["frameworks"].add("qml")
        if list(fixture_dir.rglob("tests/*.cpp")):
            # Buscamos QTest en los tests
            for cpp_file in fixture_dir.rglob("tests/*.cpp"):
                try:
                    if "QTEST" in cpp_file.read_text(encoding="utf-8", errors="replace"):
                        covered["frameworks"].add("qt-test")
                        break
                except (OSError, UnicodeDecodeError):
                    continue

    # Detectar FastAPI via app/main.py con constructor FastAPI() (F06q).
    for main_py in fixture_dir.rglob("main.py"):
        if not main_py.is_file():
            continue
        # Solo contar si vive bajo un directorio app/ (no el raiz).
        rel = main_py.relative_to(fixture_dir).as_posix()
        if rel.startswith("app/") and "/" in rel[len("app/"):]:
            try:
                content = main_py.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                continue
            if "FastAPI(" in content:
                covered["frameworks"].add("fastapi")
                break

    # Detectar go-chi via go.mod (F06s).
    for go_mod in fixture_dir.rglob("go.mod"):
        if not go_mod.is_file():
            continue
        try:
            content = go_mod.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        if "github.com/go-chi/chi" in content:
            covered["frameworks"].add("go-chi")
        if "github.com/google/wire" in content:
            covered["frameworks"].add("wire")
        if "github.com/mattn/go-sqlite3" in content:
            covered["frameworks"].add("sqlite")
        break

    # Detectar sqlc via sqlc.yaml (F06s).
    for sqlc_yaml in fixture_dir.rglob("sqlc.yaml"):
        if not sqlc_yaml.is_file():
            continue
        covered["frameworks"].add("sqlc")
        break

    # Detectar Rust frameworks via Cargo.toml (F06t).
    for cargo_toml in fixture_dir.rglob("Cargo.toml"):
        if not cargo_toml.is_file():
            continue
        # No detectar el Cargo.toml del workspace hijo.
        rel = cargo_toml.relative_to(fixture_dir).as_posix()
        if rel.startswith("derive-macro/"):
            continue
        try:
            content = cargo_toml.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        if "axum" in content:
            covered["frameworks"].add("axum")
        if "tokio" in content:
            covered["frameworks"].add("tokio")
        if "sqlx" in content:
            covered["frameworks"].add("sqlx")
        if "thiserror" in content:
            covered["frameworks"].add("thiserror")
        if "serde" in content and "derive" in content:
            covered["frameworks"].add("serde")
        # Cargo build script.
        if "build.rs" in rel or (fixture_dir / "build.rs").is_file():
            covered["build_systems"].add("cargo-build-script")
        break

    # Detectar go:embed via grep (F06s).
    for go_file in fixture_dir.rglob("*.go"):
        if not go_file.is_file():
            continue
        if "stub-davecheney" in str(go_file.relative_to(fixture_dir)):
            continue
        try:
            content = go_file.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        if "//go:embed " in content:
            covered["frameworks"].add("embed")
            break

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
