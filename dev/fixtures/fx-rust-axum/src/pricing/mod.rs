pub mod entity;
pub mod service;
pub mod handler;

use axum::Router;
use axum::routing::{get, post, patch, delete};
use sqlx::SqlitePool;

pub fn routes(pool: SqlitePool) -> Router {
    Router::new()
        .route("/prices", post(handler::create_price))
        .route("/prices", get(handler::list_prices))
        .route("/prices/:id", get(handler::get_price))
        .route("/prices/:id", patch(handler::update_price))
        .route("/prices/:id", delete(handler::delete_price))
        .with_state(pool)
}
