"""
OAuth2 client management utilities.

Functions for creating and managing OAuth2 clients.
"""

from __future__ import annotations

import secrets
import time
from typing import Any

from sqlalchemy.orm import Session

from gateway.models import OAuth2Client


def generate_client_id(nbytes: int = 24) -> str:
    """Generate a URL-safe client ID."""
    return secrets.token_urlsafe(nbytes)


def generate_client_secret(nbytes: int = 48) -> str:
    """Generate a URL-safe client secret."""
    return secrets.token_urlsafe(nbytes)


def create_client(
    db: Session,
    *,
    client_name: str,
    grant_types: list[str],
    redirect_uris: list[str],
    response_types: list[str],
    scope: str,
    token_endpoint_auth_method: str,
) -> OAuth2Client:
    """
    Create a new OAuth2 client registration.
    
    Args:
        db: Database session
        client_name: Human-readable client name
        grant_types: Allowed grant types (e.g., ["authorization_code", "refresh_token"])
        redirect_uris: Allowed redirect URIs
        response_types: Allowed response types (e.g., ["code"])
        scope: Space-separated scope string
        token_endpoint_auth_method: Auth method (e.g., "client_secret_basic", "none")
        
    Returns:
        The created OAuth2Client
    """
    client = OAuth2Client(
        client_id=generate_client_id(),
        client_id_issued_at=int(time.time()),
    )

    # Set client secret based on auth method
    if token_endpoint_auth_method == "none":
        client.client_secret = ""
    else:
        client.client_secret = generate_client_secret()

    # Set client metadata
    client_metadata: dict[str, Any] = {
        "client_name": client_name,
        "grant_types": grant_types,
        "redirect_uris": redirect_uris,
        "response_types": response_types,
        "scope": scope,
        "token_endpoint_auth_method": token_endpoint_auth_method,
    }
    client.set_client_metadata(client_metadata)

    db.add(client)
    db.commit()
    db.refresh(client)
    return client
