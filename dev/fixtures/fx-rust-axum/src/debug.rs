//! Trampa S03: dead debug helper.
//!
//! La funcion `debug_println` no se invoca en produccion; solo existe
//! para uso durante el desarrollo local.

pub fn debug_println(s: &str) {
    // Dead code: no se invoca en runtime. La skill debe detectarlo
    // via grep de "debug_println".
    eprintln!("[DEBUG] {}", s);
}
