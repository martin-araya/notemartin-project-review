// F06x: tests de las 6 trampas del ecosistema + 6 del paquete + 3
// superficiales. Cada test verifica la presencia del patron en el
// codigo fuente del fixture.
#include "fxproc/executor.hpp"
#include "fxproc/registry.hpp"
#include "fxproc/pipeline.hpp"
#include "fxproc/result.hpp"
#include "fxproc/version.hpp"
#include "fxproc/filters.hpp"

#include <atomic>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <future>
#include <gtest/gtest.h>
#include <string>
#include <thread>

namespace fs = std::filesystem;

#ifndef FXPROC_SOURCE_DIR
#define FXPROC_SOURCE_DIR "."
#endif
#ifndef FXPROC_BUILD_DIR
#define FXPROC_BUILD_DIR "."
#endif

// --- E01: static registrar ---
TEST(TrapE01, StaticRegistrarAutoRegisters) {
    auto& reg = fxproc::Registry::instance();
    EXPECT_GE(reg.size(), 4u);  // ToUpper, Reverse, Json, to_json_dup
}

// --- E02: templates + CRTP + concepts ---
TEST(TrapE02, PipelineUsesTemplateDispatch) {
    fxproc::Pipeline<fxproc::ToUpper, fxproc::Reverse> p(
        fxproc::ToUpper{}, fxproc::Reverse{});
    EXPECT_EQ(p.run("hello"), "OLLEH");
}

TEST(TrapE02, CRTPProvidesLabel) {
    fxproc::Pipeline<fxproc::ToUpper> p(fxproc::ToUpper{});
    EXPECT_EQ(p.label(), "Pipeline");
}

// --- E03: x-macros ---
TEST(TrapE03, XMacrosGenerateMultipleFilters) {
    auto& reg = fxproc::Registry::instance();
    // La trampa P06 hace que la lista tenga 4 entradas (con un
    // duplicado de Json).
    EXPECT_GE(reg.size(), 3u);  // al menos 3 entradas unicas
}

// --- E04: headers generados por CMake ---
TEST(TrapE04, ConfigHeaderExists) {
    fs::path p = std::string(FXPROC_BUILD_DIR) + "/generated/fxproc/config.h";
    if (!fs::exists(p)) {
        GTEST_SKIP() << "config.h no generado: " << p;
    }
    std::ifstream in(p);
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    EXPECT_NE(content.find("FX_VERSION"), std::string::npos);
    EXPECT_NE(content.find("FX_PROJECT_NAME"), std::string::npos);
}

// --- E05: dlopen + dlsym ---
TEST(TrapE05, PluginLoaderUsesDlopen) {
    std::ifstream in(std::string(FXPROC_SOURCE_DIR) + "/src/plugin_loader.cpp");
    ASSERT_TRUE(in.is_open());
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    EXPECT_NE(content.find("dlopen"), std::string::npos);
    EXPECT_NE(content.find("dlsym"), std::string::npos);
    EXPECT_NE(content.find("fx_plugin_register"), std::string::npos);
}

// --- E06: dispatch virtual + static init order ---
TEST(TrapE06, InitOrderTrapMarkerIsSet) {
    EXPECT_EQ(fxproc::init_order_marker(), 1);
}

// --- P01: thread no join ---
TEST(TrapP01, ExecutorSubmitDetaches) {
    // La trampa P01 se planta en src/executor.cpp: el thread se
    // detach() en lugar de join(). Verificamos que el codigo usa
    // .detach().
    std::ifstream in(std::string(FXPROC_SOURCE_DIR) + "/src/executor.cpp");
    ASSERT_TRUE(in.is_open());
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    EXPECT_NE(content.find(".detach()"), std::string::npos);
}

TEST(TrapP01, ExecutorActiveThreadsIncreases) {
    std::atomic<bool> go{false};
    std::atomic<bool> done{false};
    fxproc::Executor executor;
    auto fut = executor.submit([&]() {
        while (!go) std::this_thread::sleep_for(std::chrono::milliseconds(1));
        done = true;
        return std::string("ok");
    });
    // Esperamos a que el thread se haya creado.
    for (int i = 0; i < 100 && fxproc::Executor::active_threads() == 0; ++i) {
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
    EXPECT_GE(fxproc::Executor::active_threads(), 1u);
    go = true;
    fut.wait();
}

// --- P02: pipeline_error_swallowed ---
TEST(TrapP02, ShouldSkipHelperExists) {
    // La trampa P02 planta should_skip_filter; verificamos que existe
    // y maneja el caso vacio sin lanzar.
    EXPECT_TRUE(fxproc::should_skip_filter(""));
    EXPECT_FALSE(fxproc::should_skip_filter("non-empty"));
}

// --- P03: plugin_memory_leak (deleter incompleto) ---
TEST(TrapP03, PluginDeleterDefined) {
    std::ifstream in(std::string(FXPROC_SOURCE_DIR) + "/include/fxproc/plugin_loader.hpp");
    ASSERT_TRUE(in.is_open());
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    EXPECT_NE(content.find("PluginDeleter"), std::string::npos);
    EXPECT_NE(content.find("dlclose"), std::string::npos);
}

// --- P04: export_race ---
TEST(TrapP04, ToFileOpensWithoutExclusiveLock) {
    std::ifstream in(std::string(FXPROC_SOURCE_DIR) + "/src/result.cpp");
    ASSERT_TRUE(in.is_open());
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    EXPECT_NE(content.find("ios::trunc"), std::string::npos);
    // La trampa es la ausencia de O_EXCL / lock.
    EXPECT_EQ(content.find("O_EXCL"), std::string::npos);
}

// --- P05: cmake_target_no_optional ---
TEST(TrapP05, TransformJsonAddedUnconditionally) {
    std::ifstream in(std::string(FXPROC_SOURCE_DIR) + "/CMakeLists.txt");
    ASSERT_TRUE(in.is_open());
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    EXPECT_NE(content.find("add_subdirectory(plugins/transform_json)"),
              std::string::npos);
    // La trampa: el target se anade sin gate por FX_HAS_PLUGINS.
    std::ifstream plugin(std::string(FXPROC_SOURCE_DIR) + "/plugins/transform_json/CMakeLists.txt");
    std::string pc((std::istreambuf_iterator<char>(plugin)),
                   std::istreambuf_iterator<char>());
    EXPECT_EQ(pc.find("if(FX_HAS_PLUGINS)"), std::string::npos);
}

// --- P06: xmacro_collision ---
TEST(TrapP06, XMacrosListHasDuplicateJson) {
    std::ifstream in(std::string(FXPROC_SOURCE_DIR) + "/include/fxproc/x_macros.h");
    ASSERT_TRUE(in.is_open());
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    // Contar ocurrencias de la linea `X(Json,` en la primera lista
    // (FX_FILTERS); la segunda (FX_FILTERS_STMT) es paralela.
    int count = 0;
    size_t pos = 0;
    while ((pos = content.find("X(Json,", pos)) != std::string::npos) {
        ++count;
        pos += std::string("X(Json,").size();
    }
    EXPECT_GE(count, 2);  // FX_FILTERS + FX_FILTERS_STMT, ambas con duplicado
}

// --- S01: dead_legacy_filter ---
TEST(TrapS01, LegacyFilterExistsButNotRegistered) {
    std::ifstream in(std::string(FXPROC_SOURCE_DIR) + "/src/filters.cpp");
    ASSERT_TRUE(in.is_open());
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    EXPECT_NE(content.find("LegacyFilter"), std::string::npos);
    auto& reg = fxproc::Registry::instance();
    EXPECT_FALSE(reg.has("legacy"));
}

// --- S02: unused_helper ---
TEST(TrapS02, DeprecatedHelpersLackDeprecationAttribute) {
    std::ifstream in(std::string(FXPROC_SOURCE_DIR) + "/include/fxproc/util/deprecated_helpers.hpp");
    ASSERT_TRUE(in.is_open());
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    EXPECT_NE(content.find("old_slugify"), std::string::npos);
    // La trampa: ningun [[deprecated]] presente.
    EXPECT_EQ(content.find("[[deprecated"), std::string::npos);
}

// --- S03: commented_out_branch ---
TEST(TrapS03, FiltersContainsCommentedOutBlock) {
    std::ifstream in(std::string(FXPROC_SOURCE_DIR) + "/src/filters.cpp");
    ASSERT_TRUE(in.is_open());
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    // Las 4 lineas comentadas que parecen codigo pero no lo son.
    EXPECT_NE(content.find("TODO: soporte para colores"), std::string::npos);
    EXPECT_NE(content.find("if (in.find(\"error\")"), std::string::npos);
}
