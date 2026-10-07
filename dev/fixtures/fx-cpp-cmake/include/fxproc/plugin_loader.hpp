// E05: plugin loader que envuelve dlopen/dlsym. La trampa paquete P03
// (plugin_memory_leak) planta un deleter incompleto que no llama
// dlclose en todos los caminos de salida.
#pragma once

#include "filter_base.hpp"
#include "registry.hpp"

#include <filesystem>
#include <memory>
#include <stdexcept>
#include <string>

namespace fxproc {

class PluginError : public std::runtime_error {
public:
    explicit PluginError(const std::string& msg) : std::runtime_error(msg) {}
};

// Símbolo que el plugin exporta con `extern "C"`. Resuelto por dlsym.
using PluginRegisterFn = void (*)(Registry&);

// E05: deleter custom. El paquete P03 planta un bug en este deleter:
// si la libreria se marca con `RTLD_LOCAL` o se carga con
// `dlopen(path, RTLD_LAZY)`, el handle puede ser valido pero el
// deleter llama `dlclose` que retorna -1 silenciosamente. Para esta
// fixture, el deleter se documenta como "incompleto" via un comentario
// que el test verifica.
struct PluginDeleter {
    void operator()(void* h) const;
};

class PluginLoader {
public:
    PluginLoader() = default;

    // Carga un .so y registra los filtros que expone.
    // Retorna el numero de filtros registrados.
    size_t load(const std::string& path);

    // Acceso a la libreria cargada (para tests).
    void* handle() const { return handle_.get(); }

    bool is_loaded() const { return static_cast<bool>(handle_); }

private:
    std::unique_ptr<void, PluginDeleter> handle_;
};

}  // namespace fxproc
