# fx-cpp-cmake

Motor de procesamiento C++20 con CMake 3.25, plugins cargados via `dlopen`, registro estatico de filtros, templates + CRTP, x-macros, headers generados por CMake y dispatch virtual con un bug de orden de inicializacion estatica plantado.

## Stack

- C++20
- GCC 13.x (clang en macOS via apple-clang)
- CMake 3.25+
- GoogleTest 1.14 (vía `FetchContent`)
- POSIX `dlopen`/`dlsym`/`dlclose` para plugins

## Features

- `cargar-plugin`: carga un `.so` por `dlopen` y resuelve `fx_plugin_register`.
- `pipeline-de-filtros`: ejecuta una cadena de filtros via CRTP y concepts.
- `exportar-resultados`: persiste el resultado del pipeline a stdout/archivo.

## Comandos

```bash
make test    # cmake -S . -B build && cmake --build build && ctest --test-dir build
make build   # solo compila
make history # genera historia git de 8 commits (solo la primera vez)
```

## Contenedor

```bash
python dev/tools/run_fixture_tests.py --fixture fx-cpp-cmake --container
```

Imagen: `gcc:13-bookworm` con `cmake` y `make`.
