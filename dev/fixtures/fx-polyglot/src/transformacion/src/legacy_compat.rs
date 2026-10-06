//! Modulo `legacy_compat` (trampa del paquete #3: rellena campos faltantes
//! con defaults silenciosos, ocultando errores del llamador).
//! Compilado solo cuando la feature `legacy_compat` esta activa.

use serde_json::{json, Value};

pub fn default_for(field: &str) -> Value {
    match field {
        "raw" => json!(""),
        "payload" => json!(""),
        _ => Value::Null,
    }
}