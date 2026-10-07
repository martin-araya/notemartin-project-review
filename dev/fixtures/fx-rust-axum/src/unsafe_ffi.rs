//! Trampa E06: bloque unsafe con FFI.
//!
//! Declara funciones externas en C que se compilan pero no se enlazan
//! en el binario. La skill debe notar que `unsafe_ffi.rs` existe
//! y que las llamadas a `c_legacy_hash` usan bloque `unsafe`.

extern "C" {
    fn c_legacy_hash(input: *const u8, len: usize) -> u64;
}

/// Wrapper safe que usa la funcion C.
///
/// # Safety
/// `input` debe apuntar a un buffer valido de al menos `len` bytes.
pub unsafe fn legacy_hash(input: *const u8, len: usize) -> u64 {
    unsafe { c_legacy_hash(input, len) }
}
