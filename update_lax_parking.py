import os
import requests
import pandas as pd
import sqlite3
from functions import make_endpoint
from functions import query_endpoint
from functions import check_response

# %%
# Constants
app_token = os.environ.get("LA_PARKING_APP_TOKEN")
headers = {"X-App-Token": app_token}

# Data sources: data.lacity.org
id_meter_policy = "s49e-q6j2"
id_meter_occupancy = "e7h6-4a3e"
id_lax_lots = "dik5-hwp6"

# %%
# Occupancy query
endp_occupancy = make_endpoint(id_meter_occupancy, query=True)
soql_occupancy = "SELECT * ORDER BY spaceid DESC"
resp_occupancy = query_endpoint(endp_occupancy, query=soql_occupancy, page=1, limit=5000)
json_occupancy = check_response(resp_occupancy)

# %%
# Policy queries
pages = 3
data_policy = []
endp_policy = make_endpoint(id_meter_policy, query=True)
soql_policy = "SELECT * ORDER BY spaceid DESC"
for page in range(1, pages+1):
    resp_policy = query_endpoint(endp_policy, query=soql_policy, page=page, limit=1000)
    json_policy = check_response(resp_policy)
    data_policy.append(json_policy)

# Not sure what to do with result
# The individual dictionaries can be coerced into dataframe
# Not sure how to combine properly
data_policy[0]


# %%
# Update current occupancy in database
#conn = sqlite3.connect("data/parking.db")
#curs = conn.cursor()
#curs.execute("DROP TABLE IF EXISTS meters_now;")
#curs.execute("CREATE TABLE meters_now(spaceid, eventtime, occupancystate);")
#curs.executemany("INSERT INTO meters_now VALUES(:spaceid, :eventtime, :occupancystate);", response_json)
#conn.commit()
#conn.close()
#df.to_sql(name="meters_now", con=connection, if_exists="replace")


# %%
# Verify current occupancy
#conn_new = sqlite3.connect("data/parking.db")
#curs_new = conn_new.cursor()
#resu_new = curs_new.execute("SELECT spaceid, occupancystate, eventtime FROM meters_now ORDER BY occupancystate DESC, eventtime DESC")
#space_id, occupancy_state, event_time = resu_new.fetchone()
#print(f"The most recently available LADOT metered spot is {space_id} as of {event_time} UTC")
#conn_new.close()



