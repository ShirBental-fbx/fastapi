##### Imports ##################################################################

from __future__ import absolute_import
from common.db_handling.EncryptedString import EncryptedString
from models.TimestampAddon import TimestampAddon
from Core import api_db

import os

##### Globals ##################################################################

##### Functions ################################################################    

##### Classes ##################################################################

class Client(api_db.Model, TimestampAddon):
    __tablename__ = "clients"

    # human readable name, not required
    name = api_db.Column(api_db.String(40))

    # human readable description, not required
    description = api_db.Column(api_db.String(400))

    # # creator of the client, not required
    # user_id = Column(ForeignKey('user.id'))
    # # required if you need to support client credential
    # user = relationship('User')

    client_key = api_db.Column(api_db.String(40), primary_key=True)
    client_secret = api_db.Column(EncryptedString(os.environ['API_SECRETS_PASSWORD']), nullable=False)

    _realms = api_db.Column(api_db.Text)
    _redirect_uris = api_db.Column(api_db.Text)

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_realms(self):
        if self._realms:
            return self._realms.split()
        return []

##### Main #####################################################################
