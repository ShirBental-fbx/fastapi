##### Imports ##################################################################

from __future__ import absolute_import
from common.db_handling.EncryptedString import EncryptedString
from models.Client import Client
from models.TimestampAddon import TimestampAddon
from Core import api_db

import os

##### Globals ##################################################################

##### Functions ################################################################    

##### Classes ##################################################################

class AccessToken(api_db.Model, TimestampAddon):
    __tablename__ = "access_tokens"

    id = api_db.Column(api_db.Integer, primary_key=True)
    client_key = api_db.Column(api_db.String(40), api_db.ForeignKey('clients.client_key', name="access_tokens_ibfk_1"), nullable=False)
    client = api_db.relationship(Client)

    fbbid = api_db.Column(api_db.Integer, nullable=False)

    token = api_db.Column(api_db.String(255))
    secret = api_db.Column(EncryptedString(os.environ['API_SECRETS_PASSWORD']))

    _realms = api_db.Column(api_db.Text)

    _client_key_idx = api_db.Index('client_key', client_key)  # foreign key index

    @property
    def realms(self):
        if self._realms:
            return self._realms.split()
        return []

    # This is needed for the package, as it assumes the access token has a user
    @property
    def user(self):
        return self.fbbid

##### Main #####################################################################
