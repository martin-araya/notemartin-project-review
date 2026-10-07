//! Handlers axum para prices.

use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};
use serde::Deserialize;
use sqlx::SqlitePool;

use crate::infra::error::AppError;

use super::service;

#[derive(Deserialize)]
pub struct CreatePriceReq {
    pub item_id: i64,
    pub amount_cents: i64,
    pub currency: String,
}

#[derive(Deserialize)]
pub struct UpdatePriceReq {
    pub amount_cents: i64,
}

pub async fn create_price(
    State(pool): State<SqlitePool>,
    Json(req): Json<CreatePriceReq>,
) -> Result<Json<crate::pricing::entity::Price>, AppError> {
    let price = service::create_price(&pool, req.item_id, req.amount_cents, &req.currency).await?;
    Ok(Json(price))
}

pub async fn list_prices(
    State(pool): State<SqlitePool>,
) -> Result<Json<Vec<crate::pricing::entity::Price>>, AppError> {
    Ok(Json(service::list_prices(&pool).await?))
}

pub async fn get_price(
    State(pool): State<SqlitePool>,
    Path(id): Path<i64>,
) -> Result<Json<crate::pricing::entity::Price>, AppError> {
    Ok(Json(service::get_price(&pool, id).await?))
}

pub async fn update_price(
    State(pool): State<SqlitePool>,
    Path(id): Path<i64>,
    Json(req): Json<UpdatePriceReq>,
) -> Result<Json<crate::pricing::entity::Price>, AppError> {
    Ok(Json(service::update_price(&pool, id, req.amount_cents).await?))
}

pub async fn delete_price(
    State(pool): State<SqlitePool>,
    Path(id): Path<i64>,
) -> Result<StatusCode, AppError> {
    service::delete_price(&pool, id).await?;
    Ok(StatusCode::NO_CONTENT)
}
