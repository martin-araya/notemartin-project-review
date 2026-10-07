// Trampa E01: proc macro derive que genera un impl para structs.
//
// El derive #[derive(Entity)] invoca esta funcion en compile time
// y genera un impl con getter y setter para los campos del struct.
// La skill debe notar que `Item` (y los demas entities) usan
// este derive y los metodos get_*/set_* no estan declarados
// explicitamente: se generan via proc-macro.

use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput, Data};

#[proc_macro_derive(Entity)]
pub fn entity_derive(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = input.ident;

    // Genera un impl con un campo estatico ESTE_NOMBRE y un
    // metodo estatico nombre() que retorna &str.
    let expanded = quote! {
        impl #name {
            pub const ENTITY_NAME: &'static str = stringify!(#name);

            pub fn entity_name() -> &'static str {
                Self::ENTITY_NAME
            }
        }
    };

    expanded.into()
}
