# fx-cpp-qt

Aplicacion de escritorio Qt 6 con Widgets y QML. Demuestra las trampas clasicas del framework: `connect` signal/slot, auto-conexiones por nombre, widgets `.ui`, `Q_PROPERTY`/`Q_INVOKABLE` para QML, recursos `.qrc` con rutas `:/`, y codigo generado por `moc` desde `Q_OBJECT`.

## Stack

- C++20 con GCC 13.x
- Qt 6.6 LTS (Core, Gui, Widgets, Qml, Quick, QuickControls2, Test)
- CMake 3.25+ con `qt_standard_project_setup`
- `moc`, `uic`, `rcc` automaticos via Qt 6.5+ targets
- Tests con Qt Test + `QT_QPA_PLATFORM=offscreen` (sin X11)
- Ubuntu/Debian via paquetes `qt6-base-dev` etc.

## Features

- `editor`: edicion de texto con status bar, undo/redo, save/open
- `preferencias`: panel QML embebido con `Q_PROPERTY` + `QSettings`
- `exportar`: persistencia a texto/HTML/Markdown via `QFileDialog`

## Comandos

```bash
make test    # cmake + build + tests Qt Test via Python runner
make build   # solo compila
make clean   # borra build/
```

## Contenedor

```bash
python dev/tools/run_fixture_tests.py --fixture fx-cpp-qt --container
```

Imagen: `gcc:13-bookworm` con `qt6-base-dev`, `qt6-declarative-dev`, `qt6-tools-dev`, `qt6-qpa-plugins`.
