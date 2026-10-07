#pragma once

#include <functional>
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>

namespace fxproc {

class FilterBase;  // forward decl

// E06: jerarquia virtual. FilterBase tiene virtual run() y un metodo
// no-virtual name() para dispatch por string.
class FilterBase {
public:
    virtual ~FilterBase() = default;
    virtual std::string run(const std::string& input) = 0;
    virtual std::string name() const = 0;
};

// E06 (continuacion): clase con destructor virtual. La trampa E06 del
// ecosistema es que un filtro plantado invoca un metodo virtual dentro
// de su propio constructor, lo que resulta en dispatch estatico en
// lugar de polimorfico. Documentado en src/filters.cpp.
class FilterError : public std::runtime_error {
public:
    explicit FilterError(const std::string& msg) : std::runtime_error(msg) {}
};

// Factory function que cada filtro define con su nombre.
using FilterFactory = std::function<std::unique_ptr<FilterBase>()>;

}  // namespace fxproc
