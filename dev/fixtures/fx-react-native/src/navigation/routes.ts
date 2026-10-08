export const Routes = {
  PAYMENTS: 'payments',
  PAYMENTS_PAY: 'payments/pay',
  HISTORY: 'history',
  HISTORY_FILTER: 'history/filter',
  NOTIFICATIONS: 'notifications',
} as const;

export type RouteName = typeof Routes[keyof typeof Routes];