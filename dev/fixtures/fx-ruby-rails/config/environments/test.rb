Rails.application.configure do
  config.cache_classes = true
  config.eager_load = true
  config.public_file_server.headers = { "Cache-Control" => "public, max-age=3600" }
  config.consider_all_requests_local = true
  config.action_controller.perform_caching = false
  config.action_dispatch.show_exceptions = :rescuable
  config.action_controller.allow_forgery_protection = false
  config.active_support.deprecation = :stderr
  # F06v: en test mostramos excepciones detalladas en lugar de rescue.
  config.action_dispatch.show_exceptions = :all
end
