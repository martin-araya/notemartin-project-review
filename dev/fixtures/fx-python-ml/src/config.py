from __future__ import annotations

from hydra.core.global_hydra import GlobalHydra


def get_param(name: str, default=None):
    """Lee un parametro de Hydra Compose o retorna default si no esta disponible."""
    if not GlobalHydra.instance().is_initialized():
        return default
    from hydra import compose_compose

    cfg = GlobalHydra.instance().config_loader().get_config().cfg
    parts = name.split(".")
    value = cfg
    try:
        for part in parts:
            value = value[part]
        return value
    except (KeyError, TypeError):
        return default


__all__ = ["get_param"]