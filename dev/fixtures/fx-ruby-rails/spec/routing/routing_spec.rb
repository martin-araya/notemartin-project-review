require "rails_helper"

RSpec.describe "Rutas de proyectos" do
  it "responde index en /proyectos" do
    expect(Rails.application.routes.recognize_path("/proyectos", method: :get)).to include(controller: "proyectos", action: "index")
  end

  it "responde create en POST /proyectos" do
    expect(Rails.application.routes.recognize_path("/proyectos", method: :post)).to include(controller: "proyectos", action: "create")
  end

  it "responde show en /proyectos/:id" do
    expect(Rails.application.routes.recognize_path("/proyectos/ABC", method: :get)).to include(controller: "proyectos", action: "show", id: "ABC")
  end
end

RSpec.describe "Rutas de facturas" do
  it "responde index en /facturas" do
    expect(Rails.application.routes.recognize_path("/facturas", method: :get)).to include(controller: "facturas", action: "index")
  end
end

RSpec.describe "Rutas de recordatorios" do
  it "responde index en /recordatorios" do
    expect(Rails.application.routes.recognize_path("/recordatorios", method: :get)).to include(controller: "recordatorios", action: "index")
  end

  it "responde cancel en PATCH /recordatorios/:id/cancel" do
    expect(Rails.application.routes.recognize_path("/recordatorios/1/cancel", method: :patch)).to include(controller: "recordatorios", action: "cancel", id: "1")
  end
end
