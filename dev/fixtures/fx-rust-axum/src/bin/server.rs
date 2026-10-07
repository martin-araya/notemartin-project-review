//! Entry point binario del servidor.
//!
//! Trampa E04: axum::serve arranca el router con el pool compartido.
//! Los extractors de los handlers (State, Json, Path, Query) se
//! ejecutan en orden durante el dispatch.

use std::net::SocketAddr;

use fxrust_axum::catalog;
use fxrust_axum::infra::{config::Config, db::connect_pool};
use fxrust_axum::pricing;
use fxrust_axum::sync;

use axum::Router;
use tokio::net::TcpListener;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cfg = Config::from_env();
    eprintln!("connecting to {}", cfg.database_url);
    let pool = connect_pool(&cfg.database_url).await?;
    let addr = SocketAddr::from(([0, 0, 0, 0], cfg.http_port));

    let app = Router::new()
        .nest("/catalog", catalog::routes(pool.clone()))
        .nest("/pricing", pricing::routes(pool.clone()))
        .nest("/sync", sync::routes(pool.clone()));

    let listener = TcpListener::bind(addr).await?;
    eprintln!("listening on {}", addr);
    axum::serve(listener, app).await?;
    Ok(())
}
