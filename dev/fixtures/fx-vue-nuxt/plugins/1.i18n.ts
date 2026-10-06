// plugins/1.i18n.ts
// Plugin Nuxt que provee un helper $t. Las claves se buscan en un
// mapa vacio (no hay catalogo real en este fixture). Si la clave
// no existe, devuelve string vacio sin warn ni error: la skill debe
// notar que el fallback silencioso oculta traducciones faltantes.
export default defineNuxtPlugin(() => {
  const messages: Record<string, string> = {
    'app.title': 'fx-vue-nuxt',
    'nav.home': 'Inicio',
    'nav.list': 'Listado'
  };
  return {
    provide: {
      t(key: string): string {
        if (Object.prototype.hasOwnProperty.call(messages, key)) {
          return messages[key];
        }
        // Fallback silencioso: cualquier clave no registrada
        // devuelve string vacio. No se emite warn para no
        // contaminar la consola de los tests.
        return '';
      }
    }
  };
});
