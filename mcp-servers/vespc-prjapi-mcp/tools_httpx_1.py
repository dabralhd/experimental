import httpx
import json
import prjapi_endpoints
import logging
from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP('prjapi-mcp-server')

BEARER_TOKEN = "eyJraWQiOiJcL3JIS3FCbG5JVldiU2RqdEJqODRQaDNyUk5SWWh4cnR6RFwvOXFTK0Q3aWc9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzMzRjNjVhNS0xNDk1LTQ1M2EtYTZkZS00ZDM4NGE3ODEwMDAiLCJjb2duaXRvOmdyb3VwcyI6WyJ3aGl0ZWxpc3QiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfOXdlbnNFNVJaIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiNHNoYjE3OGdsbWxsc3I3NWdmb2JoZmRzYmEiLCJvcmlnaW5fanRpIjoiZDk4OTE1MzgtMjcyYy00NWM2LWFmNzQtZjJhN2UyNjI4ZjcyIiwiZXZlbnRfaWQiOiI1NWNmY2UxNi03ZWMzLTQzZWEtYTMyMi03ODQ3Nzg3YTgwMzEiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIGh0dHBzOlwvXC9vYXV0aDIuZGV2LnN0bS12ZXNwdWNjaS5jb21cL3Rlc3QgcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3NTMyMDU4MDIsImV4cCI6MTc1MzI5MjIwMiwiaWF0IjoxNzUzMjA1ODAyLCJqdGkiOiI4NmMzMzA5ZS02NDhjLTQ5ZDAtOTIyMS0wYjJjODcwOWU5Y2UiLCJ1c2VybmFtZSI6IjMzNGM2NWE1LTE0OTUtNDUzYS1hNmRlLTRkMzg0YTc4MTAwMCJ9.kC0g3NSSUdMxRyjW6Bav-c-aibndM7T_3ayqxUd-KFA5hkFZHbwr7aCcTgYNdKz7Gt5EL0GWPr2Pq3Vn2HstJ6O_mglyquNWP-z_RjM9v59sKsDY-VtrnhcsZ7h3o_VQB9EvFdwq0f5AEYQJnrqHhQWicsjbn400EOVEraYti7oeX-oiyD8_FpPFbbqSBGBgHD9Du3SDBLQDyDylykGCo0mofr9G6iRq-uIkdElUwabTweX-sbDg_1fR6ejYkmJsHVH-KwpKxdS6rkoWss8cl8T1sWk5bcw2QGpn53_L2QAXrBRjI_J1zBNMAZirDeVm952zc0ZURB-qljm0-tkxXg"


def setup_logger(name="tools-httpx", level=logging.ERROR):
    """
    Set up and return a logger with the specified name and level.
    Ensures that logs are output to the console.

    Args:
        name (str): Name of the logger to create or retrieve.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: Configured logger instance with a StreamHandler.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.debug("Entered setup_logger()")
    logger.debug("Exiting setup_logger()")
    return logger

logger = setup_logger(name='logger_mcp_server', level=logging.ERROR)

def get_headers(token):
    """
    Construct the HTTP headers for API requests.

    Args:
        token (str): Bearer token for Authorization.

    Returns:
        dict: Dictionary containing Authorization and Accept headers.
    """
    logger.debug("Entered get_headers()")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    logger.debug(f"Exiting get_headers() with headers: {headers}")
    return headers

def make_http_request(url, headers, http_method: str = 'get', params=None, logger=None):
    """
    Make an HTTP request (GET or POST) to the specified URL with given headers and parameters.
    Logs request and response details if a logger is provided.

    Args:
        url (str): The full URL to send the HTTP request to.
        headers (dict): HTTP headers to include in the request.
        http_method (str): HTTP method to use ('get' or 'post'). Defaults to 'get'.
        params (dict, optional): Query parameters for the request. Defaults to None.
        logger (logging.Logger, optional): Logger for logging details. Defaults to None.

    Returns:
        dict or None: Parsed JSON response if successful, None otherwise.
    """
    if logger:
        logger.debug("Entered make_http_request()")
    try:
        with httpx.Client() as client:
            if logger:
                logger.debug(f"Preparing to make {http_method.upper()} request.")
                logger.info(f"Making HTTP/REST request to: {url}")
                logger.debug(f"Headers: {headers}")
                logger.debug(f"Params: {params}")
            if http_method.lower() == 'get':
                response = client.get(url, headers=headers, params=params)
                if logger:
                    logger.debug("GET request sent.")
            elif http_method.lower() == 'post':
                response = client.post(url, headers=headers, params=params)
                if logger:
                    logger.debug("POST request sent.")
            else:
                if logger:
                    logger.error(f"Unsupported HTTP method: {http_method}")
                raise ValueError(f"Unsupported HTTP method: {http_method}")
            response.raise_for_status()
            if logger:
                logger.debug(f"Status Code: {response.status_code}")
                logger.debug(f"Response Headers: {response.headers}")
                logger.debug("Response Body:")
            try:
                data = response.json()
                if logger:
                    logger.debug("Response successfully parsed as JSON.")
                    logger.info(json.dumps(data, indent=2))
                if logger:
                    logger.debug("Exiting make_http_request() with successful response.")
                return data
            except json.JSONDecodeError:
                if logger:
                    logger.error("Response was not valid JSON.")
                    logger.error(response.text)
                    logger.debug("Exiting make_http_request() due to JSON decode error.")
                return None
    except httpx.HTTPStatusError as e:
        if logger:
            logger.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            logger.debug("Exiting make_http_request() due to HTTPStatusError.")
    except httpx.RequestError as e:
        if logger:
            logger.debug(f"An error occurred while requesting {e.request.url!r}: {e}")
            logger.debug("Exiting make_http_request() due to RequestError.")
    except Exception as e:
        if logger:
            logger.debug(f"An unexpected error occurred: {e}")
            logger.debug("Exiting make_http_request() due to Exception.")
    if logger:
        logger.debug("Exiting make_http_request() with None.")
    return None

def get_projects(api_endpoint: str, headers: dict, params: dict = None, org_id: str=None):
    """
    Build the full request URL, optionally add organization ID to parameters,
    and make an HTTP GET request to the specified API endpoint.

    Args:
        api_endpoint (str): The API endpoint path (e.g., "/projects").
        headers (dict): HTTP headers for the request.
        params (dict, optional): Query parameters for the request. Defaults to None.
        org_id (str, optional): Organization ID to add as 'as_org' query parameter. Defaults to None.

    Returns:
        None
    """
    logger.debug("Entered get_projects()")
    BASE_URL = "https://dev.stm-vespucci.com:443/svc/project-api/3"

    request_url = f"{BASE_URL}{api_endpoint}"
    if params is None:
        params = {}
    if org_id:
        params["as_org"] = org_id

    response = make_http_request(request_url, headers, http_method='get', params=params, logger=logger)
    logger.debug(f'Response from {request_url}:\n{json.dumps(response, indent=2) if response else "No response or error occurred."}')
    logger.debug("Exiting get_projects()")
    return response

def delete_project(api_endpoint: str, headers: dict, params: dict = None, org_id: str=None):
    """
    delete a user project having given name for the user in STAIoT Craft online tool.

    Args:
        api_endpoint (str): The API endpoint path (e.g., "/projects").
        headers (dict): HTTP headers for the request.
        params (dict, optional): Query parameters for the request. Defaults to None.
        org_id (str, optional): Organization ID to add as 'as_org' query parameter. Defaults to None.

    Returns:
        None
    """
    logger.debug("Entered get_projects()")
    BASE_URL = "https://dev.stm-vespucci.com:443/svc/project-api/3"

    request_url = f"{BASE_URL}{api_endpoint}"
    if params is None:
        params = {}
    if org_id:
        params["as_org"] = org_id

    response = make_http_request(request_url, headers, http_method='get', params=params, logger=logger)
    logger.debug(f'Response from {request_url}:\n{json.dumps(response, indent=2) if response else "No response or error occurred."}')
    logger.debug("Exiting get_projects()")
    return response

@mcp_server.tool()
def fetch_usr_prjs():
    '''Fetch user projects from STAIoT Craft project API.'''

    logger.debug('Entered fetch_usr_prjs')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = get_projects(prjapi_endpoints.ENDPOINT_PROJECTS, headers=get_headers(BEARER_TOKEN))
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        return usr_prjs
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_usr_prjs')

@mcp_server.tool()
def fetch_usr_prj_list():
    '''Fetch list of projects for given user from STAIoT Craft project API.'''

    logger.debug('Entered fetch_usr_prj_list')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = get_projects(prjapi_endpoints.ENDPOINT_PROJECTS, headers=get_headers(BEARER_TOKEN))
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        key = 'ai_project_name'
        return [usr_prjs[i][key] for i in range(len(usr_prjs)) if key in usr_prjs[i]]
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_usr_prj_list')  


@mcp_server.tool()
def fetch_usr_prj_using_name(ai_project_name: str):
    '''Fetch details of given project for a given user from STAIoT Craft project API.
    
    Args: 'ai_project_name' - name of the project to fetch.'
    '''

    logger.debug('Entered fetch_usr_prj_list')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = get_projects(prjapi_endpoints.ENDPOINT_PROJECTS, headers=get_headers(BEARER_TOKEN))
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        for prj in usr_prjs:
            if prj['ai_project_name'] == ai_project_name:
                logger.debug(f"Found project with name: {ai_project_name}")
                return prj
        logger.warning(f"Project with name '{ai_project_name}' not found in the user's projects.")
        return None
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_usr_prj_list')     

@mcp_server.tool()
def delete_usr_prj_using_name(ai_project_name: str):
    '''Fetch details of given project for a given user from STAIoT Craft project API.
    
    Args: 'ai_project_name' - name of the project to fetch.'
    '''

    logger.debug('Entered fetch_usr_prj_list')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = get_projects(prjapi_endpoints.ENDPOINT_PROJECTS + '/' + ai_project_name, headers=get_headers(BEARER_TOKEN))
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        for prj in usr_prjs:
            if prj['ai_project_name'] == ai_project_name:
                logger.debug(f"Found project with name: {ai_project_name}")
                return prj
        logger.warning(f"Project with name '{ai_project_name}' not found in the user's projects.")
        return None
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_usr_prj_list')            

@mcp_server.tool()
def fetch_usr_prj_attr(attr: str='ai_project_name'):
    '''Fetch specific attributes for all projects for given user from STAIoT Craft project API.
    
    Args: 'ai_project_name', 'ai_project_id', 'description', 'models', 'deployments'.
    '''

    logger.debug('Entered fetch_usr_prj_list')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = get_projects(prjapi_endpoints.ENDPOINT_PROJECTS, headers=get_headers(BEARER_TOKEN))
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        return [usr_prjs[i][attr] for i in range(len(usr_prjs)) if attr in usr_prjs[i]]
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_usr_prj_list')     

@mcp_server.tool()
def fetch_example_prjs():
    '''Fetch example projects from STAIoT Craft project API.'''

    logger.debug('Entered fetch_example_prjs')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = get_projects(prjapi_endpoints.ENDPOINT_TEMPLATES_PROJECTS, headers=get_headers(BEARER_TOKEN))
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        return usr_prjs
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_example_prjs') 
    
     

if __name__ == "__main__":
    # Initialize and run the server
    mcp_server.run(transport='stdio')    

# if __name__ == "__main__":
#     #test_get_usr_prjs()
#     test_get_example_prjs()
#     logger.info("Script executed directly, running test_get_usr_projects()")    