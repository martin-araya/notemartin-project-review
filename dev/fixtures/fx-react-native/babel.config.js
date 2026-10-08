module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      [
        'module-resolver',
        {
          root: ['./'],
          alias: {
            '@app': './src',
            '@features': './src/features',
            '@store': './src/store',
            '@nav': './src/navigation',
            '@native': './src/native',
            '@plugins': './src/plugins',
            '@util': './src/util',
          },
        },
      ],
    ],
  };
};