// E02: pipeline con concepts, CRTP y SFINAE. El pipeline se compone
// en tiempo de compilacion (cada filtro es un parametro template)
// pero se ejecuta en runtime via `run(input)`.
#pragma once

#include "filter_base.hpp"
#include "x_macros.h"

#include <stdexcept>
#include <string>
#include <tuple>
#include <type_traits>
#include <utility>

namespace fxproc {

// E02: concept que restringe los filtros a clases derivadas de
// FilterBase con un `run` que acepta y devuelve std::string.
template <typename F>
concept Filter = std::is_base_of_v<FilterBase, F> &&
    requires(F f, const std::string& in) {
        { f.run(in) } -> std::convertible_to<std::string>;
    };

// E02: CRTP base para que cada pipeline concreto pueda especializar
// el dispatch sin pasar por la jerarquia virtual.
template <typename Derived>
class PipelineBase {
public:
    std::string label() const { return static_cast<const Derived*>(this)->label_impl(); }
};

// E02: SFINAE para detectar si el filtro tiene un metodo `describe()`.
template <typename F, typename = void>
struct has_describe : std::false_type {};

template <typename F>
struct has_describe<F, std::void_t<decltype(std::declval<F>().describe())>>
    : std::true_type {};

// Pipeline: tupla de filtros y ejecucion secuencial.
template <Filter... Filters>
class Pipeline : public PipelineBase<Pipeline<Filters...>> {
public:
    explicit Pipeline(Filters... fs)
        : filters_(std::move(fs)...) {}

    std::string label_impl() const { return "Pipeline"; }

    // E02: ejecucion secuencial. Si un filtro devuelve vacio, el
    // pipeline se aborta con FilterError. La trampa paquete P02
    // (pipeline_error_swallowed) intercepta y devuelve input sin
    // loggear.
    std::string run(const std::string& input) {
        std::string current = input;
        std::apply([&](auto&... f) {
            ((current = f.run(current)), ...);
        }, filters_);
        return current;
    }

private:
    std::tuple<Filters...> filters_;
};

}  // namespace fxproc
