class Recordatorio
  # E05: otra subclase STI plantada para que la skill detecte la herencia
  # polimorfica. No se usa directamente en los tests pero aparece en el
  # listado de subclases (`Recordatorio.subclasses`).
  class Push < Recordatorio
    validates :device_token, presence: true

    def canal
      "push"
    end
  end
end
