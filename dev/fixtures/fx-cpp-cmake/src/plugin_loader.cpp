#include "fxproc/plugin_loader.hpp"

#include <filesystem>
#include <fstream>
#include <string>

#include <cstring>
#include <dlfcn.h>

namespace fs = std::filesystem;

namespace fxproc {

void PluginDeleter::operator()(void* h) const {
    if (h) {
        // P03 trampa: el deleter no loggea el resultado de dlclose.
        // Si la libreria ya fue descargada por otra via, dlclose
        // retorna -1 con errno=ENOLCK y se ignora.
        ::dlclose(h);
    }
}

size_t PluginLoader::load(const std::string& path) {
    // Limpia el handle previo si existe.
    handle_.reset();

    if (!std::filesystem::exists(path)) {
        throw PluginError("plugin not found: " + path);
    }

    // E05: RTLD_NOW fuerza la resolucion de todos los simbolos en el
    // momento de dlopen. Con RTLD_LAZY, los errores aparecerian al
    // invocar fx_plugin_register.
    void* h = ::dlopen(path.c_str(), RTLD_NOW | RTLD_LOCAL);
    if (!h) {
        const char* err = ::dlerror();
        throw PluginError(std::string("dlopen failed: ") + (err ? err : "unknown"));
    }

    handle_.reset(h);

    // E05: dlsym para el simbolo de registro.
    ::dlerror();  // limpia errores previos
    auto sym = reinterpret_cast<PluginRegisterFn>(::dlsym(h, "fx_plugin_register"));
    if (!sym) {
        const char* err = ::dlerror();
        throw PluginError(std::string("symbol fx_plugin_register not found: ") +
                          (err ? err : "unknown"));
    }

    size_t before = Registry::instance().size();
    sym(Registry::instance());
    return Registry::instance().size() - before;
}

}  // namespace fxproc
