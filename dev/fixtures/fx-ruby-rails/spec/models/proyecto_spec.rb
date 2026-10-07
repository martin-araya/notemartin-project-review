require "rails_helper"

RSpec.describe Proyecto, type: :model do
  it "es valido con atributos por defecto" do
    expect(build(:proyecto)).to be_valid
  end

  it "requiere nombre" do
    p = build(:proyecto, nombre: nil)
    expect(p).not_to be_valid
    expect(p.errors[:nombre]).to be_present
  end

  it "requiere presupuesto no negativo" do
    p = build(:proyecto, presupuesto: -1)
    expect(p).not_to be_valid
  end

  it "normaliza el codigo en before_save" do
    p = create(:proyecto, codigo: "  fx-pry-1  ")
    expect(p.reload.codigo).to eq("FX-PRY-1")
  end

  it "asigna tracking_id via concern Trackable" do
    p = create(:proyecto)
    expect(p.tracking_id).to be_present
    expect(p.tracking_code).to start_with("FX-PROYECTO-")
  end

  it "limita el estado a inclusion" do
    p = build(:proyecto, estado: "nope")
    expect(p).not_to be_valid
  end
end
