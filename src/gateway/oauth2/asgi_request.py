"""
ASGI/Starlette request adapter for Authlib.

Provides a bridge between FastAPI/Starlette requests and Authlib's OAuth2 server.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from urllib.parse import parse_qs

from starlette.requests import Request as StarletteRequest


@dataclass
class ASGIOAuthRequest:
    """
    OAuth2 request adapter for ASGI frameworks.
    
    Wraps a Starlette/FastAPI request in a format compatible with Authlib's
    AuthorizationServer methods.
    """
    
    method: str
    uri: str
    headers: dict[str, str]
    data: dict[str, Any] = field(default_factory=dict)
    body: bytes = b""
    
    @property
    def form(self) -> dict[str, Any]:
        """Alias for data, for Authlib compatibility."""
        return self.data
    
    @property
    def args(self) -> dict[str, str]:
        """Query string parameters."""
        if "?" in self.uri:
            query_string = self.uri.split("?", 1)[1]
            parsed = parse_qs(query_string)
            return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
        return {}

    @classmethod
    async def from_starlette(cls, request: StarletteRequest) -> "ASGIOAuthRequest":
        """
        Create an ASGIOAuthRequest from a Starlette/FastAPI request.
        
        Args:
            request: The incoming Starlette request
            
        Returns:
            ASGIOAuthRequest instance for use with Authlib
        """
        body = await request.body()
        
        data: dict[str, Any] = {}
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                form_data = await request.form()
                data = dict(form_data)
            except Exception:
                try:
                    data = await request.json()
                except Exception:
                    pass
        
        if request.method == "GET":
            data = dict(request.query_params)
        
        return cls(
            method=request.method,
            uri=str(request.url),
            headers={k.lower(): v for k, v in request.headers.items()},
            data=data,
            body=body,
        )
    
    def __getattr__(self, name: str) -> Any:
        """
        Provide attribute access for Authlib compatibility.
        """
        if name in self.data:
            return self.data[name]
        if name in self.args:
            return self.args[name]
        raise AttributeError(f"ASGIOAuthRequest has no attribute {name}")
