//! Transformacion poliglota (F06f). Lee JSON por stdin, transforma segun la
//! combinacion de features de Cargo seleccionadas, y escribe JSON por stdout.
//!
//! Features:
//! - `v1` (default): lee {id, raw}, emite {id, transformed: raw + "::v1"}.
//! - `v2`: lee {id, payload}, emite {id, transformed: payload + "::v2"}.
//! - `strict`: rechaza campos extra con exit 64.
//! - `legacy_compat`: rellena campos faltantes con defaults silenciosos.

use std::io::{self, BufRead, Write};
use std::process::ExitCode;

mod lib;

fn main() -> ExitCode {
    let stdin = io::stdin();
    let stdout = io::stdout();
    let mut out = stdout.lock();

    for line_res in stdin.lock().lines() {
        let line = match line_res {
            Ok(l) => l,
            Err(_) => return ExitCode::from(5),
        };
        if line.trim().is_empty() {
            eprintln!("linea vacia (exit 2)");
            return ExitCode::from(2);
        }
        let parsed = match lib::parse_line(&line) {
            Ok(v) => v,
            Err(e) => {
                eprintln!("json malformado: {} (exit 8)", e);
                return ExitCode::from(8);
            }
        };
        let out_obj = match lib::transform(parsed) {
            Ok(v) => v,
            Err(e) => return e,
        };
        match serde_json::to_string(&out_obj) {
            Ok(s) => {
                if let Err(_) = writeln!(out, "{}", s) {
                    return ExitCode::from(5);
                }
            }
            Err(_) => return ExitCode::from(5),
        }
    }
    ExitCode::from(0)
}