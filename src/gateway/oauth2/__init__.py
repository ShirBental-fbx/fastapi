from authlib.integrations.flask_oauth2 import AuthorizationServer, ResourceProtector
from authlib.integrations.sqla_oauth2 import (
    create_query_client_func,
    create_revocation_endpoint,
    create_bearer_token_validator,
)
from authlib.oauth2.rfc7636 import CodeChallenge

from gateway.core import api_db
from gateway.models.OAuth2Client import OAuth2Client
from gateway.models.OAuth2Token import OAuth2Token
from gateway.models.oauth2.AuthorizationCodeGrant import AuthorizationCodeGrant
from gateway.models.oauth2.OAuth2Manager import save_token
from gateway.models.oauth2.RefreshTokenGrant import RefreshTokenGrant
