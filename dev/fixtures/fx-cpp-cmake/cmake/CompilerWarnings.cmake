# F06x: añade flags de warning agresivos para hacer visibles los bugs
# plantados como trampas (static init order, xmacro collision).
function(fxproc_set_warnings target)
    target_compile_options(${target} PRIVATE
        -Wall -Wextra -Wpedantic -Wshadow -Wnon-virtual-dtor
        -Wno-unused-parameter
    )
endfunction()
