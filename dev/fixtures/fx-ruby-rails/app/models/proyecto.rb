class Proyecto < ApplicationRecord
  include Trackable

  # E02: callback before_save que normaliza el codigo. La trampa: el callback
  # corre antes de las validaciones, por lo que un nombre invalido se
  # normaliza igual y termina guardandose sin pasar por `validates :codigo`.
  before_save :normaliza_codigo
  after_destroy :registrar_baja_en_log

  validates :nombre, presence: true
  validates :codigo, presence: true
  validates :presupuesto, numericality: { greater_than_or_equal_to: 0 }
  validates :estado, inclusion: { in: %w[activo pausado cerrado] }

  has_many :facturas, dependent: :destroy
  has_many :recordatorios, as: :sujeto, dependent: :destroy

  scope :activos, -> { where(estado: "activo") }
  scope :por_presupuesto, ->(min) { where("presupuesto >= ?", min) }

  # P05: el listado dispara N+1 al contar recordatorios por cada proyecto.
  # El controlador no usa `with_count` ni `includes`, por lo que el test
  # detecta las queries adicionales (paquete: route_convention_override en
  # el controller + n_plus_one en el modelo).
  def recordatorios_pendientes
    recordatorios.where(estado: "pendiente").count
  end

  def to_param
    codigo
  end

  private

  def normaliza_codigo
    self.codigo = codigo.to_s.strip.upcase if codigo.present?
  end

  def registrar_baja_en_log
    Rails.logger.info("[proyectos] destroy id=#{id} codigo=#{codigo}")
  end
end
