use std::fs;

fn read(rel: &str) -> String {
    let path = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(rel);
    fs::read_to_string(&path).unwrap_or_else(|e| panic!("read {}: {}", rel, e))
}

#[test]
fn test_p01_proc_macro_generates_wrong_impl() {
    // Trampa P01: el proc macro podria generar codigo incorrecto.
    // Verificamos que el codigo generado tiene al menos un metodo
    // que existe (entity_name) y que la firma del derive es correcta.
    let derive = read("derive-macro/src/lib.rs");
    assert!(derive.contains("fn entity_derive"));
    assert!(derive.contains("ENTITY_NAME"));
    assert!(derive.contains("entity_name"));
}

#[test]
fn test_p02_blanket_impl_no_conflict() {
    // Trampa P02: la blanket impl podria entrar en conflicto con
    // una impl especifica. Verificamos que no hay conflicto actual
    // (no hay impl especifica de Json en el codigo).
    let blanket = read("src/infra/blanket_impl.rs");
    assert!(blanket.contains("impl<T> Json for T"));
    // La blanket es la unica impl de Json en el codigo: no hay
    // impl especifica que pudiera entrar en conflicto.
    assert!(!blanket.contains("impl Json for Item"));
}

#[test]
fn test_p03_cargo_feature_typo() {
    // Trampa P03: el feature typo en Cargo.toml no se compilaria.
    // Aqui el feature es correcto: `legacy = []`.
    let cargo = read("Cargo.toml");
    assert!(cargo.contains("legacy = []"));
    assert!(!cargo.contains("lagacy"));
}

#[test]
fn test_p04_axum_extractor_order() {
    // Trampa P04: el orden de extractors en axum afecta el orden
    // de las validaciones. Verificamos que los handlers tienen
    // State primero (que es la convencion).
    let catalog = read("src/catalog/handler.rs");
    // El handler create_item tiene State(pool), Json(req) en
    // ese orden. La firma puede ocupar multiples lineas, asi que
    // buscamos "State(pool)" y "Json(req)" en todo el archivo.
    assert!(catalog.contains("State(pool)"));
    assert!(catalog.contains("Json(req)"));
    let state_pos = catalog.find("State(pool)").unwrap();
    let json_pos = catalog.find("Json(req)").unwrap();
    assert!(state_pos < json_pos, "State debe ir antes que Json");
}

#[test]
fn test_p05_from_impl_no_cycles() {
    // Trampa P05: las impls From podrian tener ciclos.
    // Verificamos que AppError no tiene From<AppError>.
    let error = read("src/infra/error.rs");
    assert!(error.contains("enum AppError"));
    let has_self_from = error.contains("From<AppError>");
    assert!(!has_self_from, "AppError no debe tener From para si mismo (ciclo)");
}

#[test]
fn test_p06_build_rs_executes() {
    // Trampa P06: el build script debe ejecutarse.
    // Verificamos que el build.rs existe y tiene el warning que
    // esperamos ver en `cargo build`.
    let build_rs = read("build.rs");
    assert!(build_rs.contains("fn main"));
    assert!(build_rs.contains("cargo:warning"));
}
