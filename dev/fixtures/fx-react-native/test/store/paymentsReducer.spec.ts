import paymentsReducer, {
  addPayment,
  setProcessing,
  setLastError,
  markPendingSync,
} from '../../src/store/slices/paymentsSlice';

describe('paymentsSlice', () => {
  it('addPayment appends to items', () => {
    const state = paymentsReducer(undefined, addPayment({
      id: 'pay-1',
      orderId: 'order-1',
      amount: 9.99,
      currency: 'USD',
      tagId: 'tag-1',
      status: 'success',
      timestamp: 1,
    }));
    expect(state.items).toHaveLength(1);
    expect(state.items[0].orderId).toBe('order-1');
  });

  it('setProcessing toggles flag', () => {
    let s = paymentsReducer(undefined, setProcessing(true));
    expect(s.isProcessing).toBe(true);
    s = paymentsReducer(s, setProcessing(false));
    expect(s.isProcessing).toBe(false);
  });

  it('setLastError updates error', () => {
    let s = paymentsReducer(undefined, setLastError('fail'));
    expect(s.lastError).toBe('fail');
    s = paymentsReducer(s, setLastError(undefined));
    expect(s.lastError).toBeUndefined();
  });

  it('markPendingSync adds to queue', () => {
    const s = paymentsReducer(undefined, markPendingSync('order-1'));
    expect(s.pendingSync).toContain('order-1');
  });
});