# """
# OAuth2 Refresh Token Grant implementation.
#
# Handles token refresh according to RFC 6749.
# """
#
# from __future__ import annotations
#
# from authlib.oauth2.rfc6749 import grants
# from sqlalchemy import select
#
# from gateway.db.context import get_db_from_context
# #from gateway.models import OAuth2Token
#
#
# class RefreshTokenGrant(grants.RefreshTokenGrant):
#     """
#     Refresh token grant type for OAuth2.
#
#     Allows clients to obtain a new access token using a refresh token.
#     """
#
#     # Include scope in refresh token response
#     INCLUDE_NEW_REFRESH_TOKEN = True
#
#     def authenticate_refresh_token(self, refresh_token: str) -> OAuth2Token | None:
#         """
#         Validate and retrieve token by refresh_token value.
#
#         Args:
#             refresh_token: The refresh token string
#
#         Returns:
#             OAuth2Token if valid and active, None otherwise
#         """
#         db = get_db_from_context()
#         stmt = select(OAuth2Token).where(OAuth2Token.refresh_token == refresh_token)
#         token = db.execute(stmt).scalars().first()
#
#         if token and token.is_refresh_token_active():
#             return token
#         return None
#
#     def authenticate_user(self, credential: OAuth2Token) -> int | None:
#         """
#         Return the user (fbbid) associated with the token.
#
#         Args:
#             credential: The validated OAuth2Token
#
#         Returns:
#             The fbbid of the token owner
#         """
#         return credential.fbbid
#
#     def revoke_old_credential(self, credential: OAuth2Token) -> None:
#         """
#         Revoke the old refresh token after issuing a new one.
#
#         Args:
#             credential: The old OAuth2Token to revoke
#         """
#         db = get_db_from_context()
#         credential.revoked = True
#         db.add(credential)
#         db.commit()
