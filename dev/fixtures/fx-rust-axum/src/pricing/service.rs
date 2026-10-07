//! Logica de negocio de prices.

use sqlx::SqlitePool;

use crate::infra::error::AppError;

use super::entity::Price;

pub async fn list_prices(pool: &SqlitePool) -> Result<Vec<Price>, AppError> {
    let rows = sqlx::query_as::<_, Price>(
        "SELECT id, item_id, amount_cents, currency FROM prices ORDER BY id",
    )
    .fetch_all(pool)
    .await?;
    Ok(rows)
}

pub async fn get_price(pool: &SqlitePool, id: i64) -> Result<Price, AppError> {
    sqlx::query_as::<_, Price>(
        "SELECT id, item_id, amount_cents, currency FROM prices WHERE id = ?",
    )
    .bind(id)
    .fetch_optional(pool)
    .await?
    .ok_or_else(|| AppError::NotFound(format!("price {}", id)))
}

pub async fn create_price(
    pool: &SqlitePool,
    item_id: i64,
    amount_cents: i64,
    currency: &str,
) -> Result<Price, AppError> {
    if amount_cents < 0 {
        return Err(AppError::Invalid("amount must be >= 0".into()));
    }
    let result = sqlx::query("INSERT INTO prices (item_id, amount_cents, currency) VALUES (?, ?, ?)")
        .bind(item_id)
        .bind(amount_cents)
        .bind(currency)
        .execute(pool)
        .await?;
    let id = result.last_insert_rowid();
    get_price(pool, id).await
}

pub async fn update_price(
    pool: &SqlitePool,
    id: i64,
    amount_cents: i64,
) -> Result<Price, AppError> {
    sqlx::query("UPDATE prices SET amount_cents = ? WHERE id = ?")
        .bind(amount_cents)
        .bind(id)
        .execute(pool)
        .await?;
    get_price(pool, id).await
}

pub async fn delete_price(pool: &SqlitePool, id: i64) -> Result<(), AppError> {
    sqlx::query("DELETE FROM prices WHERE id = ?")
        .bind(id)
        .execute(pool)
        .await?;
    Ok(())
}
