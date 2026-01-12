# Imports ##################################################################

from __future__ import absolute_import

import uuid
from datetime import datetime, timedelta
from secrets import token_urlsafe

from sqlalchemy import Index

from common.db_handling.EncryptedString import EncryptedString
from models.OldPlaidToken import OldPlaidToken
from models.TimestampAddon import TimestampAddon
from Core import api_db
import os

# Globals ##################################################################

DAYS_TOKEN_GIVES_ACCESS = 15
DAYS_TOKEN_REFRESHABLE = 30

# Functions ################################################################


def generate_plaid_user_id():
    return str(uuid.uuid4())


def generate_auth_token():
    return token_urlsafe(32)


def get_access_until_value():
    return datetime.now() + timedelta(days=DAYS_TOKEN_GIVES_ACCESS)


def get_refreshable_until_value():
    return datetime.now() + timedelta(days=DAYS_TOKEN_REFRESHABLE)


# Classes ##################################################################


class PlaidToken(api_db.Model, TimestampAddon):
    __tablename__ = "plaid_tokens"

    id = api_db.Column(api_db.Integer, primary_key=True)
    user_id = api_db.Column(api_db.Integer, nullable=False)
    fbbid = api_db.Column(api_db.Integer, nullable=False)  # Indexed

    plaid_user_id = api_db.Column(api_db.String(40), default=generate_plaid_user_id, nullable=False)  # Indexed
    auth_token = api_db.Column(EncryptedString(os.environ['PX_API_SECRETS_PASSWORD']), default=generate_auth_token, nullable=False)

    has_access_until = api_db.Column(api_db.DateTime, default=get_access_until_value)
    refreshable_until = api_db.Column(api_db.DateTime, default=get_refreshable_until_value)

    triggered_reversed_token = api_db.Column(api_db.Boolean, default=False)

    is_valid = api_db.Column(api_db.Boolean, default=True)

    old_plaid_tokens = api_db.relationship(OldPlaidToken, backref='plaid_token')

    _fbbid_idx = Index('plaid_tokens_fbbid_idx', fbbid)
    _plaid_user_id_idx = Index('plaid_tokens_plaid_user_id_idx', plaid_user_id)

    @property
    def has_access(self):
        return self.has_access_until > datetime.now() and self.is_valid

    @property
    def is_refreshable(self):
        return self.refreshable_until > datetime.now() and self.is_valid

    def refresh_token(self):
        self.old_plaid_tokens.append(OldPlaidToken(plaid_token_id=self.id, auth_token=self.auth_token))
        self.auth_token = generate_auth_token()
        self.has_access_until = get_access_until_value()
        self.refreshable_until = get_refreshable_until_value()

# Main #####################################################################
