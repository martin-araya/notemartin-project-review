# E04: define_method + method_missing legacy. Simula un resolver de
# constantes "legacy" para clases que ya no existen. No tiene llamadas
# explicitas en el codigo de la app: queda como superficie que la skill
# debe descubrir al recorrer config/initializers/.
module LegacyConstants
  module Resolver
    def self.define_lookup(name)
      define_method(name) do |*args|
        if Object.const_defined?(name.to_s.singularize.classify, false)
          Object.const_get(name.to_s.singularize.classify)
        else
          nil
        end
      end
    end

    def method_missing(method_name, *args)
      if method_name.to_s.start_with?("lookup_")
        candidate = method_name.to_s.sub("lookup_", "").classify
        if Object.const_defined?(candidate, false)
          Object.const_get(candidate)
        else
          super
        end
      else
        super
      end
    end

    def respond_to_missing?(method_name, include_private = false)
      method_name.to_s.start_with?("lookup_") || super
    end
  end
end
