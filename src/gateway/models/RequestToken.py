##### Imports ##################################################################

from __future__ import absolute_import
from gateway.models.Client import Client
from gateway.models.TimestampAddon import TimestampAddon
from Core import api_db

##### Globals ##################################################################

##### Functions ################################################################    

##### Classes ##################################################################

class RequestToken(api_db.Model, TimestampAddon):
    __tablename__ = "request_tokens"

    id = api_db.Column(api_db.Integer, primary_key=True)
    fbbid = api_db.Column(api_db.Integer, nullable=True)

    client_key = api_db.Column(
        api_db.String(40), api_db.ForeignKey('clients.client_key', name="request_tokens_ibfk_1"),
        nullable=False,
    )
    client = api_db.relationship(Client)

    token = api_db.Column(api_db.String(255))  # Indexed
    secret = api_db.Column(api_db.String(255), nullable=False)

    verifier = api_db.Column(api_db.String(255))

    redirect_uri = api_db.Column(api_db.Text)
    _realms = api_db.Column(api_db.Text)

    _client_key_idx = api_db.Index('client_key', client_key)  # foreign key index
    _token_idx = api_db.Index('ix_request_tokens_token', token)

    @property
    def realms(self):
        if self._realms:
            return self._realms.split()
        return []
    
##### Main #####################################################################
