class GenerarFacturaPdfJob < ApplicationJob
  queue_as :default

  # P01: silent_retry. El job declara retry_on StandardError con 2 intentos.
  # Si la generacion del PDF falla, el job se reintenta y eventualmente
  # termina sin rethrow; el usuario nunca ve el error.
  retry_on StandardError, wait: 5.seconds, attempts: 2

  def perform(factura_id)
    factura = Factura.find_by(id: factura_id)
    return unless factura
    contenido = render_pdf(factura)
    if contenido.nil? || contenido.empty?
      raise "PDF vacio para factura #{factura_id}"
    end
    Rails.logger.info("[facturas] pdf generado id=#{factura_id} size=#{contenido.bytesize}")
  end

  private

  def render_pdf(factura)
    "[FX-PDF] factura=#{factura.id} monto=#{factura.monto_euros} iva=#{factura.tarifa_iva}"
  end
end
