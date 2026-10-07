class Factura < ApplicationRecord
  include Trackable

  belongs_to :proyecto
  has_many :recordatorios, as: :sujeto, dependent: :destroy

  validates :monto_cents, numericality: { greater_than: 0 }
  validates :tarifa_iva, inclusion: { in: [0, 4, 10, 21] }
  validates :estado, inclusion: { in: %w[borrador emitida pagada anulada] }
  validate :estado_target_valido

  # E02: after_commit encola un job Sidekiq. La trampa: el callback se
  # ejecuta solo cuando la transaccion externa hace commit; en un test
  # que envuelve en transaction el commit nunca ocurre, asi que el job
  # queda pendiente. Por eso el test que verifica la intencion usa el
  # contador de ActiveJob despues de hacer un commit explicito.
  after_commit :encolar_generacion_pdf, on: :create

  scope :emitidas, -> { where(estado: "emitida") }
  scope :por_proyecto, ->(proyecto_id) { where(proyecto_id: proyecto_id) }

  def monto_euros
    (monto_cents || 0) / 100.0
  end

  def total_con_iva
    monto_euros * (1 + (tarifa_iva.to_f / 100.0))
  end

  def transicionar_a!(nuevo_estado)
    unless %w[borrador emitida pagada anulada].include?(nuevo_estado)
      raise ArgumentError, "estado invalido: #{nuevo_estado}"
    end
    update!(estado: nuevo_estado)
  end

  private

  def encolar_generacion_pdf
    GenerarFacturaPdfJob.perform_later(id) if estado == "emitida"
  end

  def estado_target_valido
    return if estado_was.nil?
    transiciones = {
      "borrador" => %w[emitida anulada],
      "emitida"  => %w[pagada anulada],
      "pagada"   => [],
      "anulada"  => []
    }
    if estado_changed? && !transiciones.fetch(estado_was, []).include?(estado)
      errors.add(:estado, "transicion invalida #{estado_was} -> #{estado}")
    end
  end
end
