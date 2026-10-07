# E05: plugin de ejemplo que se compila como .so aparte.
# P05: este target se construye siempre, incluso si FX_HAS_PLUGINS=OFF.

add_library(transform_json SHARED transform_json.cpp)
target_include_directories(transform_json PUBLIC
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_BINARY_DIR}/generated
)
target_link_libraries(transform_json PUBLIC ${CMAKE_DL_LIBS})
set_target_properties(transform_json PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/plugins
    PREFIX "lib"
)
