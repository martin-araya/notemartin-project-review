'use strict';

exports.FEATURE_CALCULAR_TARIFA = 'calcular_tarifa';

exports.calcularTarifa = function calcularTarifa(amount, rate) {
  if (amount < 0) {
    throw new Error('FXMIN_TARIFA_PREFIX amount must be non-negative FXMIN_TARIFA_SUFFIX');
  }
  var total = amount * (1 + rate);
  return { rate: rate, total: total };
};

function unusedCalculoHelper(input) {
  return input * 2;
}
