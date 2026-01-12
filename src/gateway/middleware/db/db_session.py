# src/gateway/middleware/db/session.py
from __future__ import annotations

from typing import Callable
from starlette.requests import Request
from starlette.responses import Response

from gateway.db.session import SessionLocal
from gateway.db.context import set_db

async def db_session_middleware(
    request: Request,
    call_next: Callable[[Request], Response],
) -> Response:
    db = SessionLocal()
    try:
        set_db(db)
        return await call_next(request)
    finally:
        db.close()
