import os
import requests
import pandas as pd

# %%
# Constants
app_token = os.environ.get("LA_PARKING_APP_TOKEN")
data_lax_lots = "https://data.lacity.org/resource/dik5-hwp6"
data_meter_occupancy = "https://data.lacity.org/resource/e7h6-4a3e"
data_meter_policy = "https://data.lacity.org/resource/s49e-q6j2"
headers = {"X-Auth-Token": app_token}

# %%
# Function create_endpoint()
def create_endpoint(
    dataset: str,
    limit: int = 1000,
    offset: int = 0,
    *,
    order: str = "",
    desc: bool = False,
    format: str = "json",
    query: str = ""
) -> str:
    """Creates an API endpoint to access the city of Los Angeles' open data.

    Limit n records. "Page" through results by offsetting and choosing
    a column to order by. Specify format. Add a query.
    """
    resource = f"{dataset}.{format}"
    params = []
    if limit > 0:
        params.append(f"$limit={limit}")
    if offset >= 0:
        params.append(f"$offset={offset}")
    if order:
        # Ascending by default
        if desc:
            params.append(f"$order={order} DESC")
        else:
            params.append(f"$order={order} ASC")
    if query:
        params.append(query)

    # Combine the optional params with "&".
    if params:
        params_string = "&".join(params)
        resource += f"?{params_string}"
    return resource

# %%
# Function request_endpoint()
def request_endpoint(url: str):
    """Fetches data from a given endpoint.

    Expect to return a list of dictionaries.
    """
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        response = None
    return response

# %%
# Function frame_response()
def frame_response(response: requests.Response):
    """Converts response into a pandas DataFrame.
    
    Lorem ipsum.
    """
    try:
        json = response.json()
        df = pd.DataFrame(json)
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON:\n{e}")
        df = pd.DataFrame()
    return df

# %%
# LAX parking lot example
endpoint_lax = create_endpoint(
    data_lax_lots,
    limit=100, offset=0, format="json")
response_lax = request_endpoint(endpoint_lax)
df_lax = frame_response(response_lax)

# %%
# Los Angeles public parking meter occupancy example
times = 10
limit = 1000
df_meter_occupancy = pd.DataFrame()
for end in range(0, times*limit, limit):
    endpoints = create_endpoint(
        dataset=data_meter_occupancy,
        limit=limit, offset=end,
        order="spaceid", desc=False, format="json")
    responses = request_endpoint(endpoints)
    if len(responses.json()) > 0:
        dfs = frame_response(responses)
        df_meter_occupancy = pd.concat(
            [dfs, df_meter_occupancy],
            ignore_index=True)
    else:
        break

# %%


# %%

