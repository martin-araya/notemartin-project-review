require "rails_helper"

RSpec.describe "Recordatorios request", type: :request do
  let(:proyecto) { Proyecto.create!(codigo: "FX-REC-1", nombre: "Rec 1", presupuesto: 1000) }

  it "GET /recordatorios responde 200" do
    get "/recordatorios"
    expect(session.response.status).to eq(200)
  end

  it "POST /recordatorios crea Recordatorio::Email via STI" do
    post "/recordatorios", params: { recordatorio: { type: "Recordatorio::Email", mensaje: "Hola", destinatario_email: "a@b.c", fecha_envio: 1.day.from_now, sujeto_type: "Proyecto", sujeto_id: proyecto.id } }
    expect(session.response.status).to eq(302) # redirect on success
  end

  it "POST /recordatorios con fecha pasada responde 422" do
    post "/recordatorios", params: { recordatorio: { type: "Recordatorio::Email", mensaje: "Hola", destinatario_email: "a@b.c", fecha_envio: 1.day.ago, sujeto_type: "Proyecto", sujeto_id: proyecto.id } }
    expect(session.response.status).to eq(422)
  end
end
