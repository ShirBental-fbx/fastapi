"""
OAuth2 Authorization Code Grant implementation.

Handles the authorization code flow according to RFC 6749.
"""

from __future__ import annotations

import secrets
from typing import Any

from authlib.oauth2.rfc6749 import grants
from sqlalchemy import select

from gateway.db.context import get_db_from_context
from gateway.models import OAuth2AuthorizationCode, OAuth2Client


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    """
    Authorization code grant type for OAuth2.
    
    Implements the full authorization code flow including PKCE support.
    """
    
    # Token endpoint authentication methods
    TOKEN_ENDPOINT_AUTH_METHODS = [
        "client_secret_basic",
        "client_secret_post",
        "none",
    ]

    def create_authorization_code(
        self, 
        client: OAuth2Client, 
        fbbid: int, 
        request: Any
    ) -> str:
        """
        Create and store a new authorization code.
        
        Args:
            client: The OAuth2 client making the request
            fbbid: The Fundbox business ID of the authorizing user
            request: The authorization request
            
        Returns:
            The generated authorization code string
        """
        db = get_db_from_context()
        code = secrets.token_urlsafe(48)
        
        item = OAuth2AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            fbbid=fbbid,
            code_challenge=request.data.get("code_challenge"),
            code_challenge_method=request.data.get("code_challenge_method"),
        )
        db.add(item)
        db.commit()
        return code

    def parse_authorization_code(
        self, 
        code: str, 
        client: OAuth2Client
    ) -> OAuth2AuthorizationCode | None:
        """
        Retrieve and validate an authorization code.
        
        Args:
            code: The authorization code to validate
            client: The client claiming the code
            
        Returns:
            The OAuth2AuthorizationCode if valid and not expired, None otherwise
        """
        db = get_db_from_context()
        stmt = select(OAuth2AuthorizationCode).where(
            OAuth2AuthorizationCode.code == code,
            OAuth2AuthorizationCode.client_id == client.client_id,
        )
        item = db.execute(stmt).scalars().first()
        
        if item and not item.is_expired():
            return item
        return None

    def delete_authorization_code(
        self, 
        authorization_code: OAuth2AuthorizationCode
    ) -> None:
        """
        Delete a used authorization code.
        
        Called after the code has been exchanged for tokens.
        
        Args:
            authorization_code: The code to delete
        """
        db = get_db_from_context()
        db.delete(authorization_code)
        db.commit()

    def authenticate_user(
        self, 
        authorization_code: OAuth2AuthorizationCode
    ) -> int | None:
        """
        Return the user (fbbid) who authorized the code.
        
        Args:
            authorization_code: The validated authorization code
            
        Returns:
            The fbbid of the authorizing user
        """
        return authorization_code.fbbid
