# Imports ##################################################################

from __future__ import absolute_import

from authlib.integrations.sqla_oauth2 import OAuth2TokenMixin
from Core import api_db


# Globals ##################################################################

# Functions ################################################################

# Classes ##################################################################


class OAuth2Token(api_db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = api_db.Column(api_db.Integer, primary_key=True)
    fbbid = api_db.Column(api_db.Integer)


# Main #####################################################################
