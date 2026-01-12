from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional
from urllib.parse import urlsplit

from starlette.requests import Request

@dataclass
class ASGIOAuthRequest:
    method: str
    url: str
    headers: Mapping[str, str]
    body: bytes
    query_string: str

    @classmethod
    async def from_starlette(cls, request: Request) -> "ASGIOAuthRequest":
        body = await request.body()
        return cls(
            method=request.method,
            url=str(request.url),
            headers={k.lower(): v for k, v in request.headers.items()},
            body=body,
            query_string=request.url.query,
        )
