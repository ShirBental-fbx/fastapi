from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
from starlette.requests import Request as StarletteRequest

@dataclass
class OAuthASGIRequest:
    method: str
    url: str
    headers: Mapping[str, str]
    query: Mapping[str, str]
    form: dict[str, Any]
    body: bytes

    @classmethod
    async def from_starlette(cls, request: StarletteRequest) -> "OAuthASGIRequest":
        body = await request.body()
        form = dict(await request.form()) if request.method in ("POST", "PUT", "PATCH") else {}
        return cls(
            method=request.method,
            url=str(request.url),
            headers={k.lower(): v for k, v in request.headers.items()},
            query=dict(request.query_params),
            form=form,
            body=body,
        )
