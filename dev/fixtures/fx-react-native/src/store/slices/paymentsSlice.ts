import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

export interface Payment {
  id: string;
  orderId: string;
  amount: number;
  currency: string;
  tagId: string;
  status: 'pending' | 'success' | 'error' | 'offline';
  timestamp: number;
}

export interface PaymentsState {
  items: Payment[];
  pendingSync: string[];
  isProcessing: boolean;
  lastError?: string;
}

const initialState: PaymentsState = {
  items: [],
  pendingSync: [],
  isProcessing: false,
};

// Trampa P2: el reducer muta `state.items` directamente via push()
// sin `prepare` callback ni copia. Sin immer, esto seria un error
// de TypeScript; con createSlice + immer de toolkit, se compila pero
// la mutacion directa sigue funcionando en runtime.
const paymentsSlice = createSlice({
  name: 'payments',
  initialState,
  reducers: {
    addPayment(state, action: PayloadAction<Payment>) {
      // Trampa P2: push directo al array (redundant given toolkit el reduce to normal).
      state.items.push(action.payload);
    },
    markPendingSync(state, action: PayloadAction<string>) {
      state.pendingSync.push(action.payload);
    },
    setProcessing(state, action: PayloadAction<boolean>) {
      state.isProcessing = action.payload;
    },
    setLastError(state, action: PayloadAction<string | undefined>) {
      state.lastError = action.payload;
    },
    clearAll(state) {
      state.items = [];
      state.pendingSync = [];
    },
  },
});

export const { addPayment, markPendingSync, setProcessing, setLastError, clearAll } =
  paymentsSlice.actions;
export default paymentsSlice.reducer;