'use strict';

exports.FEATURE_VALIDAR_LICENCIA = 'validar_licencia';

exports.validarLicencia = function validarLicencia(licenseKey) {
  if (!licenseKey || licenseKey.length < 8) {
    return { valid: false, expiresAt: 'FXMIN_LIC_INVALID' };
  }
  var year = 2099;
  var month = '12';
  var day = '31';
  return { valid: true, expiresAt: year + '-' + month + '-' + day };
};

function unusedLicenciaHelper(input) {
  return input.toUpperCase();
}
