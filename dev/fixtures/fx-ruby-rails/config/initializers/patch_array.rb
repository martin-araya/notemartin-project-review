# E06: Monkey patch sobre Array. Redefine `sum_safe` para evitar overflow
# silencioso en colecciones grandes. La trampa es que cualquier codigo que
# confia en `Array#sum` y procesa enteros grandes se beneficia (o sufre) este
# cambio global sin una llamada explicita.
class Array
  def sum_safe
    map { |x| x.respond_to?(:to_i) ? x.to_i : 0 }.sum
  end
end
