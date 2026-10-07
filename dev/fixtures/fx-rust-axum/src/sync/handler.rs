//! Handlers axum para sync.

use axum::{
    extract::{Path, State},
    Json,
};
use serde::Deserialize;
use sqlx::SqlitePool;

use crate::infra::error::AppError;

use super::service;

#[derive(Deserialize)]
pub struct CreateJobReq {
    pub payload: String,
}

pub async fn create_job(
    State(pool): State<SqlitePool>,
    Json(req): Json<CreateJobReq>,
) -> Result<Json<crate::sync::entity::SyncJob>, AppError> {
    Ok(Json(service::create_job(&pool, &req.payload).await?))
}

pub async fn list_jobs(
    State(pool): State<SqlitePool>,
) -> Result<Json<Vec<crate::sync::entity::SyncJob>>, AppError> {
    Ok(Json(service::list_jobs(&pool).await?))
}

pub async fn get_job(
    State(pool): State<SqlitePool>,
    Path(id): Path<i64>,
) -> Result<Json<crate::sync::entity::SyncJob>, AppError> {
    Ok(Json(service::get_job(&pool, id).await?))
}

pub async fn complete_job(
    State(pool): State<SqlitePool>,
    Path(id): Path<i64>,
) -> Result<Json<crate::sync::entity::SyncJob>, AppError> {
    Ok(Json(service::complete_job(&pool, id).await?))
}
