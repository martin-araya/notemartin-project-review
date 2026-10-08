import { withInfoPlist, type ConfigPlugin } from 'expo/config-plugins';

/**
 * Trampa E3: este config plugin es invocado en `app.json` y modifica
 * la salida de `expo prebuild`. Añade NFCReaderUsageDescription al Info.plist.
 */
const withNfc: ConfigPlugin = (config) => {
  return withInfoPlist(config, (cfg) => {
    cfg.modResults.NSNFCReaderUsageDescription =
      cfg.modResults.NSNFCReaderUsageDescription ??
      'Used to read NFC tags for payment';
    cfg.modResults.NSCameraUsageDescription =
      cfg.modResults.NSCameraUsageDescription ??
      'Used to capture card photos';
    return cfg;
  });
};

export default withNfc;