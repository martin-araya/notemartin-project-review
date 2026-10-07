# Plugin contract — fxproc

Cada plugin debe exportar exactamente un simbolo con vinculacion C:

```c
extern "C" void fx_plugin_register(fxproc::Registry& reg);
```

La app principal resuelve este simbolo con `dlsym(handle, "fx_plugin_register")`
y le pasa la instancia singleton de `Registry`. El plugin debe
llamar `reg.register_filter(name, factory)` por cada filtro que quiera
exponer.

## Nombre y convenciones

- El archivo debe compilarse como una libreria compartida (`.so` en Linux,
  `.dylib` en macOS) con vinculacion local (`RTLD_LOCAL`).
- El nombre del archivo no importa; el contrato es el simbolo.
- Los filtros deben devolver `std::unique_ptr<fxproc::FilterBase>` desde
  su factory.

## Plantilla minima

```cpp
#include "fxproc/filter_base.hpp"
#include "fxproc/registry.hpp"
#include <memory>

namespace fxproc {
class MyFilter : public FilterBase {
public:
    std::string run(const std::string& in) override { /* ... */ return in; }
    std::string name() const override { return "my_filter"; }
};
}

extern "C" void fx_plugin_register(fxproc::Registry& reg) {
    reg.register_filter("my_filter", []() {
        return std::make_unique<fxproc::MyFilter>();
    });
}
```
