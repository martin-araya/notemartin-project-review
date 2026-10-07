use fxrust_axum::infra::db::connect_pool;
use fxrust_axum::sync;

#[tokio::test]
async fn test_sync_create_job_returns_correct() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    let job = sync::service::create_job(&pool, "test payload")
        .await
        .expect("create_job");
    assert_eq!(job.payload, "test payload");
    assert_eq!(job.status, "pending");
}

#[tokio::test]
async fn test_sync_list_jobs_returns_all() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    sync::service::create_job(&pool, "job1").await.expect("create1");
    sync::service::create_job(&pool, "job2").await.expect("create2");
    let jobs = sync::service::list_jobs(&pool).await.expect("list");
    assert!(jobs.len() >= 2);
}

#[tokio::test]
async fn test_sync_complete_job_sets_status() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    let created = sync::service::create_job(&pool, "to-complete")
        .await
        .expect("create");
    let completed = sync::service::complete_job(&pool, created.id)
        .await
        .expect("complete");
    assert_eq!(completed.status, "completed");
}

#[tokio::test]
async fn test_sync_create_with_empty_payload_returns_error() {
    let pool = connect_pool("sqlite::memory:").await.expect("pool");
    let result = sync::service::create_job(&pool, "").await;
    assert!(result.is_err());
}
