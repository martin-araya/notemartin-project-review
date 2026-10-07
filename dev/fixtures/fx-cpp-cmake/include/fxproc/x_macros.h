// E03: x-macros que generan tipos y registro a partir de una lista.
// La trampa paquete P06 duplica un nombre en FX_FILTERS; el segundo
// shadow al primero.
#pragma once

#include "filter_base.hpp"
#include "registry.hpp"

namespace fxproc {

// Lista canonica de filtros. La trampa paquete P06 duplica "Json" para
// forzar la colision en el registro. Cada entrada termina con `;` para
// que el caller la use como una lista de statements (FX_FILTERS_STMT).
#define FX_FILTERS(X) \
    X(ToUpper,  to_upper)   \
    X(Reverse,  reverse)    \
    X(Json,     to_json)    \
    X(Json,     to_json_dup)

// Variante con punto y coma al final de cada X(...) para uso como
// statements (e.g. ++count; ++count; ++count; ++count;).
#define FX_FILTERS_STMT(X)          \
    X(ToUpper,  to_upper);           \
    X(Reverse,  reverse);            \
    X(Json,     to_json);            \
    X(Json,     to_json_dup);

// Declara una clase para cada filtro via x-macro.
#define FX_DECLARE_FILTER(ClassName, NameStr) \
    class ClassName : public FilterBase {     \
    public:                                   \
        std::string run(const std::string& in) override; \
        std::string name() const override { return NameStr; } \
    };

}  // namespace fxproc
