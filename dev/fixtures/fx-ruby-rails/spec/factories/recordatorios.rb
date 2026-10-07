FactoryBot.define do
  factory :recordatorio, class: "Recordatorio" do
    association :sujeto, factory: :proyecto
    mensaje { "Recordatorio demo" }
    fecha_envio { 1.day.from_now }
    estado { "pendiente" }
  end

  factory :recordatorio_email, class: "Recordatorio::Email" do
    association :sujeto, factory: :proyecto
    mensaje { "Email demo" }
    destinatario_email { "demo@fx-rails.test" }
    fecha_envio { 1.day.from_now }
  end

  factory :recordatorio_sms, class: "Recordatorio::Sms" do
    association :sujeto, factory: :proyecto
    mensaje { "SMS demo" }
    destinatario_telefono { "+34666555444" }
    fecha_envio { 1.day.from_now }
  end
end
