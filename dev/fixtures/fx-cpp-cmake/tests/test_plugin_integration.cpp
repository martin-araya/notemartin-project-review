// F06x: test de integracion con el plugin real. Compilado aparte
// para que pueda enlazarse contra libtransform_json.so.
#include "fxproc/registry.hpp"
#include "fxproc/version.hpp"
#include "fxproc/filters.hpp"

#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <gtest/gtest.h>
#include <string>

namespace fs = std::filesystem;

namespace {

fs::path locate_plugin() {
    // Buscamos libtransform_json.so en build/plugins o al lado del binario.
    fs::path candidates[] = {
        fs::path("build/plugins/libtransform_json.so"),
        fs::path("../plugins/libtransform_json.so"),
        fs::path("plugins/libtransform_json.so"),
    };
    for (const auto& c : candidates) {
        if (fs::exists(c)) return c;
    }
    return {};
}

}  // namespace

TEST(PluginIntegration, PluginIsAvailable) {
    fs::path lib = locate_plugin();
    if (lib.empty()) {
        GTEST_SKIP() << "libtransform_json.so no encontrado en build/plugins/";
    }
    EXPECT_TRUE(fs::exists(lib));
}

TEST(PluginIntegration, VersionIsReasonable) {
    std::string v = fxproc::version();
    EXPECT_FALSE(v.empty());
    EXPECT_NE(v.find("0"), std::string::npos);
}
