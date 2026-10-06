// Slice del carrito.
// Trampa del paquete #5: addItem muta el array (push) en lugar de crear uno
// nuevo. Redux Toolkit detecta esto via Immer (que se queja al mutar fuera
// de produce), pero si alguien pasa un array ya clonado, el comportamiento
// cambia. La skill debe notar que esta forma es fragil.

import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { CartItem } from "../../types/index.js";

interface CartState {
  items: CartItem[];
  lastUpdated: string | null;
}

const initialState: CartState = {
  items: [],
  lastUpdated: null,
};

const cartSlice = createSlice({
  name: "cart",
  initialState,
  reducers: {
    addItem(
      state,
      action: PayloadAction<{ productId: string; unitPrice: number; quantity?: number }>,
    ) {
      const { productId, unitPrice, quantity = 1 } = action.payload;
      const existing = state.items.find((i) => i.productId === productId);
      if (existing) {
        existing.quantity += quantity;
      } else {
        // Trampa #5: push mutante. Funciona con Immer pero rompe si alguien
        // usa el slice fuera de Redux (p.ej. tests con freezed state).
        state.items.push({ productId, unitPrice, quantity });
      }
      state.lastUpdated = new Date().toISOString();
    },
    removeItem(state, action: PayloadAction<string>) {
      const idx = state.items.findIndex((i) => i.productId === action.payload);
      if (idx >= 0) {
        state.items.splice(idx, 1);
        state.lastUpdated = new Date().toISOString();
      }
    },
    clear(state) {
      state.items.length = 0;
      state.lastUpdated = new Date().toISOString();
    },
  },
});

export const { addItem, removeItem, clear } = cartSlice.actions;
export const cartReducer = cartSlice.reducer;