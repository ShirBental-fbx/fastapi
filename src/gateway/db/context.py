from __future__ import annotations
from contextvars import ContextVar
from sqlalchemy.orm import Session

_db: ContextVar[Session | None] = ContextVar("db_session", default=None)

def set_db(session: Session) -> None:
    _db.set(session)

def get_db_from_context() -> Session:
    session = _db.get()
    if session is None:
        raise RuntimeError("DB session is not set in context")
    return session
