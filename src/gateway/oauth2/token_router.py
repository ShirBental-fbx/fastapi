"""
OAuth2 Token endpoints using external authentication service.

This module provides token endpoints that delegate to an external
authentication service (fundbox.sdk.authentication).
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/oauth", tags=["oauth2-external"])


class TokenPayload(BaseModel):
    """Request body for token endpoint."""
    grant_type: str
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    refresh_token: Optional[str] = None


class RevokePayload(BaseModel):
    """Request body for token revocation endpoint."""
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    token: Optional[str] = None


def _get_grant_type(grant_type: str):
    """
    Convert grant type string to SDK enum.
    
    This function requires fundbox-sdk to be installed.
    """
    try:
        from fundbox.sdk.authentication.dto.oauth2.token_request import GrantType
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="External authentication service not configured"
        )
    
    if grant_type == "client_credentials":
        return GrantType.CLIENT_CREDENTIALS
    if grant_type == "refresh_token":
        return GrantType.REFRESH_TOKEN
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid grant type",
    )


@router.post("/external/token")
def issue_token_external(payload: TokenPayload):
    """
    Issue token via external authentication service.
    
    This endpoint delegates token issuance to the Fundbox authentication
    service for client credentials and refresh token grants.
    """
    try:
        from fundbox.common.service_client import RemoteException
        from fundbox.sdk.authentication.client import get_authentication_service_api_client
        from fundbox.sdk.authentication.dto.oauth2.token_request import TokenRequest
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="External authentication service not configured"
        )
    
    try:
        req = TokenRequest(
            grant_type=_get_grant_type(payload.grant_type),
            client_id=payload.client_id,
            client_secret=payload.client_secret,
            refresh_token=payload.refresh_token,
        )
        result = get_authentication_service_api_client().issue_oauth2_client_token(req)
        return asdict(result)

    except (RemoteException.InvalidCredentials, RemoteException.InvalidGrantException) as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))
    except RemoteException.AuthorizationServerException as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))


@router.post("/external/revoke", status_code=status.HTTP_204_NO_CONTENT)
def revoke_token_external(payload: RevokePayload):
    """
    Revoke token via external authentication service.
    
    This endpoint delegates token revocation to the Fundbox authentication service.
    """
    try:
        from fundbox.common.service_client import RemoteException
        from fundbox.sdk.authentication.client import get_authentication_service_api_client
        from fundbox.sdk.authentication.dto.oauth2.token_request import RevokeTokenRequest
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="External authentication service not configured"
        )
    
    try:
        req = RevokeTokenRequest(
            client_id=payload.client_id,
            client_secret=payload.client_secret,
            token=payload.token,
        )
        get_authentication_service_api_client().revoke_oauth2_token(req)
        return None

    except (RemoteException.InvalidCredentials, RemoteException.InvalidToken) as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))
    except RemoteException.AuthorizationServerException as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
