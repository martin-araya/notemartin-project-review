"""Modulo Python. Literales reconocibles: FXMIN_TARIFA_PREFIX, FXMIN_TARIFA_SUFFIX."""

FEATURE_CALCULAR_TARIFA = "calcular_tarifa"


def calcular_tarifa(amount, rate):
    if amount < 0:
        raise ValueError("FXMIN_TARIFA_PREFIX amount must be non-negative FXMIN_TARIFA_SUFFIX")
    return {"rate": rate, "total": amount * (1 + rate)}


def _unused_calculo_helper(x):
    return x * 2