//! Logica de negocio del catalog.
//!
//! Trampa E05: el `?` operator usa las `From` derivations de AppError
//! para convertir `sqlx::Error` en `AppError::Db` automaticamente.

use sqlx::SqlitePool;

use crate::infra::error::AppError;

use super::entity::Item;

pub async fn list_items(pool: &SqlitePool) -> Result<Vec<Item>, AppError> {
    let rows = sqlx::query_as::<_, Item>("SELECT id, sku, name, price_cents FROM items ORDER BY id")
        .fetch_all(pool)
        .await?;
    Ok(rows)
}

pub async fn get_item(pool: &SqlitePool, id: i64) -> Result<Item, AppError> {
    let row = sqlx::query_as::<_, Item>(
        "SELECT id, sku, name, price_cents FROM items WHERE id = ?",
    )
    .bind(id)
    .fetch_optional(pool)
    .await?
    .ok_or_else(|| AppError::NotFound(format!("item {}", id)))?;
    Ok(row)
}

pub async fn create_item(
    pool: &SqlitePool,
    sku: &str,
    name: &str,
    price_cents: i64,
) -> Result<Item, AppError> {
    if sku.trim().is_empty() {
        return Err(AppError::Invalid("sku is empty".into()));
    }
    let result = sqlx::query("INSERT INTO items (sku, name, price_cents) VALUES (?, ?, ?)")
        .bind(sku)
        .bind(name)
        .bind(price_cents)
        .execute(pool)
        .await?;
    let id = result.last_insert_rowid();
    let item = get_item(pool, id).await?;
    Ok(item)
}

pub async fn update_item(
    pool: &SqlitePool,
    id: i64,
    name: &str,
    price_cents: i64,
) -> Result<Item, AppError> {
    sqlx::query("UPDATE items SET name = ?, price_cents = ? WHERE id = ?")
        .bind(name)
        .bind(price_cents)
        .bind(id)
        .execute(pool)
        .await?;
    get_item(pool, id).await
}

pub async fn delete_item(pool: &SqlitePool, id: i64) -> Result<(), AppError> {
    sqlx::query("DELETE FROM items WHERE id = ?")
        .bind(id)
        .execute(pool)
        .await?;
    Ok(())
}
