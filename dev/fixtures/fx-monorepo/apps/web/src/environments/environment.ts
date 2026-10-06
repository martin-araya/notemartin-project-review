// Interface tokenizable para el environment. El archivo real se reemplaza
// por environment.development.ts o environment.production.ts en build time
// (trampa del ecosistema #5: fileReplacements en angular.json).
export interface Environment {
  production: boolean;
  apiBaseUrl: string;
}

export const environment: Environment = {
  production: false,
  apiBaseUrl: '/api',
};
