use std::fs;

fn read(rel: &str) -> String {
    let path = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(rel);
    fs::read_to_string(&path).unwrap_or_else(|e| panic!("read {}: {}", rel, e))
}

#[test]
fn test_s01_dead_debug_helper() {
    // Trampa S03: dead debug helper.
    let debug = read("src/debug.rs");
    assert!(debug.contains("pub fn debug_println"));
    // Verificar que no se usa en el codigo de produccion.
    let server = read("src/bin/server.rs");
    assert!(!server.contains("debug_println"));
}

#[test]
fn test_s02_dead_legacy_feature() {
    // Trampa S02: codigo gated por feature legacy.
    let legacy = read("src/features_legacy.rs");
    assert!(legacy.contains("LegacyEvent"));
    assert!(legacy.contains("#[cfg(feature = \"legacy\")]"));
}

#[test]
fn test_s03_dead_unused_function() {
    // Trampa S03: dead debug helper.
    // (Cubierto por test_s01.) Ademas verificamos que
    // features_legacy tiene un metodo que solo se compila
    // con --features legacy.
    let legacy = read("src/features_legacy.rs");
    assert!(legacy.contains("pub fn hash"));
}
