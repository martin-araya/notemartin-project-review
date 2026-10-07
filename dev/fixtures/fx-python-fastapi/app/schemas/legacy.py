"""Legacy Pydantic v2 schema (trampa S02: dead code).

LegacyUsuarioSchema existe pero nunca se importa en el codigo del
fixture. La skill debe detectarlo via grep.
"""
from pydantic import BaseModel


class LegacyUsuarioSchema(BaseModel):
    """Modelo legacy que existia en versiones anteriores del API.

    Trampa S02: este modelo NO se usa en ningun endpoint, schema
    activo ni migracion. Solo existe por compatibilidad historica.
    """
    legacy_id: int
    legacy_username: str
    legacy_role: str = "viewer"