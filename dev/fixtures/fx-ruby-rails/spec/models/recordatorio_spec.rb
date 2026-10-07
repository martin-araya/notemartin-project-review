require "rails_helper"

RSpec.describe Recordatorio, type: :model do
  let(:proyecto) { create(:proyecto) }

  it "crea Recordatorio::Email valido" do
    r = build(:recordatorio_email, sujeto: proyecto)
    expect(r).to be_valid
  end

  it "rechaza Recordatorio::Email sin destinatario" do
    r = build(:recordatorio_email, sujeto: proyecto, destinatario_email: nil)
    expect(r).not_to be_valid
  end

  it "crea Recordatorio::Sms valido" do
    r = build(:recordatorio_sms, sujeto: proyecto)
    expect(r).to be_valid
  end

  it "rechaza Recordatorio::Sms con telefono malformado" do
    r = build(:recordatorio_sms, sujeto: proyecto, destinatario_telefono: "abc")
    expect(r).not_to be_valid
  end

  it "rechaza fecha_envio en pasado" do
    r = build(:recordatorio_email, sujeto: proyecto, fecha_envio: 1.day.ago)
    expect(r).not_to be_valid
  end

  it "cancela con cancel! y expone cancelled?" do
    r = create(:recordatorio_email, sujeto: proyecto)
    r.cancel!
    expect(r.cancelled?).to be true
  end
end
