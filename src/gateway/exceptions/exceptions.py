from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RemoteException(Exception):
    message: str
    status_code: int | None = None
    response_body: str | None = None

    def __str__(self) -> str:
        return self.message
