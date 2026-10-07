# F06z: tests/CMakeLists.txt
enable_testing()

# Test runner: un solo binario con todos los tests Qt Test.
qt_add_executable(qtapp_tests
    test_main.cpp
)
set_target_properties(qtapp_tests PROPERTIES OUTPUT_NAME "qtapp_tests")
target_link_libraries(qtapp_tests PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
    Qt6::Qml
    Qt6::Quick
    Qt6::Test
    qtapp_core
)
target_include_directories(qtapp_tests PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_BINARY_DIR}/generated
)

# Sin GUI completa en CI: usar offscreen platform.
add_test(NAME qtapp_tests COMMAND qtapp_tests)
set_tests_properties(qtapp_tests PROPERTIES
    ENVIRONMENT "QT_QPA_PLATFORM=offscreen"
)
