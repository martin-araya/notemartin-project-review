import withNfc from '../../src/plugins/withNfc';

describe('withNfc plugin', () => {
  it('adds NSNFCReaderUsageDescription', () => {
    const config: any = { name: 'test', slug: 'test', modResults: {} };
    const result: any = withNfc(config);
    expect(result.modResults.NSNFCReaderUsageDescription).toBeDefined();
  });
});