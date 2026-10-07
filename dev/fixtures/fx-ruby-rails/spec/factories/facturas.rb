FactoryBot.define do
  factory :factura do
    association :proyecto
    monto_cents { 10_000 }
    tarifa_iva { 21 }
    estado { "emitida" }
  end
end
