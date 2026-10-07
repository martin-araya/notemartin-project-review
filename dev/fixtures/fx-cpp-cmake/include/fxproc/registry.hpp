// E01: registro estatico de filtros. Cada filtro se auto-registra
// creando un `static Registrar<MyFilter>` en el archivo .cpp. La
// instanciacion del template ocurre antes de main(), asi que el
// registro esta poblado cuando el programa arranca.
#pragma once

#include "filter_base.hpp"

#include <functional>
#include <memory>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace fxproc {

class RegistryError : public std::runtime_error {
public:
    explicit RegistryError(const std::string& msg) : std::runtime_error(msg) {}
};

class Registry {
public:
    static Registry& instance() {
        static Registry r;
        return r;
    }

    // E01: registrar un factory por nombre. Lanza RegistryError si el
    // nombre ya existe (con la trampa paquete P04: shadow silencioso
    // cuando el filtro se declara via x-macros duplicado).
    void register_filter(const std::string& name, FilterFactory factory) {
        if (auto [it, inserted] = filters_.emplace(name, std::move(factory)); !inserted) {
            // P04: xmacro_collision. Por defecto, el segundo factory
            // SOBREESCRIBE al primero silenciosamente. La fixture
            // documenta esta decision con un test que verifica el
            // shadow.
            it->second = std::move(factory);
        }
    }

    bool has(const std::string& name) const {
        return filters_.find(name) != filters_.end();
    }

    std::unique_ptr<FilterBase> create(const std::string& name) const {
        auto it = filters_.find(name);
        if (it == filters_.end()) {
            throw RegistryError("filter not registered: " + name);
        }
        return it->second();
    }

    std::vector<std::string> names() const {
        std::vector<std::string> out;
        out.reserve(filters_.size());
        for (auto const& [k, v] : filters_) out.push_back(k);
        return out;
    }

    size_t size() const { return filters_.size(); }

    void clear() { filters_.clear(); }

private:
    Registry() = default;
    std::unordered_map<std::string, FilterFactory> filters_;
};

// E01: helper de auto-registro. El filtro declara
// `static fxproc::Registrar<MyFilter> reg_("my_filter");` en su .cpp
// y el template, al instanciarse, llama Registry::register_filter
// en su constructor.
template <typename T>
class Registrar {
public:
    Registrar(const std::string& name) {
        Registry::instance().register_filter(name, []() {
            return std::make_unique<T>();
        });
    }
};

// Macro util: declaramos una variable global (anonima namespace) del
// tipo Registrar<ClassName>. La instanciacion ocurre antes de main()
// gracias al mecanismo de inicializacion estatica de C++.
// No usamos `static` porque C++17 depreca `static` en namespace scope
// para tipos con destructor no trivial; la variable queda con linkage
// interno via namespace anonimo.
// El nombre de la variable se construye con __COUNTER__ para evitar
// colisiones entre invocaciones (P06: xmacro_collision). El truco de
// 3 niveles es necesario porque `__COUNTER__` no se expande cuando
// esta adyacente a `##`.
#define FX_PASTE3_(a, b, c) a##b##c
#define FX_PASTE3(a, b, c) FX_PASTE3_(a, b, c)

#define FX_REGISTER_FILTER(ClassName, NameString)                                  \
    namespace { ::fxproc::Registrar<ClassName> FX_PASTE3(_fx_reg_, __COUNTER__, _)(NameString); }

}  // namespace fxproc
