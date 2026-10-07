# E05: STI con columna `type`. La clase base declara la columna `type` en
# la migracion; las subclases (Recordatorio::Email, Recordatorio::Sms)
# viven bajo el namespace `Recordatorio`. ActiveRecord resuelve la clase
# hija con `recordatorio.type`.
#
# P04 trampa: sobreescribimos `find_sti_class` para que un `type`
# desconocido caiga en Recordatorio base en lugar de levantar
# `ActiveRecord::SubclassNotFound`. Asi el codigo de la app no se entera
# de que la subclase no existe.
class Recordatorio < ApplicationRecord
  include SoftDeletable

  self.inheritance_column = :type

  belongs_to :sujeto, polymorphic: true

  validates :mensaje, presence: true
  validates :fecha_envio, presence: true
  validate :fecha_envio_no_pasada

  # P04: sti_invalid_type_silent. find_sti_class devuelve Recordatorio
  # base si la constante no existe o no es subclase valida. Esto evita
  # que ActiveRecord::SubclassNotFound se propague y permite que el
  # registro se guarde silenciosamente.
  def self.find_sti_class(type_name)
    klass = type_name.constantize rescue nil
    if klass.is_a?(Class) && klass < Recordatorio
      klass
    else
      Recordatorio
    end
  end

  scope :pendientes, -> { where(estado: "pendiente") }
  scope :caducados, -> { where("fecha_envio < ?", Time.current).where(estado: "pendiente") }

  def marcar_enviado!
    update!(estado: "enviado", enviado_at: Time.current)
  end

  def marcar_caducado!
    update!(estado: "caducado")
  end

  private

  def fecha_envio_no_pasada
    return if fecha_envio.blank?
    if fecha_envio < Time.current
      errors.add(:fecha_envio, "no puede estar en el pasado")
    end
  end

  # F06v: trampa paquete P04. En Ruby 3.x no se puede asignar `self.class =`,
  # asi que registramos el type via `becomes!` solo si la clase existe.
  # Si la constante no existe o no es subclase de Recordatorio, el recordatorio
  # queda como Recordatorio base silenciosamente.
  def asegurar_clase_sti
    return if type.blank?
    klass = type.constantize rescue nil
    return unless klass.is_a?(Class)
    if klass < Recordatorio
      # P04 trampa: sin esto, los STI hijos se quedarian como Recordatorio.
      # El `becomes!` no funciona aqui (no es un save), asi que usamos
      # `type=` con el setter que Rails provee para STI.
      send(:type=, klass.name)
    end
  end
end
