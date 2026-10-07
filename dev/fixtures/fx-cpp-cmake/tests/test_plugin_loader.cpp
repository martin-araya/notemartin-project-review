// F06x: tests del plugin loader (E05: dlopen).
#include "fxproc/plugin_loader.hpp"
#include "fxproc/registry.hpp"

#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <gtest/gtest.h>
#include <string>

namespace fs = std::filesystem;

namespace {

// Construye la ruta al .so del plugin. CMake la pasa como macro.
#ifndef FXPROC_PLUGIN_LIB
#define FXPROC_PLUGIN_LIB "build/plugins/libtransform_json.so"
#endif

}  // namespace

TEST(PluginLoader, ThrowsOnMissingFile) {
    fxproc::PluginLoader loader;
    EXPECT_THROW(loader.load("/does/not/exist/libfoo.so"), fxproc::PluginError);
}

TEST(PluginLoader, ThrowsOnNonElfFile) {
    // Creamos un archivo temporal que no es un .so.
    fs::path tmp = fs::temp_directory_path() / "fxproc_not_a_so.txt";
    {
        std::ofstream f(tmp);
        f << "esto no es un shared object";
    }
    fxproc::PluginLoader loader;
    EXPECT_THROW(loader.load(tmp.string()), fxproc::PluginError);
    fs::remove(tmp);
}

namespace {

// Loader estatico para que la libreria permanezca cargada durante
// toda la corrida de tests. Si el loader se destruyera, dlclose se
// llamaria y los std::function registrados apuntarian a memoria
// liberada.
fxproc::PluginLoader& shared_loader() {
    static fxproc::PluginLoader* loader = nullptr;
    if (!loader) {
        loader = new fxproc::PluginLoader();
    }
    return *loader;
}

}  // namespace

TEST(PluginLoader, LoadsTransformJsonPlugin) {
    fs::path lib = FXPROC_PLUGIN_LIB;
    if (!fs::exists(lib)) {
        GTEST_SKIP() << "plugin no construido: " << lib;
    }
    auto& loader = shared_loader();
    size_t n = loader.load(lib.string());
    EXPECT_GE(n, 2u);
    EXPECT_TRUE(loader.is_loaded());
    EXPECT_NE(loader.handle(), nullptr);
    auto& reg = fxproc::Registry::instance();
    auto f = reg.create("lower");
    ASSERT_NE(f, nullptr);
    EXPECT_EQ(f->run("HELLO"), "hello");
}

TEST(PluginLoader, RegistersNewFiltersFromPlugin) {
    auto& reg = fxproc::Registry::instance();
    EXPECT_TRUE(reg.has("lower"));
    EXPECT_TRUE(reg.has("slugify"));
    auto f2 = reg.create("slugify");
    ASSERT_NE(f2, nullptr);
    EXPECT_EQ(f2->run("Hello World"), "hello_world");
}
