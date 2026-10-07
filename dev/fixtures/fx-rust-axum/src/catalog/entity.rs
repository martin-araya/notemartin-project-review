//! Entidad Item con proc macro derive custom (E01).
//!
//! El derive `Entity` invoca el proc macro `entity_derive` que genera
//! un `impl` con `ENTITY_NAME` y `entity_name()`. La skill debe
//! notar que estos metodos NO estan declarados aqui; se generan
//! en compile time.

use fxrust_derive::Entity;
use serde::{Deserialize, Serialize};
use sqlx::FromRow;

#[derive(Entity, Debug, Clone, Serialize, Deserialize, FromRow)]
pub struct Item {
    pub id: i64,
    pub sku: String,
    pub name: String,
    pub price_cents: i64,
}
