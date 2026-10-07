class CalculadoraIva
  TARIFAS_VALIDAS = [0, 4, 10, 21].freeze

  def self.calcular(base_cents, tarifa)
    unless TARIFAS_VALIDAS.include?(tarifa.to_i)
      raise ArgumentError, "tarifa invalida: #{tarifa}"
    end
    (base_cents.to_i * (1 + tarifa.to_i / 100.0)).round
  end
end
