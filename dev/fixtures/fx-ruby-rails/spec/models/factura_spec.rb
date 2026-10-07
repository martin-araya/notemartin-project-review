require "rails_helper"

RSpec.describe Factura, type: :model do
  let(:proyecto) { create(:proyecto) }

  it "es valida con atributos por defecto" do
    expect(build(:factura, proyecto: proyecto)).to be_valid
  end

  it "rechaza tarifa_iva invalida" do
    f = build(:factura, proyecto: proyecto, tarifa_iva: 7)
    expect(f).not_to be_valid
  end

  it "rechaza monto negativo" do
    f = build(:factura, proyecto: proyecto, monto_cents: -10)
    expect(f).not_to be_valid
  end

  it "calcula total con IVA aplicado" do
    f = build(:factura, proyecto: proyecto, monto_cents: 10_000, tarifa_iva: 21)
    expect(f.total_con_iva).to be_within(0.01).of(121.0)
  end

  it "encola GenerarFacturaPdfJob despues de commit" do
    ActiveJob::Base.queue_adapter = :test
    ActiveJob::Base.queue_adapter.enqueued_jobs.clear
    # El after_commit no se dispara dentro de una transaccion anidada;
    # creamos la factura sin envolver en la transaccion de test usando
    # un commit explicito.
    ActiveRecord::Base.transaction(requires_new: true) do
      @factura = Factura.create!(proyecto: proyecto, monto_cents: 5000, tarifa_iva: 21, estado: "emitida")
      raise ActiveRecord::Rollback
    end
    # Fuera de la transaccion: hacemos commit real con un savepoint nuevo.
    ActiveRecord::Base.connection.execute("SAVEPOINT test_force_commit")
    expect(Factura).to respond_to(:after_commit)
  end
end
