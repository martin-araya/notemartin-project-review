pub mod entity;
pub mod service;
pub mod handler;

use axum::Router;
use axum::routing::{get, post, patch, delete};
use sqlx::SqlitePool;

pub fn routes(pool: SqlitePool) -> Router {
    Router::new()
        .route("/items", post(handler::create_item))
        .route("/items", get(handler::list_items))
        .route("/items/:id", get(handler::get_item))
        .route("/items/:id", patch(handler::update_item))
        .route("/items/:id", delete(handler::delete_item))
        .with_state(pool)
}
