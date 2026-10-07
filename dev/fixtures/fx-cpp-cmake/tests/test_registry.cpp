// F06x: tests del Registry (E01: static init).
#include "fxproc/registry.hpp"
#include "fxproc/filters.hpp"

#include <gtest/gtest.h>

using fxproc::Registry;

TEST(Registry, ContainsCanonicalFilters) {
    auto& reg = Registry::instance();
    EXPECT_TRUE(reg.has("to_upper"));
    EXPECT_TRUE(reg.has("reverse"));
    EXPECT_TRUE(reg.has("to_json"));
    EXPECT_TRUE(reg.has("to_json_dup"));
}

TEST(Registry, HasAtLeastFourFilters) {
    auto& reg = Registry::instance();
    EXPECT_GE(reg.size(), 4u);
}

TEST(Registry, CreateReturnsValidFilter) {
    auto& reg = Registry::instance();
    auto f = reg.create("to_upper");
    ASSERT_NE(f, nullptr);
    EXPECT_EQ(f->name(), "to_upper");
    EXPECT_EQ(f->run("hello"), "HELLO");
}

TEST(Registry, ThrowsOnUnknownFilter) {
    auto& reg = Registry::instance();
    EXPECT_THROW(reg.create("does_not_exist"), fxproc::RegistryError);
}
