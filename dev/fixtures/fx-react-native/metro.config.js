const path = require('path');
const { getDefaultConfig } = require('expo/metro-config');

// Trampa E5: aliases para Metro.
// NOTA: la trampa P6 planta que el alias `@features` apunta a `src/features`
// (correcto), pero los imports reales tienen `.tsx`/`ts` en paths que NO
// se resuelven automaticamente sin `resolver.sourceExts`.
const config = getDefaultConfig(__dirname);

config.resolver = {
  ...config.resolver,
  extraNodeModules: {
    '@app': path.resolve(__dirname, 'src'),
    '@features': path.resolve(__dirname, 'src/features'),
    '@store': path.resolve(__dirname, 'src/store'),
    '@nav': path.resolve(__dirname, 'src/navigation'),
    '@native': path.resolve(__dirname, 'src/native'),
    '@plugins': path.resolve(__dirname, 'src/plugins'),
    '@util': path.resolve(__dirname, 'src/util'),
  },
  sourceExts: ['js', 'jsx', 'ts', 'tsx', 'json'],
};

module.exports = config;