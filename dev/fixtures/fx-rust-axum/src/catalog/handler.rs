//! Handlers axum con extractors (E04).
//!
//! Los extractors (State, Json, Path, Query) se ejecutan en orden
//! durante el dispatch. Si uno falla, los siguientes no corren y
//! axum responde 400 o 422.

use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::IntoResponse,
    Json,
};
use serde::{Deserialize, Serialize};
use sqlx::SqlitePool;

use crate::infra::error::AppError;

use super::entity::Item;
use super::service;

#[derive(Deserialize)]
pub struct CreateItemReq {
    pub sku: String,
    pub name: String,
    pub price_cents: i64,
}

#[derive(Deserialize)]
pub struct UpdateItemReq {
    pub name: String,
    pub price_cents: i64,
}

pub async fn create_item(
    State(pool): State<SqlitePool>,
    Json(req): Json<CreateItemReq>,
) -> Result<impl IntoResponse, AppError> {
    let item = service::create_item(&pool, &req.sku, &req.name, req.price_cents).await?;
    Ok((StatusCode::CREATED, Json(item)))
}

pub async fn list_items(
    State(pool): State<SqlitePool>,
) -> Result<Json<Vec<Item>>, AppError> {
    let items = service::list_items(&pool).await?;
    Ok(Json(items))
}

pub async fn get_item(
    State(pool): State<SqlitePool>,
    Path(id): Path<i64>,
) -> Result<Json<Item>, AppError> {
    let item = service::get_item(&pool, id).await?;
    Ok(Json(item))
}

pub async fn update_item(
    State(pool): State<SqlitePool>,
    Path(id): Path<i64>,
    Json(req): Json<UpdateItemReq>,
) -> Result<Json<Item>, AppError> {
    let item = service::update_item(&pool, id, &req.name, req.price_cents).await?;
    Ok(Json(item))
}

pub async fn delete_item(
    State(pool): State<SqlitePool>,
    Path(id): Path<i64>,
) -> Result<StatusCode, AppError> {
    service::delete_item(&pool, id).await?;
    Ok(StatusCode::NO_CONTENT)
}
