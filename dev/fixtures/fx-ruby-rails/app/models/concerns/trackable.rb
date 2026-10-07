# E03: Concern con `included do`. Trackable agrega un `before_create` que
# asigna un `tracking_id` unico y mantiene actualizado `last_seen_at`. Es
# incluido por Proyecto y Factura, lo que duplica el callback en ambos
# modelos (trampa P03: concern_included_twice con logica sutilmente divergente).
module Trackable
  extend ActiveSupport::Concern

  included do
    before_create :assign_tracking_id
    before_save :stamp_last_seen_at
  end

  module ClassMethods
    def tracked_by
      where.not(tracking_id: nil)
    end
  end

  def tracking_code
    "FX-#{self.class.name.demodulize.upcase}-#{tracking_id}"
  end

  private

  def assign_tracking_id
    self.tracking_id ||= SecureRandom.hex(6)
  end

  def stamp_last_seen_at
    self.last_seen_at = Time.current
  end
end
