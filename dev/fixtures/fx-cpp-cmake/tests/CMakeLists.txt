# F06x: tests con GoogleTest via FetchContent.
include(FetchContent)

set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz
    URL_HASH SHA256=8ad598c73ad796e0d8280b082cebd82a630d73e73cd3c70057938a6501bba5d7
)
FetchContent_MakeAvailable(googletest)

include(GoogleTest)

# Tests.
add_executable(unit_tests
    test_registry.cpp
    test_pipeline.cpp
    test_filters.cpp
    test_x_macros.cpp
    test_cmake_generated.cpp
    test_plugin_loader.cpp
    test_dispatch.cpp
    test_export.cpp
    test_traps.cpp
)
target_link_libraries(unit_tests PRIVATE fxproc_core GTest::gtest_main)
target_include_directories(unit_tests PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_BINARY_DIR}/generated
)
target_compile_definitions(unit_tests PRIVATE
    FXPROC_SOURCE_DIR="${CMAKE_SOURCE_DIR}"
    FXPROC_BUILD_DIR="${CMAKE_BINARY_DIR}"
    FXPROC_PLUGIN_LIB="${CMAKE_BINARY_DIR}/plugins/libtransform_json${CMAKE_SHARED_LIBRARY_SUFFIX}"
)
add_test(NAME unit_tests COMMAND unit_tests)

# Test que carga el plugin y verifica dlopen real.
add_executable(plugin_loader_test test_plugin_integration.cpp)
target_link_libraries(plugin_loader_test PRIVATE fxproc_core GTest::gtest_main)
add_dependencies(plugin_loader_test transform_json)
target_compile_definitions(plugin_loader_test PRIVATE
    FXPROC_PLUGIN_LIB="${CMAKE_BINARY_DIR}/plugins/libtransform_json${CMAKE_SHARED_LIBRARY_SUFFIX}"
    FXPROC_SOURCE_DIR="${CMAKE_SOURCE_DIR}"
)
target_include_directories(plugin_loader_test PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_BINARY_DIR}/generated
)
add_test(NAME plugin_loader_test COMMAND plugin_loader_test)
