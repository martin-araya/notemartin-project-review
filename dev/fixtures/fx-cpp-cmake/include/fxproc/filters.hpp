#pragma once

#include "filter_base.hpp"

namespace fxproc {

// E02 + E03: las clases se declaran via x-macro en x_macros.h, pero
// las declaraciones concretas se duplican aqui para que el codigo
// de los tests las pueda usar directamente.
class ToUpper : public FilterBase {
public:
    std::string run(const std::string& in) override;
    std::string name() const override { return "to_upper"; }
};

class Reverse : public FilterBase {
public:
    std::string run(const std::string& in) override;
    std::string name() const override { return "reverse"; }
};

class Json : public FilterBase {
public:
    std::string run(const std::string& in) override;
    std::string name() const override { return "to_json"; }
};

int init_order_marker();

bool should_skip_filter(const std::string& in);

}  // namespace fxproc
