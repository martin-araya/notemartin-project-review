# F06z: CMakeLists.txt - build de la aplicacion Qt 6.
# E04: usa qt_standard_project_setup (Qt 6.5+) que configura automatic
# CMake AUTOMOC/AUTORCC/AUTOUIC.

cmake_minimum_required(VERSION 3.25)
project(qtapp VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
# AUTOMOC/AUTORCC/AUTOUIC se activan globalmente y a nivel de target.
# Esto es necesario porque qt_add_library en Qt 6.4 no propaga
# AUTOMOC a la libreria qtapp_core que contiene los QObjects.
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

# E01/E06: find_package(Qt6) + qt_standard_project_setup. Esto configura
# AUTOMOC, AUTORCC, AUTOUIC de manera idempotente.
# Debian bookworm trae Qt 6.4.2; usamos 6.4 como minimo.
find_package(Qt6 6.4 REQUIRED COMPONENTS Core Gui Widgets Qml Quick QuickControls2 QuickWidgets Test)

qt_standard_project_setup(REQUIRES 6.4)

# E01..E06: creamos qtapp_core como libreria estatica con todos los
# QObjects (Editor, Preferences, Exporter, MainWindow, PreferencesProxy).
# Esto permite que los tests y el binario principal compartan los
# simbolos generados por moc.
#
# IMPORTANTE: pasamos explicitamente los headers para que AUTOMOC los
# procese. Sin esto, qt_add_library no genera moc_*.cpp para los
# QObjects que solo aparecen via include en los .cpp.
qt_add_library(qtapp_core STATIC
    src/editor.cpp
    src/preferences.cpp
    src/exporter.cpp
    src/main_window.cpp
    src/preferences_proxy.cpp
    include/qtapp/editor.h
    include/qtapp/preferences.h
    include/qtapp/exporter.h
    include/qtapp/main_window.h
    include/qtapp/preferences_proxy.h
)
target_include_directories(qtapp_core PUBLIC
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_BINARY_DIR}/generated
)
target_link_libraries(qtapp_core PUBLIC
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
    Qt6::Qml
    Qt6::Quick
    Qt6::QuickControls2
    Qt6::QuickWidgets
)
# E03: AUTOUIC busca los .ui en el mismo dir que el .cpp que los incluye.
# Anadimos ui/ a los search paths.
target_include_directories(qtapp_core PRIVATE ${CMAKE_SOURCE_DIR}/ui)
set_target_properties(qtapp_core PROPERTIES
    AUTOUIC_SEARCH_PATHS "${CMAKE_SOURCE_DIR}/ui"
)

# Genera el ejecutable principal.
qt_add_executable(qtapp_exe src/main.cpp)
target_link_libraries(qtapp_exe PRIVATE qtapp_core)

# E05: registra el archivo de recursos resources/resources.qrc.
# AUTORCC genera qrc_resources.cpp automaticamente.
qt_add_resources(qtapp_exe "resources"
    PREFIX "/"
    FILES
        resources/icons/save.svg
        resources/icons/open.svg
        resources/icons/export.svg
        resources/styles/app.qss
)

# E03: genera ui_main_window.h desde ui/main_window.ui.
# AUTOUIC lo hace automaticamente. Anadimos ui/ a los search paths
# de qtapp_core y del ejecutable principal.
set_target_properties(qtapp_core PROPERTIES
    AUTOUIC_SEARCH_PATHS "${CMAKE_SOURCE_DIR}/ui"
)

# E04: modulo QML para PreferencesPage.qml + ThemeSwitcher.qml.
# IMPORTANTE: el URI del modulo genera un directorio `qtapp/` con los QML
# compilados. Por eso renombramos el ejecutable a `qtapp_exe` para evitar
# colision.
qt_add_qml_module(qtapp
    URI QtApp
    VERSION 1.0
    QML_FILES
        qml/PreferencesPage.qml
        qml/ThemeSwitcher.qml
)

# Tests Qt Test.
enable_testing()
add_subdirectory(tests)
