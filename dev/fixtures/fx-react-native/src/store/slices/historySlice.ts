import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

import type { Payment } from './paymentsSlice';

export interface HistoryState {
  items: Payment[];
  filter: string;
  sort: 'recent' | 'oldest' | 'amount';
  page: number;
  pageSize: number;
}

const initialState: HistoryState = {
  items: [],
  filter: '',
  sort: 'recent',
  page: 0,
  pageSize: 50,
};

const historySlice = createSlice({
  name: 'history',
  initialState,
  reducers: {
    setFilter(state, action: PayloadAction<string>) {
      state.filter = action.payload;
      state.page = 0;
    },
    setSort(state, action: PayloadAction<HistoryState['sort']>) {
      state.sort = action.payload;
    },
    nextPage(state) {
      state.page += 1;
    },
    ingestFromPayments(state, action: PayloadAction<Payment[]>) {
      state.items.push(...action.payload);
    },
  },
});

export const { setFilter, setSort, nextPage, ingestFromPayments } = historySlice.actions;
export default historySlice.reducer;