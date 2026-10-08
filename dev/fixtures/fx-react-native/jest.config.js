module.exports = {
  preset: 'jest-expo',
  setupFiles: ['<rootDir>/jest.setup.js'],
  setupFilesAfterEach: [],
  testPathIgnorePatterns: [
    '/node_modules/',
    '/android_stub/',
    '/ios_stub/',
    '/.expo/',
  ],
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg|@reduxjs/toolkit))',
  ],
  moduleNameMapper: {
    '^@app/(.*)$': '<rootDir>/src/$1',
    '^@features/(.*)$': '<rootDir>/src/features/$1',
    '^@store/(.*)$': '<rootDir>/src/store/$1',
    '^@nav/(.*)$': '<rootDir>/src/navigation/$1',
    '^@native/(.*)$': '<rootDir>/src/native/$1',
    '^@plugins/(.*)$': '<rootDir>/src/plugins/$1',
    '^@util/(.*)$': '<rootDir>/src/util/$1',
  },
};