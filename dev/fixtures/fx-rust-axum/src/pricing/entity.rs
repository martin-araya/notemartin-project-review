//! Entidad Price.

use fxrust_derive::Entity;
use serde::{Deserialize, Serialize};
use sqlx::FromRow;

#[derive(Entity, Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct Price {
    pub id: i64,
    pub item_id: i64,
    pub amount_cents: i64,
    pub currency: String,
}
