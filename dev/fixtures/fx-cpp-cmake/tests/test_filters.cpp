// F06x: tests de los filtros puros.
#include "fxproc/filters.hpp"
#include "fxproc/version.hpp"

#include <gtest/gtest.h>

using fxproc::ToUpper;
using fxproc::Reverse;
using fxproc::Json;

TEST(ToUpperFilter, UppercasesAscii) {
    ToUpper f;
    EXPECT_EQ(f.run("hello"), "HELLO");
    EXPECT_EQ(f.run("MiXeD"), "MIXED");
}

TEST(ReverseFilter, ReversesString) {
    Reverse f;
    EXPECT_EQ(f.run("abc"), "cba");
    EXPECT_EQ(f.run(""), "");
}

TEST(JsonFilter, IncludesInputAndVersion) {
    Json f;
    std::string out = f.run("hello");
    EXPECT_NE(out.find("hello"), std::string::npos);
    EXPECT_NE(out.find(fxproc::version()), std::string::npos);
}
