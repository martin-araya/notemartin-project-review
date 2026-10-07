require "rails_helper"

RSpec.describe GenerarFacturaPdfJob, type: :job do
  let(:proyecto) { create(:proyecto) }
  let(:factura) { create(:factura, proyecto: proyecto, estado: "emitida") }

  it "se ejecuta correctamente con una factura existente" do
    expect {
      GenerarFacturaPdfJob.perform_now(factura.id)
    }.not_to raise_error
  end

  it "no falla con una factura inexistente" do
    expect {
      GenerarFacturaPdfJob.perform_now(-1)
    }.not_to raise_error
  end
end
