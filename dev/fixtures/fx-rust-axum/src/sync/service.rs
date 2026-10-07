//! Logica de negocio de sync.

use sqlx::SqlitePool;

use crate::infra::error::AppError;

use super::entity::SyncJob;

pub async fn list_jobs(pool: &SqlitePool) -> Result<Vec<SyncJob>, AppError> {
    let rows = sqlx::query_as::<_, SyncJob>(
        "SELECT id, payload, status FROM sync_jobs ORDER BY id",
    )
    .fetch_all(pool)
    .await?;
    Ok(rows)
}

pub async fn get_job(pool: &SqlitePool, id: i64) -> Result<SyncJob, AppError> {
    sqlx::query_as::<_, SyncJob>("SELECT id, payload, status FROM sync_jobs WHERE id = ?")
        .bind(id)
        .fetch_optional(pool)
        .await?
        .ok_or_else(|| AppError::NotFound(format!("job {}", id)))
}

pub async fn create_job(pool: &SqlitePool, payload: &str) -> Result<SyncJob, AppError> {
    if payload.trim().is_empty() {
        return Err(AppError::Invalid("payload is empty".into()));
    }
    let result = sqlx::query("INSERT INTO sync_jobs (payload, status) VALUES (?, 'pending')")
        .bind(payload)
        .execute(pool)
        .await?;
    let id = result.last_insert_rowid();
    get_job(pool, id).await
}

pub async fn complete_job(pool: &SqlitePool, id: i64) -> Result<SyncJob, AppError> {
    sqlx::query("UPDATE sync_jobs SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?")
        .bind(id)
        .execute(pool)
        .await?;
    get_job(pool, id).await
}
