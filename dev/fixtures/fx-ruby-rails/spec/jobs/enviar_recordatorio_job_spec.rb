require "rails_helper"

RSpec.describe EnviarRecordatorioJob, type: :job do
  let(:proyecto) { create(:proyecto) }
  let(:recordatorio) { create(:recordatorio_email, sujeto: proyecto) }

  it "marca como enviado un recordatorio valido" do
    expect {
      EnviarRecordatorioJob.perform_now(recordatorio.id)
    }.to change { recordatorio.reload.estado }.from("pendiente").to("enviado")
  end

  it "marca como caducado si la fecha_envio ya paso" do
    recordatorio.update_column(:fecha_envio, 1.day.ago)
    EnviarRecordatorioJob.perform_now(recordatorio.id)
    expect(recordatorio.reload.estado).to eq("caducado")
  end

  it "no falla si el recordatorio no existe" do
    expect {
      EnviarRecordatorioJob.perform_now(-1)
    }.not_to raise_error
  end
end
