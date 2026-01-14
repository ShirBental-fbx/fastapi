from __future__ import annotations

from collections.abc import Generator
from sqlalchemy.orm import Session

from gateway.db.context import get_db_from_context
from gateway.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    existing = get_db_from_context()
    if existing is not None:
        yield existing
        return

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
