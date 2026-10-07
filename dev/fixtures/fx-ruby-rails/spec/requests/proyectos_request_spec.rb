require "rails_helper"

RSpec.describe "Proyectos request", type: :request do
  it "GET /proyectos responde 200" do
    get "/proyectos"
    File.write("/tmp/resp.html", session.response.body)
    expect(session.response.status).to eq(200)
  end

  it "POST /proyectos crea un proyecto valido" do
    expect {
      post "/proyectos", params: { proyecto: { codigo: "FX-1", nombre: "Demo", presupuesto: 100, estado: "activo" } }
    }.to change(Proyecto, :count).by(1)
  end

  it "POST /proyectos con datos invalidos responde 422" do
    post "/proyectos", params: { proyecto: { nombre: "" } }
    expect(session.response.status).to eq(422)
  end
end
