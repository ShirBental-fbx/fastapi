# Imports ##################################################################

from __future__ import absolute_import
from authlib.oauth2.rfc6749 import grants
from Core import api_db
from models.OAuth2Token import OAuth2Token


# Globals ##################################################################

# Functions ################################################################

# Classes ##################################################################

class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        token = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if token and token.is_refresh_token_active():
            return token

    def authenticate_user(self, credential):
        return credential.fbbid

    def revoke_old_credential(self, credential):
        credential.revoked = True
        api_db.session.add(credential)
        api_db.session.commit()



# Main #####################################################################
