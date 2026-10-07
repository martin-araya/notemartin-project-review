use fxrust_axum::infra::db::connect_pool;
use fxrust_axum::pricing;

#[tokio::test]
async fn test_pricing_create_price_returns_correct() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    let price = pricing::service::create_price(&pool, 1, 1999, "USD")
        .await
        .expect("create_price");
    assert_eq!(price.item_id, 1);
    assert_eq!(price.amount_cents, 1999);
    assert_eq!(price.currency, "USD");
}

#[tokio::test]
async fn test_pricing_list_prices_returns_all() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    pricing::service::create_price(&pool, 1, 100, "USD")
        .await
        .expect("create1");
    pricing::service::create_price(&pool, 2, 200, "EUR")
        .await
        .expect("create2");
    let prices = pricing::service::list_prices(&pool).await.expect("list");
    assert!(prices.len() >= 2);
}

#[tokio::test]
async fn test_pricing_get_price_returns_correct() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    let created = pricing::service::create_price(&pool, 5, 500, "USD")
        .await
        .expect("create");
    let found = pricing::service::get_price(&pool, created.id)
        .await
        .expect("get");
    assert_eq!(found.amount_cents, 500);
}

#[tokio::test]
async fn test_pricing_create_with_negative_amount_returns_error() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    let result = pricing::service::create_price(&pool, 1, -100, "USD").await;
    assert!(result.is_err());
}
