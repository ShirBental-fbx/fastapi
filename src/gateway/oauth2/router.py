from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from gateway.oauth2.server import build_authorization_server
from gateway.oauth2.asgi_request import ASGIOAuthRequest

router = APIRouter()
server = build_authorization_server()

@router.get("/oauth/authorize")
async def authorize_get(request: Request):
    oauth_req = await ASGIOAuthRequest.from_starlette(request)
    return HTMLResponse("TODO authorize page")

@router.post("/oauth/authorize")
async def authorize_post(request: Request):
    oauth_req = await ASGIOAuthRequest.from_starlette(request)
    # create_authorization_response(...) של core
    return Response(content=b"TODO", status_code=501)

@router.post("/oauth/token")
async def issue_token(request: Request):
    oauth_req = await ASGIOAuthRequest.from_starlette(request)
    # create_token_response(...)
    return Response(content=b"TODO", status_code=501)

@router.post("/oauth/revoke")
async def revoke_token(request: Request):
    oauth_req = await ASGIOAuthRequest.from_starlette(request)
    return Response(content=b"TODO", status_code=501)
