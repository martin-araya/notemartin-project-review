require "rails_helper"

RSpec.describe "Facturas request", type: :request do
  let(:proyecto) { Proyecto.create!(codigo: "FX-REQ-1", nombre: "Req 1", presupuesto: 1000) }

  it "GET /facturas responde 200" do
    get "/facturas"
    expect(session.response.status).to eq(200)
  end

  it "POST /facturas con tarifa invalida responde 422" do
    post "/facturas", params: { factura: { proyecto_id: proyecto.id, monto_cents: 100, tarifa_iva: 7 } }, as: :json
    expect(session.response.status).to eq(422)
  end

  it "POST /facturas con datos validos responde 201" do
    post "/facturas", params: { factura: { proyecto_id: proyecto.id, monto_cents: 1000, tarifa_iva: 21 } }, as: :json
    expect(session.response.status).to eq(201)
  end
end
