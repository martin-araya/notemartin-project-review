//! Trampa E02: blanket impl generica sobre cualquier tipo que
//! implemente Serialize.
//!
//! Cualquier struct que derive Serialize automaticamente satisface
//! `Json::to_json` via esta impl. La trampa: la firma generica
//! es invisible sin leer la firma completa.

use serde::Serialize;

pub trait Json {
    fn to_json(&self) -> String;
}

impl<T> Json for T
where
    T: Serialize,
{
    fn to_json(&self) -> String {
        serde_json::to_string(self).unwrap_or_default()
    }
}
