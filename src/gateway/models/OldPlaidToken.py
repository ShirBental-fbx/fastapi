# Imports ##################################################################

from __future__ import absolute_import

from common.db_handling.EncryptedString import EncryptedString
from gateway.models.TimestampAddon import TimestampAddon
from Core import api_db
import os

# Globals ##################################################################

# Functions ################################################################

# Classes ##################################################################


class OldPlaidToken(api_db.Model, TimestampAddon):
    __tablename__ = "old_plaid_tokens"

    id = api_db.Column(api_db.Integer, primary_key=True)
    plaid_token_id = api_db.Column(api_db.Integer, api_db.ForeignKey("plaid_tokens.id", name="plaid_tokens_id"), nullable=False)
    auth_token = api_db.Column(EncryptedString(os.environ['PX_API_SECRETS_PASSWORD']), nullable=False)

    _plaid_token_id_idx = api_db.Index('plaid_tokens_id', plaid_token_id)  # foreign key index

# Main #####################################################################
