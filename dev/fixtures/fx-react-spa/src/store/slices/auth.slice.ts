// Slice del store: tokens + sesion del usuario activo.
// Contiene token + usuario + isAuthenticated. La persistencia se hace via
// sessionStorage desde LoginPage (no desde el slice).

import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { User } from "../../types/index.js";

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  lastLoginAt: string | null;
}

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  lastLoginAt: null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    loginSuccess(state, action: PayloadAction<{ user: User; token: string }>) {
      state.user = action.payload.user;
      state.token = action.payload.token;
      state.isAuthenticated = true;
      state.lastLoginAt = new Date().toISOString();
    },
    logout(state) {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
      state.lastLoginAt = null;
    },
    hydrate(state, action: PayloadAction<{ user: User; token: string }>) {
      state.user = action.payload.user;
      state.token = action.payload.token;
      state.isAuthenticated = true;
    },
  },
});

export const { loginSuccess, logout, hydrate } = authSlice.actions;
export const authReducer = authSlice.reducer;