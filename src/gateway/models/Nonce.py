##### Imports ##################################################################

from __future__ import absolute_import
from gateway.models.Client import Client
from gateway.models.TimestampAddon import TimestampAddon
from Core import api_db

##### Globals ##################################################################

##### Functions ################################################################    

##### Classes ##################################################################

class Nonce(api_db.Model, TimestampAddon):
    __tablename__ = "nonces"

    id = api_db.Column(api_db.Integer, primary_key=True)

    timestamp = api_db.Column(api_db.Integer)
    nonce = api_db.Column(api_db.String(40))
    client_key = api_db.Column(api_db.String(40), api_db.ForeignKey('clients.client_key', name="nonces_ibfk_1"), nullable=False)
    client = api_db.relationship(Client)
    request_token = api_db.Column(api_db.String(50))
    access_token = api_db.Column(api_db.String(50))

    _client_key_idx = api_db.Index('client_key', client_key)  # foreign key index
    
##### Main #####################################################################
