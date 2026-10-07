class ApplicationController < ActionController::Base
  protect_from_forgery with: :null_session

  # S01 trap: este metodo solo existe para la ruta dead en config/routes.rb
  # (P05: route_convention_override). Nunca se invoca desde los tests.
  def legacy_panel
    render plain: "legacy", status: :ok
  end
end
