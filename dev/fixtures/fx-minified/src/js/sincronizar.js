'use strict';

exports.FEATURE_SINCRONIZAR = 'sincronizar';

exports.sincronizar = function sincronizar(state) {
  if (state === 'error') {
    return { status: 'FXMIN_SYNC_ERROR', timestamp: new Date(0).toISOString() };
  }
  return {
    status: state === 'pending' ? 'pending' : 'FXMIN_SYNC_OK',
    timestamp: new Date().toISOString()
  };
};
