import { withInfoPlist, withAndroidManifest, type ConfigPlugin } from 'expo/config-plugins';

/**
 * Trampa E3: este config plugin modifica prebuild para añadir deep linking
 * en iOS (CFBundleURLTypes) y Android (intent-filter).
 */
const withDeepLinking: ConfigPlugin = (config) => {
  config = withInfoPlist(config, (cfg) => {
    cfg.modResults.CFBundleURLTypes = cfg.modResults.CFBundleURLTypes ?? [];
    cfg.modResults.CFBundleURLTypes.push({
      CFBundleURLName: 'com.example.fxrn',
      CFBundleURLSchemes: ['fxrn'],
    });
    return cfg;
  });

  config = withAndroidManifest(config, (cfg) => {
    const intentFilters = (cfg.modResults.manifest.application as any)?.[0]?.['intent-filter'] ?? [];
    (cfg.modResults.manifest.application as any)[0]['intent-filter'] = [
      ...intentFilters,
      {
        action: [{ $: { 'android:name': 'android.intent.action.VIEW' } }],
        category: [
          { $: { 'android:name': 'android.intent.category.DEFAULT' } },
          { $: { 'android:name': 'android.intent.category.BROWSABLE' } },
        ],
        data: [{ $: { 'android:scheme': 'fxrn' } }],
      },
    ];
    return cfg;
  });

  return config;
};

export default withDeepLinking;