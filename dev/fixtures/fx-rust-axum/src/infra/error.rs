//! Trampa E05: error con `From` derivations para usar `?` operator.
//!
//! El operador `?` en los servicios usa automaticamente las
//! implementaciones `From` derivadas por `thiserror` para
//! convertir `sqlx::Error` y otros errores en `AppError`.
//! La skill debe notar las `#[from]` y los `?` en el codigo.

use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("not found: {0}")]
    NotFound(String),

    #[error("db error: {0}")]
    Db(#[from] sqlx::Error),

    #[error("invalid input: {0}")]
    Invalid(String),

    #[error("internal error: {0}")]
    Internal(#[from] anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, code) = match &self {
            AppError::NotFound(_) => (StatusCode::NOT_FOUND, "not_found"),
            AppError::Db(_) => (StatusCode::INTERNAL_SERVER_ERROR, "db_error"),
            AppError::Invalid(_) => (StatusCode::BAD_REQUEST, "invalid_input"),
            AppError::Internal(_) => (StatusCode::INTERNAL_SERVER_ERROR, "internal_error"),
        };
        let body = Json(json!({
            "error": code,
            "message": self.to_string(),
        }));
        (status, body).into_response()
    }
}
