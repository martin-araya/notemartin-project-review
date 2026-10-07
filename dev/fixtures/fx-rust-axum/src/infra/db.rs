//! Conexion a la DB y migraciones con sqlx.
//!
//! Trampa P04: axum extractors en los handlers se ejecutan en
//! orden (State, Path, Json, etc.). Si un extractor falla, los
//! siguientes no se ejecutan.

use sqlx::sqlite::{SqlitePool, SqlitePoolOptions};

pub async fn connect_pool(database_url: &str) -> Result<SqlitePool, sqlx::Error> {
    let pool = SqlitePoolOptions::new()
        .max_connections(1)
        .connect(database_url)
        .await?;
    sqlx::migrate!("./migrations").run(&pool).await?;
    Ok(pool)
}
