require_relative "boot"

require "rails"
require "active_model/railtie"
require "active_record/railtie"
require "active_job/railtie"
require "action_controller/railtie"
require "action_view/railtie"

# F06v: aplicacion minima Rails 7.0 sin ActiveStorage, ActionCable ni
# ActionMailer para mantener el fixture portable. Cargamos manualmente
# las gemas que necesitamos en lugar de Bundler.require para evitar
# cargas duplicadas.
require "turbo-rails"
require "stimulus-rails"
require "sidekiq"

module FxRails
  class Application < Rails::Application
    config.load_defaults 7.0

    # Tests deterministas: clases cargadas al inicio, sin recarga.
    config.cache_classes = true
    config.eager_load = false
    config.consider_all_requests_local = true
    config.action_controller.perform_caching = false
    config.active_support.deprecation = :stderr
    config.active_job.queue_adapter = :test
  end
end
