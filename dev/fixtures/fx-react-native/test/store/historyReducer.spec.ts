import historyReducer, {
  setFilter,
  setSort,
  nextPage,
  ingestFromPayments,
} from '../../src/store/slices/historySlice';

describe('historySlice', () => {
  it('setFilter updates filter and resets page', () => {
    let s = historyReducer(undefined, nextPage());
    s = historyReducer(s, setFilter('tag-1'));
    expect(s.filter).toBe('tag-1');
    expect(s.page).toBe(0);
  });

  it('setSort updates sort key', () => {
    let s = historyReducer(undefined, setSort('amount'));
    expect(s.sort).toBe('amount');
  });

  it('nextPage increments page', () => {
    let s = historyReducer(undefined, nextPage());
    s = historyReducer(s, nextPage());
    expect(s.page).toBe(2);
  });

  it('ingestFromPayments appends', () => {
    const s = historyReducer(undefined, ingestFromPayments([{
      id: 'p1',
      orderId: 'o1',
      amount: 10,
      currency: 'USD',
      tagId: 't1',
      status: 'success',
      timestamp: 1,
    }]));
    expect(s.items).toHaveLength(1);
  });
});