# Seed minimo para los tests de integracion.
proyecto = Proyecto.find_or_create_by!(codigo: "FX-DEMO") do |p|
  p.nombre = "Proyecto demo"
  p.presupuesto = 10_000
  p.estado = "activo"
end

Factura.find_or_create_by!(proyecto: proyecto, monto_cents: 12_000) do |f|
  f.tarifa_iva = 21
  f.estado = "emitida"
end

Recordatorio::Email.find_or_create_by!(
  sujeto: proyecto,
  mensaje: "Bienvenida al proyecto",
  destinatario_email: "demo@fx-rails.test",
  fecha_envio: 1.day.from_now
)
