require "rails_helper"

RSpec.describe Recordatorio, type: :model do
  let(:proyecto) { create(:proyecto) }

  it "rechaza Recordatorio::Email sin email del destinatario" do
    r = build(:recordatorio_email, sujeto: proyecto, destinatario_email: nil)
    expect(r).not_to be_valid
    expect(r.errors[:destinatario_email]).to be_present
  end

  it "rechaza Recordatorio::Email con email invalido" do
    r = build(:recordatorio_email, sujeto: proyecto, destinatario_email: "no-es-email")
    expect(r).not_to be_valid
  end

  it "acepta Recordatorio::Email con email valido" do
    r = build(:recordatorio_email, sujeto: proyecto)
    expect(r).to be_valid
  end
end
