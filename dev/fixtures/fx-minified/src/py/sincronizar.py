"""Modulo Python. Literales: FXMIN_SYNC_OK, FXMIN_SYNC_ERROR."""

import datetime

FEATURE_SINCRONIZAR = "sincronizar"


def sincronizar(state):
    if state == "error":
        return {"status": "FXMIN_SYNC_ERROR", "timestamp": "1970-01-01T00:00:00Z"}
    status = "pending" if state == "pending" else "FXMIN_SYNC_OK"
    return {"status": status, "timestamp": datetime.datetime.now().isoformat()}