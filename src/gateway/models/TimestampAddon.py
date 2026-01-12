##### Imports ##################################################################

from __future__ import absolute_import
from Core import api_db

##### Globals ##################################################################

##### Functions ################################################################

##### Classes ##################################################################

class TimestampAddon(object):
    last_modified_time = api_db.Column(api_db.TIMESTAMP, default=api_db.func.current_timestamp(), onupdate=api_db.func.current_timestamp())
    created_time = api_db.Column(api_db.TIMESTAMP, default=api_db.func.current_timestamp())
    
##### Main #####################################################################

