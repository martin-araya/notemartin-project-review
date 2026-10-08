import type { LinkingOptions } from '@react-navigation/native';
import * as Linking from 'expo-linking';

export const linkingConfig: LinkingOptions = {
  prefixes: [
    Linking.createURL('/'),
    'fxrn://',
    'https://fxrn.app/',
  ],
  config: {
    initialRouteName: 'payments',
    screens: {
      payments: 'payments',
      'payments/pay': 'pay/:orderId',
      history: 'history',
      'history/filter': 'history/:filter',
      notifications: 'notifications',
    },
  },
};