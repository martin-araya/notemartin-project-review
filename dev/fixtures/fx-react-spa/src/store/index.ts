// Store global de la SPA.
// Combina Redux Toolkit (slices) con RTK Query (ver api/baseApi.ts).

import { configureStore } from "@reduxjs/toolkit";
import { setupListeners } from "@reduxjs/toolkit/query";
import { authReducer } from "./slices/auth.slice.js";
import { cartReducer } from "./slices/cart.slice.js";
import { baseApi } from "../api/baseApi.js";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    cart: cartReducer,
    [baseApi.reducerPath]: baseApi.reducer,
  },
  middleware: (getDefault) => getDefault().concat(baseApi.middleware),
});

setupListeners(store.dispatch);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;