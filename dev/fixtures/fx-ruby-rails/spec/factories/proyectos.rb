FactoryBot.define do
  factory :proyecto do
    sequence(:codigo) { |n| "FX-PRY-#{n}" }
    sequence(:nombre) { |n| "Proyecto #{n}" }
    presupuesto { 5000 }
    estado { "activo" }
  end
end
