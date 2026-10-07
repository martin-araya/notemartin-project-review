// E05: plugin demo. Exporta `extern "C" void fx_plugin_register(Registry&)`
// que la app principal busca via `dlsym`. Al registrarse, el plugin
// anade dos filtros custom: `lower` y `slugify`.
//
// El archivo compila como `libtransform_json.so` en build/plugins/.
#include "fxproc/filter_base.hpp"
#include "fxproc/registry.hpp"

#include <algorithm>
#include <cctype>
#include <string>

namespace fxproc {

class Lower : public FilterBase {
public:
    std::string run(const std::string& in) override {
        std::string out = in;
        std::transform(out.begin(), out.end(), out.begin(),
                       [](unsigned char c) { return std::tolower(c); });
        return out;
    }
    std::string name() const override { return "lower"; }
};

class Slugify : public FilterBase {
public:
    std::string run(const std::string& in) override {
        std::string out;
        out.reserve(in.size());
        for (char c : in) {
            if (std::isalnum(static_cast<unsigned char>(c))) {
                out += static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
            } else if (c == ' ' || c == '-') {
                out += '_';
            }
        }
        return out;
    }
    std::string name() const override { return "slugify"; }
};

}  // namespace fxproc

// E05: simbolo de registro resuelto por dlsym.
extern "C" void fx_plugin_register(fxproc::Registry& reg) {
    reg.register_filter("lower", []() {
        return std::make_unique<fxproc::Lower>();
    });
    reg.register_filter("slugify", []() {
        return std::make_unique<fxproc::Slugify>();
    });
}
