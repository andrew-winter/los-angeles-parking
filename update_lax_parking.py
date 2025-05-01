import os
import requests
import sqlite3
import pandas as pd
from functions import create_endpoint
from functions import request_endpoint
from functions import frame_response

# %%
# Constants
app_token = os.environ.get("LA_PARKING_APP_TOKEN")
data_lax_parking_lots = "https://data.lacity.org/resource/dik5-hwp6"
headers = {"X-Auth-Token": app_token}

# %%
# Request LAX parking lot data and convert from JSON to a pandas DataFrame
endpoint = create_endpoint(data_lax_parking_lots, limit=100, offset=0, format="json")
response = request_endpoint(endpoint)
df = frame_response(response)

# %%


# %%
# Database
database = r'data/lax_parking.db'
connection = sqlite3.connect(database)
cursor = connection.cursor()
sql_create_parking_lots = """
    SELECT
        PARKING_LOTS_NOW(
            key_value, lotdescription)
"""
cursor.execute(sql_create_parking_lots)
connection.close()

# %%
df.to_sql(name="PARKING_LOTS_NOW", con=connection, if_exists="replace")

# %%


# %%
#connection = sqlite3.connect('data\dbs\pbp.sqlite')

#data_dictionary.to_sql(name='data_dictionary', con=connection, if_exists='fail')

#pbp.to_sql(name=f'pbp_{yr}', con=connection, if_exists='fail')
