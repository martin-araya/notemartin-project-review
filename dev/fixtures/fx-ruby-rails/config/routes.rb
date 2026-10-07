Rails.application.routes.draw do
  # E01: convencion sobre configuracion. resources genera 7 rutas por feature
  # sin necesidad de declararlas una a una en este archivo.
  resources :proyectos
  resources :facturas
  resources :recordatorios do
    member do
      patch :cancel
    end
  end

  # P05: route_convention_override. Esta ruta nunca es invocada por la suite
  # de tests ni por los controladores; queda como ruido en `rails routes`.
  get "panel/legacy", to: "application#legacy_panel", as: :legacy_panel

  root to: redirect("/proyectos")
end
