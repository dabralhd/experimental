import httpx
import json
import prjapi_endpoints
import logging

logger = logging.getLogger("tools-httpx")
logger.setLevel(logging.INFO)
# Add this block to ensure logs are shown in the console
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# --- Configuration ---
# Replace with the actual base URL of your API
# For example, if your API is running locally on port 8080:
BASE_URL = "https://dev.stm-vespucci.com:443/svc/project-api/3" # According to servers: - url: /3 in your spec

# Your Bearer Token (JWT)
# Replace with your actual JWT token. You would typically obtain this after
# a successful login or authentication process.
YOUR_BEARER_TOKEN = "eyJraWQiOiJcL3JIS3FCbG5JVldiU2RqdEJqODRQaDNyUk5SWWh4cnR6RFwvOXFTK0Q3aWc9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzMzRjNjVhNS0xNDk1LTQ1M2EtYTZkZS00ZDM4NGE3ODEwMDAiLCJjb2duaXRvOmdyb3VwcyI6WyJ3aGl0ZWxpc3QiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfOXdlbnNFNVJaIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiNHNoYjE3OGdsbWxsc3I3NWdmb2JoZmRzYmEiLCJvcmlnaW5fanRpIjoiZDk4OTE1MzgtMjcyYy00NWM2LWFmNzQtZjJhN2UyNjI4ZjcyIiwiZXZlbnRfaWQiOiI1NWNmY2UxNi03ZWMzLTQzZWEtYTMyMi03ODQ3Nzg3YTgwMzEiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIGh0dHBzOlwvXC9vYXV0aDIuZGV2LnN0bS12ZXNwdWNjaS5jb21cL3Rlc3QgcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3NTMyMDU4MDIsImV4cCI6MTc1MzI5MjIwMiwiaWF0IjoxNzUzMjA1ODAyLCJqdGkiOiI4NmMzMzA5ZS02NDhjLTQ5ZDAtOTIyMS0wYjJjODcwOWU5Y2UiLCJ1c2VybmFtZSI6IjMzNGM2NWE1LTE0OTUtNDUzYS1hNmRlLTRkMzg0YTc4MTAwMCJ9.kC0g3NSSUdMxRyjW6Bav-c-aibndM7T_3ayqxUd-KFA5hkFZHbwr7aCcTgYNdKz7Gt5EL0GWPr2Pq3Vn2HstJ6O_mglyquNWP-z_RjM9v59sKsDY-VtrnhcsZ7h3o_VQB9EvFdwq0f5AEYQJnrqHhQWicsjbn400EOVEraYti7oeX-oiyD8_FpPFbbqSBGBgHD9Du3SDBLQDyDylykGCo0mofr9G6iRq-uIkdElUwabTweX-sbDg_1fR6ejYkmJsHVH-KwpKxdS6rkoWss8cl8T1sWk5bcw2QGpn53_L2QAXrBRjI_J1zBNMAZirDeVm952zc0ZURB-qljm0-tkxXg"

# Optional: as_org query parameter
# If you want to fetch projects as a specific organization, uncomment and set this.
# ORG_ID = "8s28038jgmf8cn8a7ka2hzhj10" # Example from spec
ORG_ID = None # Set to None if not using

# --- Construct the Request ---
api_endpoint = "/projects"
request_url = f"{BASE_URL}{api_endpoint}"

headers = {
    "Authorization": f"Bearer {YOUR_BEARER_TOKEN}",
    "Accept": "application/json" # As specified in the responses content type
}

params = {}
if ORG_ID:
    params["as_org"] = ORG_ID

# --- Make the GET Request ---
try:
    # Use httpx.Client for persistent connections if making multiple requests
    with httpx.Client() as client:
        logger.info(f"Making GET request to: {request_url}")
        logger.debug(f"Headers: {headers}")
        if params:
            logger.info(f"Params: {params}")

        response = client.get(request_url, headers=headers, params=params)

        # --- Handle the Response ---
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        logger.debug(f"\nStatus Code: {response.status_code}")
        logger.debug("Response Body:")
        try:
            # The spec indicates application/json content
            projects_list = response.json()
            logger.info(json.dumps(projects_list, indent=2))

        except json.JSONDecodeError:
            logger.error("Response was not valid JSON.")
            logger.error(response.text)

except httpx.HTTPStatusError as e:
    logger.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
except httpx.RequestError as e:
    logger.debug(f"An error occurred while requesting {e.request.url!r}: {e}")
except Exception as e:
    logger.debug(f"An unexpected error occurred: {e}")