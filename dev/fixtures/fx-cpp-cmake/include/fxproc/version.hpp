// F06x: header con macros que vienen del archivo generado por CMake
// (trampa E04). La skill debe ejecutar
// `cmake -S . -B build && cat build/generated/fxproc/config.h` para
// descubrir la version real.
#pragma once
#include "fxproc/config.h"  // generado por configure_file en build/generated/
#include <string>

namespace fxproc {

inline std::string version() {
    return FX_VERSION;
}

inline std::string project_name() {
    return FX_PROJECT_NAME;
}

#ifdef FX_HAS_PLUGINS
inline constexpr bool has_plugins() { return true; }
#else
inline constexpr bool has_plugins() { return false; }
#endif

}  // namespace fxproc
