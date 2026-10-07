# Qt Build — F06z

## Toolchain

- Qt 6.6 LTS via `qt6-base-dev`, `qt6-declarative-dev`, `qt6-tools-dev`, `qt6-tools-dev-tools`
- `libqt6test6` (runtime) — no hay `-dev` package en Debian bookworm
- GCC 13.x + CMake 3.25+
- Linux + xcb/offscreen platform plugin (CI usa offscreen)

## Estructura de build

```
build/
├── qtapp_exe                       # binario principal
├── libqtapp_core.a                 # libreria con los QObjects
├── tests/qtapp_tests                # binario de tests
├── qtapp/                          # QML module cacheado
└── qtapp_core_autogen/             # codigo moc generado
```

## Targets

- `make test` — cmake + build + ctest con `QT_QPA_PLATFORM=offscreen`
- `make build` — solo compilar
- `make clean` — borra build/

## Trampas que el build expone

El proceso de build genera codigo que la skill debe reconocer:

- `moc_*.cpp` (E06) generado por `moc` a partir de headers con `Q_OBJECT`
- `ui_main_window.h` (E03) generado por `uic` desde `ui/main_window.ui`
- `qrc_*.cpp` (E05) generado por `rcc` desde `resources/resources.qrc`
- `qtapp_qmltyperegistrations.cpp` y `qmlcache/qtapp_qml/*.cpp` (E04) generado por `qmltyperegistrar` y `qmlcachegen` desde los archivos `.qml`
