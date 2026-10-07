//! Entidad SyncJob.

use fxrust_derive::Entity;
use serde::{Deserialize, Serialize};
use sqlx::FromRow;

#[derive(Entity, Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct SyncJob {
    pub id: i64,
    pub payload: String,
    pub status: String,
}
