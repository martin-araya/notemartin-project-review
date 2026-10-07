# Concern para soft-delete: marca `cancelled_at` en vez de borrar.
# Se usa en Recordatorio (R-06 de la feature `recordatorios`).
module SoftDeletable
  extend ActiveSupport::Concern

  included do
    scope :active, -> { where(cancelled_at: nil) }
    scope :cancelled, -> { where.not(cancelled_at: nil) }
  end

  def cancel!
    update!(cancelled_at: Time.current)
  end

  def cancelled?
    cancelled_at.present?
  end
end
