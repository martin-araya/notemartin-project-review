// F06x: tests del Pipeline (E02: templates + CRTP + concepts).
#include "fxproc/pipeline.hpp"
#include "fxproc/filters.hpp"

#include <gtest/gtest.h>

using fxproc::Pipeline;
using fxproc::ToUpper;
using fxproc::Reverse;

TEST(Pipeline, EmptyRunsIdentity) {
    // Un pipeline de 0 filtros acepta cualquier input.
    // No se construye sin filtros aqui porque Pipeline requiere al
    // menos uno. Probamos run de un solo filtro.
    Pipeline<ToUpper> p(ToUpper{});
    EXPECT_EQ(p.run("hello"), "HELLO");
}

TEST(Pipeline, SingleFilterApplies) {
    Pipeline<ToUpper> p(ToUpper{});
    EXPECT_EQ(p.run("abc"), "ABC");
}

TEST(Pipeline, TwoFiltersCompose) {
    Pipeline<ToUpper, Reverse> p(ToUpper{}, Reverse{});
    EXPECT_EQ(p.run("hello"), "OLLEH");
}

TEST(Pipeline, LabelReturnsPipeline) {
    Pipeline<ToUpper, Reverse> p(ToUpper{}, Reverse{});
    EXPECT_EQ(p.label(), "Pipeline");
}
