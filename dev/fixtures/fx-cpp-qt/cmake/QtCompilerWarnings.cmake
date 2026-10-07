# F06z: QtCompilerWarnings.cmake - flags de warning para Qt.
function(qtapp_set_warnings target)
    target_compile_options(${target} PRIVATE
        -Wall -Wextra -Wpedantic -Wshadow -Wnon-virtual-dtor
        -Wno-unused-parameter
    )
endfunction()
