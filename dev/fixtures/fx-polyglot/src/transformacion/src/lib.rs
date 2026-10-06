//! Implementacion real del binario de Rust. Las distintas ramas estan
//! controladas por las features de Cargo (trampa #3 del ecosistema).

use serde_json::{json, Map, Value};
use std::process::ExitCode;

#[cfg(feature = "strict")]
mod strict;
#[cfg(feature = "legacy_compat")]
mod legacy_compat;

/// Parsea una linea JSON. Devuelve el Value o un error.
pub fn parse_line(line: &str) -> Result<Value, String> {
    serde_json::from_str(line).map_err(|e| e.to_string())
}

/// Transforma segun las features activas. El campo de entrada esperado cambia:
///   v1 (default) -> lee `.raw`
///   v2           -> lee `.payload`
/// El campo de salida siempre es `transformed`.
pub fn transform(parsed: Value) -> Result<Value, Result<Map<String, Value>, ExitCode>> {
    let mut out = Map::new();
    let obj = match parsed.as_object() {
        Some(o) => o,
        None => {
            return Err(Ok(Map::from_iter([(
                "error".into(),
                Value::String("no es objeto".into()),
            )])))
        }
    };

    let id = obj
        .get("id")
        .cloned()
        .unwrap_or_else(|| Value::String(String::new()));
    out.insert("id".into(), id);

    // Rejection de campos extra con strict (trampa #5: campos extra ignorados
    // en v1 sin strict, rechazados con strict).
    #[cfg(feature = "strict")]
    {
        if strict::has_unknown_fields(obj) {
            eprintln!("campo extra detectado (exit 64)");
            return Err(Err(ExitCode::from(64)));
        }
    }

    // Seleccion del campo de entrada segun la feature.
    #[cfg(feature = "v2")]
    let input_field = "payload";
    #[cfg(not(feature = "v2"))]
    let input_field = "raw";

    let raw_value = if obj.contains_key(input_field) {
        obj.get(input_field).cloned().unwrap_or(Value::Null)
    } else {
        #[cfg(feature = "legacy_compat")]
        {
            legacy_compat::default_for(input_field)
        }
        #[cfg(not(feature = "legacy_compat"))]
        {
            Value::Null
        }
    };

    let raw_str = raw_value.as_str().unwrap_or("").to_string();
    let suffix = {
        #[cfg(feature = "v2")]
        {
            "::v2"
        }
        #[cfg(not(feature = "v2"))]
        {
            "::v1"
        }
    };
    out.insert(
        "transformed".into(),
        Value::String(format!("{}{}", raw_str, suffix)),
    );

    // Marca la feature usada para que el orquestador la pueda mostrar.
    let feature_marker = {
        #[cfg(feature = "v2")]
        {
            "v2"
        }
        #[cfg(not(feature = "v2"))]
        {
            "v1"
        }
    };
    out.insert("via".into(), Value::String(feature_marker.into()));

    Ok(Value::Object(out))
}