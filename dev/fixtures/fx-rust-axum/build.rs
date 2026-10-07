// Trampa E06: build script que se ejecuta en compile time.
// Imprime un warning que se ve en `cargo build`.
fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:warning=fxrust-axum build script executed");
}
