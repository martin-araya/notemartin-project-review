// jest.config.js
// Configuracion de Jest para Angular + NgRx + jasmine-marbles.
module.exports = {
  preset: 'jest-preset-angular',
  globalSetup: 'jest-preset-angular/global-setup',
  moduleNameMapper: {
    '^@app/(.*)$': '<rootDir>/src/app/$1',
    '^@env/(.*)$': '<rootDir>/src/environments/$1'
  },
  testEnvironmentOptions: {
    customExportConditions: ['node']
  },
  setupFilesAfterEach: [],
  testMatch: ['<rootDir>/tests/**/*.test.ts', '<rootDir>/src/**/*.spec.ts'],
  testTimeout: 20000
};
