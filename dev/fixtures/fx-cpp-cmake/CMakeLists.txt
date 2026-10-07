cmake_minimum_required(VERSION 3.25)
project(fxproc VERSION 0.1.0 LANGUAGES CXX)

# C++20 obligatorio.
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

# E04: Header generado por CMake via configure_file.
# Definimos las variables que el .in expande con @ONLY.
set(FXPROC_VERSION "${PROJECT_VERSION}")
set(FXPROC_PROJECT_NAME "${PROJECT_NAME}")
configure_file(
    ${CMAKE_SOURCE_DIR}/cmake/config.h.in
    ${CMAKE_BINARY_DIR}/generated/fxproc/config.h
    @ONLY
)

# Exportamos el directorio de includes y la libreria principal.
add_library(fxproc_core STATIC
    src/registry.cpp
    src/pipeline.cpp
    src/plugin_loader.cpp
    src/executor.cpp
    src/filters.cpp
    src/result.cpp
)
target_include_directories(fxproc_core PUBLIC
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_BINARY_DIR}/generated
)
# POSIX necesario para dlopen/dlsym/dlclose.
target_link_libraries(fxproc_core PUBLIC ${CMAKE_DL_LIBS})

# El binario principal (CLI de demo).
add_executable(fxproc src/main.cpp)
target_link_libraries(fxproc PRIVATE fxproc_core)

# Demo de exportacion.
add_executable(export_demo apps/export_demo.cpp)
target_link_libraries(export_demo PRIVATE fxproc_core)

# P05: el target del plugin de transform_json se construye siempre, incluso
# si FX_HAS_PLUGINS=OFF. La macro se declara en config.h pero no se respeta
# en este subdirectorio.
option(FX_HAS_PLUGINS "Build dlopen plugins" ON)
add_subdirectory(plugins/transform_json)

# Tests
enable_testing()
add_subdirectory(tests)
