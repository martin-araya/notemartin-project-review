use std::fs;

fn read(rel: &str) -> String {
    let path = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(rel);
    fs::read_to_string(&path).unwrap_or_else(|e| panic!("read {}: {}", rel, e))
}

#[test]
fn test_e01_proc_macro_derive() {
    // Trampa E01: el proc macro `Entity` genera impl en compile time.
    let lib_rs = read("derive-macro/src/lib.rs");
    assert!(lib_rs.contains("proc_macro_derive(Entity)"));
    assert!(lib_rs.contains("TokenStream"));

    // Los entities usan #[derive(Entity)].
    let catalog = read("src/catalog/entity.rs");
    assert!(catalog.contains("#[derive(Entity"));
    assert!(catalog.contains("fxrust_derive::Entity"));
}

#[test]
fn test_e02_blanket_impl() {
    // Trampa E02: blanket impl sobre cualquier tipo que implemente Serialize.
    let blanket = read("src/infra/blanket_impl.rs");
    assert!(blanket.contains("impl<T>"));
    assert!(blanket.contains("T: Serialize"));
    assert!(blanket.contains("Json for T"));
}

#[test]
fn test_e03_cargo_features() {
    // Trampa E03: cargo features con #[cfg(feature = "legacy")].
    let cargo = read("Cargo.toml");
    assert!(cargo.contains("[features]"));
    assert!(cargo.contains("legacy"));

    let legacy = read("src/features_legacy.rs");
    assert!(legacy.contains("#[cfg(feature = \"legacy\")]"));
}

#[test]
fn test_e04_axum_extractors() {
    // Trampa E04: extractors de axum en las firmas de los handlers.
    let catalog_handler = read("src/catalog/handler.rs");
    assert!(catalog_handler.contains("State(pool)"));
    assert!(catalog_handler.contains("Json(req)"));
    assert!(catalog_handler.contains("Path(id)"));

    let pricing_handler = read("src/pricing/handler.rs");
    assert!(pricing_handler.contains("State(pool)"));
    assert!(pricing_handler.contains("Json(req)"));
}

#[test]
fn test_e05_error_flow_question() {
    // Trampa E05: error con From derivations y `?` operator.
    let error = read("src/infra/error.rs");
    assert!(error.contains("#[derive(Error"));
    assert!(error.contains("thiserror::Error"));
    assert!(error.contains("#[from]"));
    assert!(error.contains("impl IntoResponse"));

    // El operador ? se usa en los services.
    let service = read("src/catalog/service.rs");
    assert!(service.contains("?"));
}

#[test]
fn test_e06_build_rs_and_unsafe_ffi() {
    // Trampa E06: build.rs y bloque unsafe con FFI.
    let build_rs = read("build.rs");
    assert!(build_rs.contains("fn main()"));
    assert!(build_rs.contains("cargo:rerun-if-changed=build.rs"));

    let unsafe_ffi = read("src/unsafe_ffi.rs");
    assert!(unsafe_ffi.contains("extern \"C\""));
    assert!(unsafe_ffi.contains("unsafe"));
    assert!(unsafe_ffi.contains("c_legacy_hash"));
}
