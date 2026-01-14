"""
Database module.

Provides database session management and base model.
"""

from gateway.db.base import Base
from gateway.db.context import get_db_from_context, set_db
from gateway.db.session import SessionLocal, engine, get_db

__all__ = [
    "Base",
    "SessionLocal",
    "engine",
    "get_db",
    "get_db_from_context",
    "set_db",
]
