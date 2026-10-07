# S01: trampa superficial. Servicio legacy con un solo metodo de clase
# que nunca es invocado por la app. La skill debe listarlo y notar que no
# tiene consumidores en app/, lib/ ni spec/.
class LegacyTextFormatter
  def self.legacy_format(input)
    input.to_s.gsub(/[^a-z0-9]/i, "").upcase
  end
end
