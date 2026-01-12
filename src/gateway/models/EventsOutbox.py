from fundbox.common.data_warehouse_api.outbox import create_table_model
from Core import api_db

EventsOutbox = create_table_model(api_db.Model)
