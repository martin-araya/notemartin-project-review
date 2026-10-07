pub mod entity;
pub mod service;
pub mod handler;

use axum::Router;
use axum::routing::{get, post};
use sqlx::SqlitePool;

pub fn routes(pool: SqlitePool) -> Router {
    Router::new()
        .route("/jobs", post(handler::create_job))
        .route("/jobs", get(handler::list_jobs))
        .route("/jobs/:id", get(handler::get_job))
        .route("/jobs/:id/complete", post(handler::complete_job))
        .with_state(pool)
}
