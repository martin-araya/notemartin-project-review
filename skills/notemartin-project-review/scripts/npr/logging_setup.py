"""Configuracion de logging de la CLI `npr` (logs/npr.log)."""
from __future__ import annotations

import logging
import sys
from datetime import datetime, timezone
from pathlib import Path


def setup(workspace: Path | None) -> logging.Logger:
    logger = logging.getLogger("npr")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s",
                            datefmt="%Y-%m-%dT%H:%M:%S%z")

    stderr = logging.StreamHandler(sys.stderr)
    stderr.setLevel(logging.INFO)
    stderr.setFormatter(fmt)
    logger.addHandler(stderr)

    if workspace is not None:
        log_path = workspace / "logs" / "npr.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        fileh = logging.FileHandler(log_path, encoding="utf-8")
        fileh.setLevel(logging.DEBUG)
        fileh.setFormatter(fmt)
        logger.addHandler(fileh)

    logger.debug("logging inicializado workspace=%s ts=%s",
                 workspace, datetime.now(timezone.utc).isoformat())
    return logger