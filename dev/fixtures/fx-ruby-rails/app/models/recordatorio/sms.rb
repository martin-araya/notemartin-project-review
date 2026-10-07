class Recordatorio
  class Sms < Recordatorio
    validates :destinatario_telefono, presence: true
    validate :telefono_formato_basico

    def canal
      "sms"
    end

    private

    def telefono_formato_basico
      return if destinatario_telefono.blank?
      unless destinatario_telefono.to_s.match?(/\A\+?\d{6,15}\z/)
        errors.add(:destinatario_telefono, "formato invalido")
      end
    end
  end
end
