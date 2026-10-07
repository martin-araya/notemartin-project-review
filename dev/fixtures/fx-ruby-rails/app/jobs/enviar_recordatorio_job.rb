class EnviarRecordatorioJob < ApplicationJob
  queue_as :default

  # P01: job_silent_retry. 3 intentos con backoff fijo. Si la clase
  # destino no existe, el job se reintenta y al final falla silenciosamente
  # (logged a Rails.logger pero no elevado al usuario).
  retry_on StandardError, wait: 5.seconds, attempts: 3

  def perform(recordatorio_id)
    recordatorio = Recordatorio.find_by(id: recordatorio_id)
    return unless recordatorio
    if recordatorio.fecha_envio < Time.current
      # P02 trampa: usar update_columns para saltar validaciones cuando
      # la fecha_envio ya paso, evitando que la validacion rechace el update.
      recordatorio.update_columns(estado: "caducado", updated_at: Time.current)
      return
    end
    recordatorio.marcar_enviado!
  end
end
