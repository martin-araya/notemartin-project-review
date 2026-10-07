# GROUND_TRUTH — fx-cpp-qt

## Vision general

Fixture Qt 6 con Widgets y QML, build con CMake + qt_standard_project_setup. Demuestra las trampas clasicas del framework: `connect` signal/slot, auto-conexiones por nombre, widgets `.ui` (XML de Qt Designer), `Q_PROPERTY`/`Q_INVOKABLE` para QML, recursos `.qrc` con rutas `:/`, y codigo generado por `moc` desde `Q_OBJECT`. Cierra el bloque "Nativo y sistemas" (F06x–F06z).

## Stack

- C++20 con GCC 13.x
- Qt 6.4.2 LTS (Core, Gui, Widgets, Qml, Quick, QuickControls2, QuickWidgets, Test) instalado via apt en Debian bookworm
- CMake 3.25+ con `qt_standard_project_setup(REQUIRES 6.4)`
- `moc` + `uic` + `rcc` automaticos via `set(CMAKE_AUTOMOC ON)` + `set(CMAKE_AUTORCC ON)` + `set(CMAKE_AUTOUIC ON)`
- Tests Qt Test con `QTEST_GUILESS_MAIN` (sin GUI) + `QT_QPA_PLATFORM=offscreen`
- QML con `qt_add_qml_module` para registrar el modulo QtApp

## Features y R-NN

| Feature | R-NN | Cubre |
|---|---|---|
| `editor` | 7 | edicion basica, undo/redo, modified flag, status bar, save/open, error de save |
| `preferencias` | 7 | load desde QSettings, binding QML, dark theme, persist, reset, Q_INVOKABLE, error |
| `exportar` | 7 | text/HTML/Markdown, format desconocido, path no escribible, Q_INVOKABLE, loop prevenido |

## Trampas plantadas (CC-04..CC-06)

### Ecosistema (6/6)
1. **E01** `QObject::connect` en `src/main_window.cpp:50-72` entre `Editor::textChanged` y `QPlainTextEdit::setPlainText`, `Preferences::darkThemeChanged` y `qApp->setStyleSheet`, etc.
2. **E02** Slots `on_<objectName>_<signal>` en `MainWindow` (auto-connect) + `setupUi()` en el constructor.
3. **E03** `ui/main_window.ui` con `QMainWindow` + 4 `QPushButton` (saveButton, exitButton, exportButton, preferencesButton) + menu + toolbar.
4. **E04** `Q_PROPERTY fontSize/darkTheme` con `NOTIFY` + `Q_INVOKABLE resetToDefaults/save` + `PreferencesProxy` que expone a QML.
5. **E05** `resources/resources.qrc` con SVGs y styles + `qt_add_resources(qtapp_exe ...)` los compila con `rcc`.
6. **E06** Todos los headers con `Q_OBJECT` (editor, preferences, exporter, main_window, preferences_proxy) generan `moc_*.cpp` via AUTOMOC.

### Paquete (6/6)
1. **P01** `connect_5_args_no_explicit` documentado en comment de `setupConnections()`.
2. **P02** `signal_loop_infinite` con caso `format == "loop"` en `exporter.cpp:doExport` que NO emite nada.
3. **P03** `legacyProperty` (QString) sin `NOTIFY` en `preferences.h:21`.
4. **P04** `qrc_path_no_colon_slash` documentado en `test_p04_qrc_path_no_colon_slash`.
5. **P05** `on_savebutton_clicked_TYPO` con `b` minuscula mientras el objectName es `saveButton` (capital B).
6. **P06** `PreferencesProxy` no llama `setObjectOwnership(..., CppOwnership)`.

### Superficiales (3/3)
1. **S01** `someUnusedSignal` declarada y emitida en `editor.cpp` sin receptor.
2. **S02** Alias en `resources.qrc` que nadie usa.
3. **S03** 3 lineas comentadas con `TODO: connect` en `main_window.cpp:on_actionQuit_triggered`.

## Salida de la suite

29 tests Qt Test passing en `gcc:13-bookworm` con `apt-get install qt6-base-dev qt6-declarative-dev qt6-tools-dev qt6-tools-dev-tools libqt6test6 libqt6quick6 libqt6quickwidgets6 libqt6quickcontrols2-6` y `QT_QPA_PLATFORM=offscreen`:

- 4 tests de `Editor` (feature 1)
- 4 tests de `Preferences` (feature 2)
- 4 tests de `Exporter` (feature 3)
- 6 tests de trampas del ecosistema
- 6 tests de trampas del paquete
- 3 tests de trampas superficiales
- 1 test de cleanup

## Comandos para reproducir

```bash
docker build -f dev/fixtures/fx-cpp-qt/Dockerfile.test -t npr-fx-cpp-qt dev/fixtures/fx-cpp-qt
docker run --rm npr-fx-cpp-qt

# o via run_fixture_tests.py:
python dev/tools/run_fixture_tests.py --fixture fx-cpp-qt --container
```

## Comandos para regenerar la historia git

```bash
cd dev/fixtures/fx-cpp-qt
bash build-history.sh
```

Crea 8 commits incrementales.

## Notas de portabilidad

- El fixture corre nativamente en linux via Docker (`gcc:13-bookworm` con Qt 6.4 de apt).
- macOS requiere Qt 6 instalado via Homebrew; el `apt-get` no funciona.
- Windows no es soportado por el manifest (QtWidgets requiere display; CI usa `QT_QPA_PLATFORM=offscreen`).
- `arm-none-eabi-gcc` no se necesita (no compilamos a bare-metal).
