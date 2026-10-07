// E02 + E06: implementacion de los filtros. El filtro ToUpper demuestra
// el dispatch virtual con el bug de orden de inicializacion estatica
// (trampa E06): un filtro intenta invocar un metodo virtual dentro
// de su propio constructor, lo que resulta en dispatch estatico.
#include "fxproc/filters.hpp"
#include "fxproc/registry.hpp"
#include "fxproc/version.hpp"

#include <algorithm>
#include <cctype>
#include <iomanip>
#include <sstream>
#include <stdexcept>
#include <string>

namespace fxproc {

// E06: una variable de inicializacion estatica plantada que rompe el
// orden. La usamos dentro del constructor de un filtro para que
// el dispatch virtual falle al auto-registrarse.
namespace {
int g_init_marker = 0;
struct InitOrderTrap {
    InitOrderTrap() {
        // Documentado como E06: si este constructor corre antes que
        // el de FilterBase (que nunca se llama directamente), el
        // dispatch virtual queda silenciosamente como estatico. Lo
        // documentamos via una variable global que el test inspecciona.
        g_init_marker = 1;
    }
};
InitOrderTrap g_trap_instance;
}  // namespace

int init_order_marker() { return g_init_marker; }

// --- ToUpper ---
std::string ToUpper::run(const std::string& in) {
    std::string out = in;
    std::transform(out.begin(), out.end(), out.begin(),
                   [](unsigned char c) { return std::toupper(c); });
    return out;
}

// --- Reverse ---
std::string Reverse::run(const std::string& in) {
    return std::string(in.rbegin(), in.rend());
}

// --- Json ---
// E02: el filtro Json usa el format string con prefijo para que
// la salida sea un objeto JSON valido.
std::string Json::run(const std::string& in) {
    // S03: trampa superficial #3. Hay 4 lineas comentadas justo
    // debajo que parecen codigo activo pero no lo son.
    // TODO: soporte para colores ANSI en la salida JSON.
    //   if (in.find("error") != std::string::npos) {
    //       return "{\"level\":\"error\",\"msg\":\"" + in + "\"}";
    //   }
    std::ostringstream os;
    os << "{\"input\":\"" << in << "\",\"version\":\"" << version() << "\"}";
    return os.str();
}

// P02: pipeline_error_swallowed. Helper que parece "silenciar errores"
// pero en realidad se usa para detectar inputs vacios.
bool should_skip_filter(const std::string& in) {
    return in.empty();
}

// --- S01: trampa superficial #1. Filtro legacy que nadie usa.
// Esta clase se compila pero no se registra porque esta excluida de
// la lista FX_FILTERS.
class LegacyFilter : public FilterBase {
public:
    std::string run(const std::string& in) override {
        return in + "_legacy";
    }
    std::string name() const override { return "legacy"; }
};

// Auto-registro de los filtros canonicos via x-macros.
// La trampa P06 (xmacro_collision) se planta en x_macros.h duplicando
// el nombre "Json" dos veces; el segundo shadow al primero.
FX_REGISTER_FILTER(ToUpper, "to_upper")
FX_REGISTER_FILTER(Reverse, "reverse")
FX_REGISTER_FILTER(Json, "to_json")

// El segundo registro "Json" con nombre "to_json_dup" demuestra que
// el shadow del registro NO se manifiesta cuando los nombres son
// distintos. La trampa solo aplica cuando el mismo nombre aparece
// dos veces, lo cual ocurre via la trampa paquete P06.
FX_REGISTER_FILTER(Json, "to_json_dup")

}  // namespace fxproc
