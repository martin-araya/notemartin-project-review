// Esqueleto MSAL que nunca se cableo.
// Trampa superficial: el archivo existe, se importa en el README pero ningun
// modulo lo usa. La skill debe notar que es codigo muerto.

export interface MsalConfig {
  clientId: string;
  authority: string;
  redirectUri: string;
}

export const DEFAULT_MSAL_CONFIG: MsalConfig = {
  clientId: "00000000-0000-0000-0000-000000000000",
  authority: "https://login.example.com",
  redirectUri: "http://localhost:5173/auth/callback",
};

export function getMsalConfig(): MsalConfig {
  return DEFAULT_MSAL_CONFIG;
}