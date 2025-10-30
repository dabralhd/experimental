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
YOUR_BEARER_TOKEN = ""

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