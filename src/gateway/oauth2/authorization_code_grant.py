from __future__ import annotations

import secrets

from authlib.oauth2.rfc6749 import grants
from sqlalchemy import select

from gateway.db.context import get_db_from_context
from gateway.models import OAuth2AuthorizationCode


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def create_authorization_code(self, client, fbbid, request):
        db = get_db_from_context()
        code = secrets.token_urlsafe(48)
        item = OAuth2AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            fbbid=fbbid,
            code_challenge=request.form.get("code_challenge"),
            code_challenge_method=request.form.get("code_challenge_method"),
        )
        db.add(item)
        db.commit()
        return code

    def parse_authorization_code(self, code, client):
        db = get_db_from_context()

        stmt = select(OAuth2AuthorizationCode).where(
            OAuth2AuthorizationCode.code == code,
            OAuth2AuthorizationCode.client_id == client.client_id,
        )
        item = db.execute(stmt).scalars().first()
        if item and not item.is_expired():
            return item
        return None

    def delete_authorization_code(self, authorization_code):
        db = get_db_from_context()
        db.delete(authorization_code)
        db.commit()

    def authenticate_user(self, authorization_code):
        return authorization_code.fbbid
