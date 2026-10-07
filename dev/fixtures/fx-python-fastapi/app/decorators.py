"""Custom decorators that register routes as side effect (trampa E05).

Trampa E05: @track_request incrementa un counter global y registra
la funcion en una lista global _REGISTERED_ROUTES. NO preserva
los metadatos del wrapper (trampa P05), por lo que __name__,
__doc__, __signature__ se pierden y FastAPI ve el endpoint con un
nombre que no es el original.
"""
from typing import Callable

_REQUEST_REGISTRY: dict[str, int] = {}
_REGISTERED_ROUTES: list[Callable] = []


def get_request_registry() -> dict[str, int]:
    return dict(_REQUEST_REGISTRY)


def get_registered_routes() -> list[Callable]:
    return list(_REGISTERED_ROUTES)


def track_request(func: Callable) -> Callable:
    """Decorador que registra la funcion y anade side effect de tracking.

    Trampa E05: ademas de wrap, registra la ruta en _REGISTERED_ROUTES
    y actualiza un counter global _REQUEST_REGISTRY.
    Trampa P05: el wrapper no preserva __name__, __doc__, __signature__
    del callable original; FastAPI ve el endpoint con un nombre que
    no es el de la funcion decorada.
    """
    name = func.__name__
    _REQUEST_REGISTRY.setdefault(name, 0)
    _REGISTERED_ROUTES.append(func)

    def wrapper(*args, **kwargs):
        _REQUEST_REGISTRY[name] += 1
        return func(*args, **kwargs)

    return wrapper