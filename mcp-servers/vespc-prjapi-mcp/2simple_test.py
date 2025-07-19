import httpx
import json

# --- Configuration ---
# Replace with the actual base URL of your API
# For example, if your API is running locally on port 8080:
BASE_URL = "https://dev.stm-vespucci.com:443/svc/project-api/3" # According to servers: - url: /3 in your spec

# Your Bearer Token (JWT)
# Replace with your actual JWT token. You would typically obtain this after
# a successful login or authentication process.
YOUR_BEARER_TOKEN = "eyJraWQiOiJcL3JIS3FCbG5JVldiU2RqdEJqODRQaDNyUk5SWWh4cnR6RFwvOXFTK0Q3aWc9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzMzRjNjVhNS0xNDk1LTQ1M2EtYTZkZS00ZDM4NGE3ODEwMDAiLCJjb2duaXRvOmdyb3VwcyI6WyJ3aGl0ZWxpc3QiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfOXdlbnNFNVJaIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiNHNoYjE3OGdsbWxsc3I3NWdmb2JoZmRzYmEiLCJvcmlnaW5fanRpIjoiODUyNDcyYWQtNjU2ZS00NjViLWEzY2MtMzY1MGE0MGFjN2I1IiwiZXZlbnRfaWQiOiIzZjNjNWEwZi05MGYxLTRiNzUtODliNS04ZmI0OTgwYjY0MDIiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIGh0dHBzOlwvXC9vYXV0aDIuZGV2LnN0bS12ZXNwdWNjaS5jb21cL3Rlc3QgcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3NTA2MDY5NTEsImV4cCI6MTc1MzAwNDMzMSwiaWF0IjoxNzUyOTE3OTMxLCJqdGkiOiIzNzE3NThiYy0zNDc1LTQ5YTYtYjRlNS05MzcxNDI5MWViMmUiLCJ1c2VybmFtZSI6IjMzNGM2NWE1LTE0OTUtNDUzYS1hNmRlLTRkMzg0YTc4MTAwMCJ9.A8Z8HyNRZBYhhO7AsZKJEF0I00z9ykBSPNft9RxHtmvpjmCQHwXaSsy8QvzYac9PwciEEo5bAN6VKDdZIu0VipopTG1-026CNVDADU_LUM8Iclza-lXDuSzl9tJ5FOsCxmP4Lfez3D8j8iBFBbFu5gVJWxZC4SBswqNzMVhtfY8BI3oZ2sag-FAANwRRTI2yLnRoscBt7qkNftDk2Du-TdsCDnSOvI17ZoYcV-7awLx0yeLWJiUZEGC7PwCdfi0-I5KVwjDuSkQlLuWEKhNnohbaoG_VSXPSEwhgEkk5AJOayIGWgBEF0UOji58Jl9aU63BHNmmdfnZsu1wTHpIPQg"

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
        print(f"Making GET request to: {request_url}")
        print(f"Headers: {headers}")
        if params:
            print(f"Params: {params}")

        response = client.get(request_url, headers=headers, params=params)

        # --- Handle the Response ---
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        print(f"\nStatus Code: {response.status_code}")
        print("Response Body:")
        try:
            # The spec indicates application/json content
            projects_list = response.json()
            print(json.dumps(projects_list, indent=2))
        except json.JSONDecodeError:
            print("Response was not valid JSON.")
            print(response.text)

except httpx.HTTPStatusError as e:
    print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
except httpx.RequestError as e:
    print(f"An error occurred while requesting {e.request.url!r}: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")