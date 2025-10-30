"""
Módulo core contendo configurações fundamentais do sistema.
"""

from core.config import settings
from core.database import Base, engine, get_db
from core.security import (
    create_access_token, 
    verify_password, 
    get_password_hash,
    get_current_user,
    get_current_admin,
    security
)

__all__ = [
    "settings",
    "Base", 
    "engine", 
    "get_db",
    "create_access_token",
    "verify_password", 
    "get_password_hash",
    "get_current_user",
    "get_current_admin", 
    "security"
]