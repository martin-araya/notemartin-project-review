use fxrust_axum::catalog;
use fxrust_axum::infra::db::connect_pool;

#[tokio::test]
async fn test_catalog_create_item_returns_201() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    let item = catalog::service::create_item(&pool, "SKU-001", "Widget", 1999)
        .await
        .expect("create_item");
    assert_eq!(item.sku, "SKU-001");
    assert_eq!(item.name, "Widget");
    assert_eq!(item.price_cents, 1999);
}

#[tokio::test]
async fn test_catalog_list_items_returns_all() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    catalog::service::create_item(&pool, "A", "Item A", 100)
        .await
        .expect("create A");
    catalog::service::create_item(&pool, "B", "Item B", 200)
        .await
        .expect("create B");
    let items = catalog::service::list_items(&pool).await.expect("list");
    assert!(items.len() >= 2);
}

#[tokio::test]
async fn test_catalog_get_item_returns_correct() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    let created = catalog::service::create_item(&pool, "X", "X-name", 500)
        .await
        .expect("create");
    let found = catalog::service::get_item(&pool, created.id)
        .await
        .expect("get");
    assert_eq!(found.sku, "X");
}

#[tokio::test]
async fn test_catalog_create_item_with_empty_sku_returns_error() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    let result = catalog::service::create_item(&pool, "  ", "name", 0).await;
    assert!(result.is_err());
}
