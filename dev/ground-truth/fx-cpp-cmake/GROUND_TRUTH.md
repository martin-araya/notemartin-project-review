# GROUND_TRUTH — fx-cpp-cmake

## Vision general

Fixture C++20 con CMake 3.25, GoogleTest 1.14 via FetchContent, plugin cargado via `dlopen`/`dlsym`, registro estatico de filtros, templates + CRTP, x-macros, header generado por CMake y dispatch virtual con bug de orden de inicializacion estatica plantado. Cubre la primera fase del bloque "Nativo y sistemas" de la matriz de fixtures (F06x-F06z).

## Stack

- C++20 (GCC 13.x en `gcc:13-bookworm`)
- CMake 3.25+ con `configure_file` para headers generados
- GoogleTest 1.14 via `FetchContent`
- POSIX `dlopen`/`dlsym`/`dlclose` para plugins

## Features y R-NN

| Feature | R-NN | Cubre |
|---|---|---|
| `cargar-plugin` | 7 | dlopen con RTLD_NOW, dlsym, errores NotFound/InvalidFormat/MissingSymbol, deleter, RTLD_LAZY vs RTLD_NOW, semantica de dlclose |
| `pipeline-de-filtros` | 7 | Pipeline<Filter...> con concepts, CRTP, std::apply, serializacion Json, ejecucion concurrente con trampa P01, timeout |
| `exportar-resultados` | 7 | to_stdout, to_file con JSON, to_file con CSV, errores de permiso/IO, race condition (P04) |

## Trampas plantadas (CC-04..CC-06)

### Ecosistema (6/6)
1. **E01** `Registrar<T>` template en `include/fxproc/registry.hpp:74-82` con auto-registro via `FX_REGISTER_FILTER` macro.
2. **E02** `concept Filter` + `Pipeline : PipelineBase<...>` CRTP en `include/fxproc/pipeline.hpp:20-55`.
3. **E03** `FX_FILTERS` / `FX_FILTERS_STMT` en `include/fxproc/x_macros.h:13-26` con duplicado intencional.
4. **E04** `configure_file` en `CMakeLists.txt:19` + `cmake/config.h.in` con `FX_VERSION`/`FX_PROJECT_NAME`/`FX_HAS_PLUGINS`.
5. **E05** `dlopen`/`dlsym` en `src/plugin_loader.cpp:39-54` + `extern "C" fx_plugin_register` en `plugins/transform_json/transform_json.cpp:36`.
6. **E06** `InitOrderTrap` global en `src/filters.cpp:30` + `FilterBase` virtual en `include/fxproc/filter_base.hpp`.

### Paquete (6/6)
1. **P01** `std::thread(...).detach()` en `src/executor.cpp:18` (no join).
2. **P02** `should_skip_filter` helper en `src/filters.cpp:70` (parece silenciar errores).
3. **P03** `PluginDeleter` no chequea retorno de `dlclose` en `include/fxproc/plugin_loader.hpp:32-39`.
4. **P04** `ofstream(path, ios::trunc)` sin `O_EXCL` ni lock en `src/result.cpp:25`.
5. **P05** `add_subdirectory(plugins/transform_json)` sin gate por `FX_HAS_PLUGINS` en `CMakeLists.txt:39`.
6. **P06** `X(Json, to_json)` duplicado en `include/fxproc/x_macros.h:16-17` + shadow silencioso en `Registry::register_filter`.

### Superficiales (3/3)
1. **S01** `LegacyFilter` class compilada en `src/filters.cpp:75-82` pero no auto-registrada.
2. **S02** 3 funciones obsoletas en `include/fxproc/util/deprecated_helpers.hpp` sin marca de deprecation.
3. **S03** 4 lineas comentadas con `TODO` en `src/filters.cpp:54-58`.

## Salida de la suite

45 tests GoogleTest + 2 tests de integracion passing en `gcc:13-bookworm` con `cmake 3.25` y `ctest --output-on-failure`.

- 4 tests de Registry (E01)
- 4 tests de Pipeline (E02)
- 3 tests de filtros puros
- 3 tests de x-macros (E03)
- 3 tests de headers generados por CMake (E04)
- 4 tests de plugin loader (E05)
- 3 tests de dispatch virtual + static init order (E06)
- 3 tests de exportacion
- 6 tests de trampas del ecosistema
- 7 tests de trampas del paquete
- 3 tests de trampas superficiales
- 2 tests de integracion del plugin

## Comandos para reproducir

```bash
docker build -f dev/fixtures/fx-cpp-cmake/Dockerfile.test -t npr-fx-cpp-cmake dev/fixtures/fx-cpp-cmake
docker run --rm npr-fx-cpp-cmake

# o via run_fixture_tests.py:
python dev/tools/run_fixture_tests.py --fixture fx-cpp-cmake --container
```

## Comandos para regenerar la historia git

```bash
cd dev/fixtures/fx-cpp-cmake
bash build-history.sh
```

Crea 8 commits incrementales.

## Notas de portabilidad

- El fixture no soporta Windows porque `dlopen` es POSIX. El manifest declara
  `requires: linux, macos` y omite Windows.
- `g++` 13.x y `cmake` 3.25+ son obligatorios; versiones anteriores tienen
  bugs de C++20 incompatibles con el codigo.
- GoogleTest 1.14 se descarga via `FetchContent` (no requiere red durante
  el build, solo en la primera configuracion).
