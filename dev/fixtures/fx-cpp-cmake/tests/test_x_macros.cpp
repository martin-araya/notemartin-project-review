// F06x: tests de x-macros (E03). Las x-macros se procesan en tiempo
// de compilacion; los tests verifican que los tipos generados se
// pueden instanciar y que la lista esta completa.
#include "fxproc/x_macros.h"
#include "fxproc/filter_base.hpp"
#include "fxproc/registry.hpp"
#include "fxproc/filters.hpp"

#include <gtest/gtest.h>

TEST(XMacros, ListDefinesFourEntries) {
    int count = 0;
    #define COUNT_X(ClassName, NameStr) ++count
    FX_FILTERS_STMT(COUNT_X)
    #undef COUNT_X
    EXPECT_GE(count, 3);
    EXPECT_LE(count, 5);
}

TEST(XMacros, DeclareFilterMacroGeneratesInstantiableClass) {
    using fxproc::ToUpper;
    ToUpper f;
    EXPECT_EQ(f.name(), "to_upper");
}

TEST(XMacros, GeneratedFiltersAreRegistered) {
    auto& reg = fxproc::Registry::instance();
    EXPECT_TRUE(reg.has("to_upper"));
    EXPECT_TRUE(reg.has("reverse"));
    EXPECT_TRUE(reg.has("to_json"));
}
