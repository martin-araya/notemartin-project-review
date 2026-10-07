require "sidekiq"

# En test/desarrollo usamos un cliente Redis simulado en proceso; en
# produccion esperariamos REDIS_URL apuntando a un Redis real.
if Rails.env.test? || Rails.env.development?
  require "mock_redis"
  REDIS_CLIENT = MockRedis.new
  Sidekiq.configure_client do |config|
    config.redis = { url: "mock://localhost:6379/0" }
  end
else
  Sidekiq.configure_server do |config|
    config.redis = { url: ENV.fetch("REDIS_URL", "redis://localhost:6379/0") }
  end
end
