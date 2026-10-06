"""Modulo Python. Literal reconocible: FXMIN_LIC_INVALID."""

FEATURE_VALIDAR_LICENCIA = "validar_licencia"


def validar_licencia(license_key):
    if not license_key or len(license_key) < 8:
        return {"valid": False, "expires_at": "FXMIN_LIC_INVALID"}
    return {"valid": True, "expires_at": "2099-12-31"}


def _unused_licencia_helper(x):
    return x.upper()