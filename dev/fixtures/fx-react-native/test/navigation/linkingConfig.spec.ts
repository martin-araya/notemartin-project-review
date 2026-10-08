import { linkingConfig } from '../../src/navigation/linkingConfig';

describe('linkingConfig', () => {
  it('declares 3 prefixes', () => {
    expect(linkingConfig.prefixes.length).toBeGreaterThanOrEqual(3);
  });

  it('includes fxrn scheme', () => {
    expect(linkingConfig.prefixes).toContain('fxrn://');
  });

  it('declares deep links to pay screen', () => {
    expect(linkingConfig.config?.screens?.['payments/pay']).toBe('pay/:orderId');
  });

  it('declares deep links to history filter', () => {
    expect(linkingConfig.config?.screens?.['history/filter']).toBe('history/:filter');
  });
});