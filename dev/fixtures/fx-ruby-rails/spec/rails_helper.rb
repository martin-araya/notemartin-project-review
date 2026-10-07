require "spec_helper"

# F06v: en Ruby 3.2.11+ la gema `logger` ya no es cargada por defecto.
# ActiveSupport 7.0 referencia Logger antes de que el autoload lo active.
require "logger"

# F06v: el environment se carga una sola vez por proceso RSpec para evitar
# que el initializer `set_autoload_paths` falle al intentar unshift sobre
# un array ya congelado.
unless defined?(Rails::Application) && Rails.application
  ENV["RAILS_ENV"] ||= "test"
  require_relative "../config/environment"
end

abort("The Rails environment is running in production mode!") if Rails.env.production?

require "capybara/rspec"
# F06v: usamos factory_bot directamente (sin factory_bot_rails que requiere
# un railtie propio que se inicializa dos veces).
require "factory_bot"
puts "F06v debug: __dir__ = #{__dir__}" if ENV["NPR_DEBUG"]
puts "F06v debug: Rails.root = #{Rails.root}" if ENV["NPR_DEBUG"]
factory_files = Dir[File.expand_path("factories/**/*.rb", __dir__)].sort
puts "F06v debug: factory files = #{factory_files.inspect}" if ENV["NPR_DEBUG"]
factory_files.each do |f|
  load f
  puts "F06v debug: after loading #{File.basename(f)}: #{FactoryBot.factories.map(&:name).inspect}" if ENV["NPR_DEBUG"]
end

# F06v: capybara usa la app Rails para los feature specs.
Capybara.app = Rails.application
Capybara.server = :webrick
Capybara.default_driver = :rack_test
Capybara.save_path = Rails.root.join("tmp/capybara").to_s

include FactoryBot::Syntax::Methods

# F06v: implementamos use_transactional_fixtures manualmente (sin
# rspec-rails) para evitar el bug de carga con ENCODING_FLAG.
# Cargamos el schema directamente (db/schema.rb) en lugar de correr
# las migraciones en cada test.
ActiveRecord::Base.establish_connection(ActiveRecord::Base.configurations.find_db_config("test"))
load File.expand_path("../db/schema.rb", __dir__)
ActiveRecord::Base.connection.execute("PRAGMA foreign_keys = ON") if ActiveRecord::Base.connection.adapter_name == "SQLite"

Capybara.server = :webrick
Capybara.default_driver = :rack_test
Capybara.save_path = Rails.root.join("tmp/capybara").to_s

RSpec.configure do |config|
  config.fixture_paths = [Rails.root.join("spec/fixtures").to_s] if File.directory?(Rails.root.join("spec/fixtures").to_s)

  # F06v: includimos IntegrationTest para usar get/post/etc en request specs
  # sin rspec-rails.
  config.include Rails.application.routes.url_helpers
  config.include ActionDispatch::TestProcess

  # F06v: transactional fixtures manuales. Cada test corre dentro de una
  # transaccion que se hace rollback al final.
  config.around(:each) do |example|
    if Rails.env.test? && defined?(ActiveRecord::Base)
      ActiveRecord::Base.transaction do
        example.run
        raise ActiveRecord::Rollback
      end
    else
      example.run
    end
  end
end

# F06v: helper de sesion HTTP para request specs (sin rspec-rails).
module RequestSpecHelper
  def app
    Rails.application
  end

  def session
    @session ||= ActionDispatch::Integration::Session.new(app)
  end

  def get(path, **opts)
    session.get(path, **opts)
  end

  def post(path, **opts)
    session.post(path, **opts)
  end
end

RSpec.configure do |config|
  config.include RequestSpecHelper, type: :request
end


