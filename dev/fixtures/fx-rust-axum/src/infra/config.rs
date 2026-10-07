//! Configuracion desde env vars.
use std::env;

#[derive(Debug, Clone)]
pub struct Config {
    pub database_url: String,
    pub http_port: u16,
}

impl Config {
    pub fn from_env() -> Self {
        Self {
            database_url: env::var("DATABASE_URL")
                .unwrap_or_else(|_| "sqlite::memory:".to_string()),
            http_port: env::var("HTTP_PORT")
                .ok()
                .and_then(|s| s.parse().ok())
                .unwrap_or(8082),
        }
    }
}
