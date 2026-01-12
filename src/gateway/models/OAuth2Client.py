# Imports ##################################################################

from __future__ import absolute_import

from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin

from Core import api_db


# Globals ##################################################################

# Functions ################################################################

# Classes ##################################################################


class OAuth2Client(api_db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = api_db.Column(api_db.Integer, primary_key=True)

# Main #####################################################################
