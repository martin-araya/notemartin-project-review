// F06x: tests de dispatch virtual y orden de inicializacion estatica
// (E06). El fixture planta un InitOrderTrap que se ejecuta antes
// que el dispatch virtual este disponible; verificamos que el
// marker existe.
#include "fxproc/filters.hpp"
#include "fxproc/filter_base.hpp"
#include "fxproc/registry.hpp"

#include <gtest/gtest.h>

TEST(StaticInit, OrderMarkerIsSet) {
    // g_init_marker es 1 si InitOrderTrap se ejecuto, 0 en caso
    // contrario. Como fxproc es una libreria static, su carga
    // inicial ocurre antes de main().
    EXPECT_EQ(fxproc::init_order_marker(), 1);
}

TEST(Dispatch, VirtualRunUsesDerivedImplementation) {
    fxproc::FilterBase* base = new fxproc::ToUpper();
    EXPECT_EQ(base->run("hello"), "HELLO");
    delete base;
}

TEST(Dispatch, RegistryCreateReturnsDerivedPointer) {
    auto& reg = fxproc::Registry::instance();
    auto f = reg.create("reverse");
    EXPECT_EQ(f->name(), "reverse");
    EXPECT_EQ(f->run("abc"), "cba");
}
