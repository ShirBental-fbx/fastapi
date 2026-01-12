from __future__ import annotations

from authlib.oauth2.rfc6749 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7636 import CodeChallenge

from gateway.models.OAuth2Client import OAuth2Client
from gateway.models.OAuth2Token import OAuth2Token
from gateway.oauth2.authorization_code_grant import AuthorizationCodeGrant
from gateway.oauth2.refresh_token_grant import RefreshTokenGrant
from gateway.oauth2.storage import query_client, save_token

def build_authorization_server() -> AuthorizationServer:
    server = AuthorizationServer(query_client=query_client, save_token=save_token)

    # grants
    server.register_grant(AuthorizationCodeGrant, [CodeChallenge(required=False)])
    server.register_grant(RefreshTokenGrant)

    return server
