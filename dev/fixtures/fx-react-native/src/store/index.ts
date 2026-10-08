import { configureStore } from '@reduxjs/toolkit';

import paymentsReducer from './slices/paymentsSlice';
import historyReducer from './slices/historySlice';
import notificationsReducer from './slices/notificationsSlice';

export const store = configureStore({
  reducer: {
    payments: paymentsReducer,
    history: historyReducer,
    notifications: notificationsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ serializableCheck: false }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;