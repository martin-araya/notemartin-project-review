// Libreria compartida del monorepo fx-monorepo.
// Los tipos viven en ``./types`` y los helpers en ``./utils``.
// El barrel reexporta todo para que ``import { ... } from '@fx-mono/shared'``
// funcione desde apps/web y apps/api.
export * from './types/index.js';
export * from './utils/index.js';
