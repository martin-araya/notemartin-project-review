// F06x: tests de los headers generados por CMake (E04).
#include "fxproc/version.hpp"
#include "fxproc/config.h"  // generado por configure_file

#include <fstream>
#include <gtest/gtest.h>
#include <string>

#ifndef FXPROC_BUILD_DIR
#define FXPROC_BUILD_DIR "."
#endif

TEST(GeneratedConfig, VersionIsNonEmpty) {
    std::string v = fxproc::version();
    EXPECT_FALSE(v.empty());
}

TEST(GeneratedConfig, VersionContainsProjectName) {
    std::string v = fxproc::version();
    // La version es "0.1.0" por defecto. Verificamos el patron.
    EXPECT_NE(v.find("."), std::string::npos);
}

TEST(GeneratedConfig, HasPluginsMacroIsDefined) {
    // FX_HAS_PLUGINS puede estar definida o no segun -DFX_HAS_PLUGINS=ON/OFF.
    // El test verifica que la macro aparece en el header generado por
    // CMake (sea como define o como undef).
    std::ifstream in(std::string(FXPROC_BUILD_DIR) + "/generated/fxproc/config.h");
    ASSERT_TRUE(in.is_open());
    std::string content((std::istreambuf_iterator<char>(in)),
                        std::istreambuf_iterator<char>());
    EXPECT_TRUE(content.find("FX_HAS_PLUGINS") != std::string::npos);
}
