//! Modulo `strict` (trampa del paquete: campos extra son rechazados).
//! Compilado solo cuando la feature `strict` esta activa.

use serde_json::{Map, Value};

const KNOWN_FIELDS: &[&str] = &["id", "raw", "payload"];

pub fn has_unknown_fields(obj: &Map<String, Value>) -> bool {
    obj.keys().any(|k| !KNOWN_FIELDS.contains(&k.as_str()))
}