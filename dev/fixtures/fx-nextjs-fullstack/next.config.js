/**
 * Next.js config (F06h).
 * Trampa paquete #6: reactStrictMode deshabilitado para silenciar
 * efectos duplicados en dev. La skill debe notar la asimetria con el
 * default de Next (que es true).
 */
const nextConfig = {
  reactStrictMode: false,
  experimental: {
    serverActions: {
      allowedOrigins: ["localhost:3000"],
    },
  },
  // Los headers de cache se documentan en app/lib/tags.ts para que la
  // skill pueda mapear las revalidaciones.
  async headers() {
    return [];
  },
};

module.exports = nextConfig;