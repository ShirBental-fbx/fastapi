# """
# OAuth2 Authorization Server configuration.
#
# Sets up the Authlib AuthorizationServer with supported grants and endpoints.
# """
#
# from __future__ import annotations
#
# from typing import Any, Callable
#
# from authlib.oauth2 import AuthorizationServer as BaseAuthorizationServer
# from authlib.oauth2.rfc6749 import grants
# from authlib.oauth2.rfc7636 import CodeChallenge
#
# from gateway.models import OAuth2Client, OAuth2Token
# from gateway.oauth2.authorization_code_grant import AuthorizationCodeGrant
# from gateway.oauth2.refresh_token_grant import RefreshTokenGrant
# from gateway.oauth2.storage import query_client, save_token
#
#
# class AuthorizationServer(BaseAuthorizationServer):
#     """
#     Custom Authorization Server for FastAPI/ASGI applications.
#
#     Extends Authlib's base AuthorizationServer with query_client and save_token
#     functions that work with our SQLAlchemy models.
#     """
#
#     def __init__(
#         self,
#         query_client: Callable[[str], OAuth2Client | None],
#         save_token: Callable[[dict[str, Any], Any], None],
#     ):
#         super().__init__()
#         self._query_client = query_client
#         self._save_token = save_token
#
#     def query_client(self, client_id: str) -> OAuth2Client | None:
#         """Query OAuth2 client by client_id."""
#         return self._query_client(client_id)
#
#     def save_token(self, token: dict[str, Any], request: Any) -> None:
#         """Save issued token to database."""
#         self._save_token(token, request)
#
#     def generate_token(
#         self,
#         grant_type: str,
#         client: OAuth2Client,
#         user: Any = None,
#         scope: str | None = None,
#         expires_in: int | None = None,
#         include_refresh_token: bool = True,
#     ) -> dict[str, Any]:
#         """Generate access token dict."""
#         from authlib.oauth2.rfc6749 import TokenMixin
#         from authlib.common.security import generate_token
#
#         token = {
#             "token_type": "Bearer",
#             "access_token": generate_token(42),
#         }
#
#         if expires_in:
#             token["expires_in"] = expires_in
#         else:
#             token["expires_in"] = 3600  # Default 1 hour
#
#         if include_refresh_token:
#             token["refresh_token"] = generate_token(48)
#
#         if scope:
#             token["scope"] = scope
#
#         return token
#
#
# def build_authorization_server() -> AuthorizationServer:
#     """
#     Build and configure the OAuth2 authorization server.
#
#     Registers:
#     - Authorization Code Grant (with optional PKCE)
#     - Refresh Token Grant
#
#     Returns:
#         Configured AuthorizationServer instance
#     """
#     server = AuthorizationServer(
#         query_client=query_client,
#         save_token=save_token,
#     )
#
#     # Register grants
#     server.register_grant(
#         AuthorizationCodeGrant,
#         [CodeChallenge(required=False)],  # PKCE optional for backwards compatibility
#     )
#     server.register_grant(RefreshTokenGrant)
#
#     return server
#
#
# # Global server instance (lazy initialization)
# _authorization_server: AuthorizationServer | None = None
#
#
# def get_authorization_server() -> AuthorizationServer:
#     """Get or create the authorization server instance."""
#     global _authorization_server
#     if _authorization_server is None:
#         _authorization_server = build_authorization_server()
#     return _authorization_server
#
#
# # For backwards compatibility
# authorization_server = build_authorization_server()
