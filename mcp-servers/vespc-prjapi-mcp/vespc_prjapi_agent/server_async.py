import httpx
import json
import prjapi_endpoints
import logging
import time
from functools import wraps
from mcp.server.fastmcp import FastMCP
from fastmcp.prompts import Message
import asyncio

staiotcraft_server = FastMCP('staiotcraft_server')

BEARER_TOKEN = ""
BASE_URL = "https://dev.stm-vespucci.com:443/svc/project-api/3"

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
        formatter = logging.Formatter('%(levelname)s %(name)s %(lineno)d: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logger(name='logger_staiotcraft_server', level=logging.DEBUG)
logger.debug("logger test line")


def time_tool(func):
    """
    Decorator to measure and log execution time for async tool functions.
    Logs timing information in milliseconds to terminal.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        tool_name = func.__name__
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
            logger.info(f"[TOOL_TIMING] {tool_name} - Duration: {duration_ms:.2f} ms - Status: SUCCESS")
            return result
        except Exception as e:
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
            logger.info(f"[TOOL_TIMING] {tool_name} - Duration: {duration_ms:.2f} ms - Status: ERROR - {type(e).__name__}: {str(e)}")
            raise
    return wrapper


def time_prompt(func):
    """
    Decorator to measure and log execution time for sync prompt functions.
    Logs timing information in milliseconds to terminal.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        prompt_name = func.__name__
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
            logger.info(f"[PROMPT_TIMING] {prompt_name} - Duration: {duration_ms:.2f} ms - Status: SUCCESS")
            return result
        except Exception as e:
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
            logger.info(f"[PROMPT_TIMING] {prompt_name} - Duration: {duration_ms:.2f} ms - Status: ERROR - {type(e).__name__}: {str(e)}")
            raise
    return wrapper

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

def get_headers_1(token):
    """
    Construct the HTTP headers for API requests.

    Args:
        token (str): Bearer token for Authorization.

    Returns:
        dict: Dictionary containing Authorization.
    """
    logger.debug("Entered get_headers_1()")
    headers = {
        "Authorization": f"Bearer {token}",
    }
    logger.debug(f"Exiting get_headers_1() with headers: {headers}")
    return headers


async def make_http_request(url, headers, http_method: str = 'get', params=None, body = None):
    """
    Make an HTTP request (GET or POST) to the specified URL with given headers and parameters.
    Logs request and response details if a logger is provided.
    Measures and logs the time taken for each API call in milliseconds.

    Args:
        url (str): The full URL to send the HTTP request to.
        headers (dict): HTTP headers to include in the request.
        http_method (str): HTTP method to use ('get' or 'post'). Defaults to 'get'.
        params (dict, optional): Query parameters for the request. Defaults to None.
        logger (logging.Logger, optional): Logger for logging details. Defaults to None.

    Returns:
        dict or None: Parsed JSON response if successful, None otherwise.
    """
    response = {}
    logger.info("Entered make_http_request()")
    
    # Record start time for API call timing
    start_time = time.perf_counter()
    
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Preparing to make {http_method.upper()} request.")
            logger.info(f"Making HTTP/REST request to: {url}")
            logger.debug(f"Headers: {headers}")
            logger.debug(f"Params: {params}")
            if http_method.lower() == 'get':
                response = await client.get(url, headers=headers, params=params)
                logger.info("GET request sent.")
                # Calculate and log timing
                end_time = time.perf_counter()
                duration_ms = (end_time - start_time) * 1000
                logger.info(f"[TIMING] {http_method.upper()} {url} - Duration: {duration_ms:.2f} ms - Status: {response.status_code}")
                if response.status_code == 200:
                    #logger.debug(f'response: {response.json()}')
                    return response.json()
            elif http_method.lower() == 'post':
                response = await client.post(url, headers=headers, params=params, json=body)
                logger.info("POST request sent.")
                # Calculate and log timing
                end_time = time.perf_counter()
                duration_ms = (end_time - start_time) * 1000
                logger.info(f"[TIMING] {http_method.upper()} {url} - Duration: {duration_ms:.2f} ms - Status: {response.status_code}")
                return response.status_code           
            elif http_method.lower() == 'delete':
                response = await client.delete(url, headers=headers, params=params)
                logger.info("DELETE request sent.")
                # Calculate and log timing
                end_time = time.perf_counter()
                duration_ms = (end_time - start_time) * 1000
                logger.info(f"[TIMING] {http_method.upper()} {url} - Duration: {duration_ms:.2f} ms - Status: {response.status_code}")
                return response.status_code           
            else:
                logger.error(f"Unsupported HTTP method: {http_method}")
                raise ValueError(f"Unsupported HTTP method: {http_method}")

            logger.debug(f"Status Code: {response.status_code}")
            logger.debug(f"Response Headers: {response.headers}")
            logger.debug("Response Body:")
    
    except httpx.HTTPStatusError as e:
        # Calculate and log timing even on error
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000
        logger.info(f"[TIMING] {http_method.upper()} {url} - Duration: {duration_ms:.2f} ms - Status: {e.response.status_code} (ERROR)")
        logger.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        logger.debug("Exiting make_http_request() due to HTTPStatusError.")
    except httpx.RequestError as e:
        # Calculate and log timing even on error
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000
        logger.info(f"[TIMING] {http_method.upper()} {url} - Duration: {duration_ms:.2f} ms - Request Error")
        logger.debug(f"An error occurred while requesting {e.request.url!r}: {e}")
        logger.debug("Exiting make_http_request() due to RequestError.")
    except Exception as e:
        # Calculate and log timing even on error
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000
        logger.info(f"[TIMING] {http_method.upper()} {url} - Duration: {duration_ms:.2f} ms - Exception: {type(e).__name__}")
        logger.debug(f"An unexpected error occurred: {e}")
        logger.debug("Exiting make_http_request() due to Exception.")
        logger.debug("Exiting make_http_request() with None.")
    logger.debug(f'response: {response}')
    return { 'response-status-code': response.status_code }


async def make_http_request_old(url, headers, http_method: str = 'get', params=None, body = None):
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
    response = {}
    logger.info("Entered make_http_request()")
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Preparing to make {http_method.upper()} request.")
            logger.info(f"Making HTTP/REST request to: {url}")
            logger.debug(f"Headers: {headers}")
            logger.debug(f"Params: {params}")
            if http_method.lower() == 'get':
                response = await client.get(url, headers=headers, params=params)
                logger.info("GET request sent.")
            elif http_method.lower() == 'post':
                response = await client.post(url, headers=headers, params=params, json=body)
                logger.info("POST request sent.")
            elif http_method.lower() == 'delete':
                response = await client.delete(url, headers=headers, params=params)
                logger.info("DELETE request sent.")                    
            else:
                logger.error(f"Unsupported HTTP method: {http_method}")
                raise ValueError(f"Unsupported HTTP method: {http_method}")

            logger.debug(f"Status Code: {response.status_code}")
            logger.debug(f"Response Headers: {response.headers}")
            logger.debug("Response Body:")
            
            # try:
            #     data = response.json()
            #     logger.debug("Response successfully parsed as JSON.")
            #     logger.info(json.dumps(data, indent=2))
            #     logger.debug("Exiting make_http_request() with successful response.")
            #     return data
            # except json.JSONDecodeError:
            #     logger.error("Response was not valid JSON.")
            #     logger.error(response.text)
            #     return None
    except httpx.HTTPStatusError as e:
        logger.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        logger.debug("Exiting make_http_request() due to HTTPStatusError.")
    except httpx.RequestError as e:
        logger.debug(f"An error occurred while requesting {e.request.url!r}: {e}")
        logger.debug("Exiting make_http_request() due to RequestError.")
    except Exception as e:
        logger.debug(f"An unexpected error occurred: {e}")
        logger.debug("Exiting make_http_request() due to Exception.")
        logger.debug("Exiting make_http_request() with None.")
    logger.debug(f'response: {response}')
    return { 'response-status-code': response.status_code }

async def invoke_url_with_http_method(request_url: str, headers: dict, params: dict = None, org_id: str=None, http_method: str = 'get', body = None):
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
    logger.debug("Entered invoke_projects_endpoint_with_http_method()")

    if params is None:
        params = {}

    response = await make_http_request(request_url, headers, http_method=http_method, params=params, body=body)
    logger.debug(f'Response from {request_url}:\n{json.dumps(response, indent=2) if response else "No response or error occurred."}')
    logger.debug("Exiting invoke_projects_endpoint_with_http_method()")
    return response

async def get_projects():
    """ Fetch all projects for the user from STAIoT Craft tool workspace. """
    logger.debug("Entered get_projects()")

    request_url = f"{BASE_URL}{prjapi_endpoints.ENDPOINT_PROJECTS}"
    headers=get_headers(BEARER_TOKEN)
    params = {}
    response = await invoke_url_with_http_method(request_url=request_url, 
                                                         headers=headers, 
                                                         http_method='get', 
                                                         params=params)
    logger.debug("Exiting get_projects()")
    return response


async def get_template_projects():
    """ Fetch template projects for STAIoT Craft tool. """
    logger.debug("Entered get_projects()")

    request_url = f"{BASE_URL}{prjapi_endpoints.ENDPOINT_TEMPLATES_PROJECTS}"
    headers=get_headers(BEARER_TOKEN)
    params = {}
    response = await invoke_url_with_http_method(request_url=request_url, 
                                                         headers=headers, 
                                                         http_method='get', 
                                                         params=params)
    logger.debug("Exiting get_projects()")
    return response


async def create_project(ai_project_name: str, description: str, version: str):
    """ Create a project for the user from STAIoT Craft tool workspace. 
    
    Args:
        ai_project_name (str): Name of the AI project to create.
        description (str): Description of the AI project.
        version (str): Version of the AI project.
    """
    logger.debug("Entered create_projects()")

    request_url = f"{BASE_URL}{prjapi_endpoints.ENDPOINT_PROJECTS}" + "?" + "is_user_project=True"
    logger.debug(f"Request URL: {request_url}")
    headers=get_headers(BEARER_TOKEN)
    params = {'is_user_project': 'True'}
    body = {
        'ai_project_name': ai_project_name,
        'description': description,
        'version': version,  
    }
    response = await invoke_url_with_http_method(request_url=request_url, 
                                                         headers=headers, 
                                                         http_method='post', 
                                                         params=params,
                                                         body=body)
    logger.debug("Exiting create_projects()")
    return response

async def clone_project(ai_project_name: str, project_name_to_clone: str, is_user_project: bool = False):
    """ clone a user project. 
    
    Args:
        ai_project_name (str): Name of the AI project to create.
        project_name_to_clone (str): project name to clone.
        version (str): Version of the AI project.
    """
    logger.debug("Entered create_projects()")

    request_url = f"{BASE_URL}{prjapi_endpoints.ENDPOINT_PROJECTS}"
    logger.debug(f"Request URL: {request_url}")
    headers=get_headers(BEARER_TOKEN)
    params = {'is_user_project': 'True' if is_user_project else 'False'}
    body = {
        'ai_project_name': ai_project_name,
        'project_name_to_clone': project_name_to_clone,
    }
    response = await invoke_url_with_http_method(request_url=request_url, 
                                                         headers=headers, 
                                                         http_method='post', 
                                                         params=params,
                                                         body=body)
    logger.debug("Exiting create_projects()")
    return response

async def delete_project(ai_project_name: str):
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
    logger.debug("Entered delete_project()")

    request_url = f"{BASE_URL}{prjapi_endpoints.ENDPOINT_PROJECTS}/{ai_project_name}"
    headers=get_headers(BEARER_TOKEN)
    params = {}    
    logger.debug(f"Request URL: {request_url}")
    if params is None:
        params = {}

    response = await invoke_url_with_http_method(request_url=request_url, 
                                                         headers=headers, 
                                                         http_method='delete', 
                                                         params=params)    
    logger.debug(f"response afte deleting project {ai_project_name}: {response}")
    logger.debug("Exiting delete_project()")
    return response

@staiotcraft_server.tool()
@time_tool
async def fetch_usr_prjs():
    '''Fetch user projects from STAIoT Craft tool's workspace.'''

    logger.debug('Entered fetch_usr_prjs')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = await get_projects()
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        return usr_prjs
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_usr_prjs')


@staiotcraft_server.tool()
@time_tool
async def fetch_template_prjs():
    '''Fetch template projects from STAIoT Craft tool.'''

    logger.debug('Entered fetch_template_prjs')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = await get_template_projects()
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        return usr_prjs
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_template_prjs')

@staiotcraft_server.tool()
@time_tool
async def fetch_usr_prj_list():
    '''Fetch list of projects from STAIoT Craft tool's workspace.'''

    logger.debug('Entered fetch_usr_prj_list')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = await get_projects()
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        key = 'ai_project_name'
        return [usr_prjs[i][key] for i in range(len(usr_prjs)) if key in usr_prjs[i]]
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_usr_prj_list')  


@staiotcraft_server.tool()
@time_tool
async def fetch_usr_prj_using_name(ai_project_name: str):
    '''Fetch details of given project for a given user from STAIoT Craft tool's workspace.
    
    Args: 'ai_project_name' - name of the project to fetch.'
    '''

    logger.debug('Entered fetch_usr_prj_list')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = await get_projects()
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

@staiotcraft_server.tool()
@time_tool
async def delete_usr_prj_using_name(ai_project_name: str):
    '''Delete given project for a given user from STAIoT Craft tool's workspace.
    
    Args: 'ai_project_name' - name of the project to fetch.'
    '''

    logger.debug('Entered fetch_usr_prj_list')
    logger.debug('Calling the /projects endpoint...')
    response = await delete_project(ai_project_name=ai_project_name)
    if response:
        logger.info(f"Deleted user project named {ai_project_name} project successfully.")
    else:
        logger.error("Failed to delete projects or no projects found.")
    logger.debug('Exiting fetch_usr_prj_list')  
    return response          

@staiotcraft_server.tool()
@time_tool
async def fetch_usr_prj_attr(attr: str='ai_project_name'):
    '''Fetch specific attributes for all projects from STAIoT Craft tool's workspace.
    
    Args: 'ai_project_name', 'ai_project_id', 'description', 'models', 'deployments'.
    '''

    logger.debug('Entered fetch_usr_prj_list')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = await get_projects()
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        return [usr_prjs[i][attr] for i in range(len(usr_prjs)) if attr in usr_prjs[i]]
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_usr_prj_list')     

@staiotcraft_server.tool()
@time_tool
async def fetch_template_prj_list():
    '''Fetch list of template projects from STAIoT Craft tool's workspace.'''

    logger.debug('Entered fetch_template_prj_list')
    logger.debug('Calling the /projects endpoint...')
    usr_prjs = await get_template_projects()
    if usr_prjs:
        logger.info(f"Fetched {len(usr_prjs)} projects successfully.")
        key = 'ai_project_name'
        return [usr_prjs[i][key] for i in range(len(usr_prjs)) if key in usr_prjs[i]]
    else:
        logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting fetch_template_prj_list')  


@staiotcraft_server.tool()
@time_tool
async def fetch_template_prj_using_name(ai_project_name: str):
    '''Fetch details of given template project from STAIoT Craft tool's workspace.
    
    Args: 'ai_project_name' - name of the project to fetch.'
    '''

    logger.debug('Entered fetch_template_prj_using_name')
    usr_prjs = await get_template_projects()
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
    logger.debug('Exiting fetch_template_prj_using_name') 

@staiotcraft_server.tool()
@time_tool
async def create_usr_prj(ai_project_name: str, description: str = "project description", version: str = '0.0.1'):
    '''Create a new project user project from scratch in STAIoT Craft tool's workspace.
    
    Args: 'ai_project_name', 'description', 'version'.
    '''

    logger.debug('Entered create_usr_prj')
    response = await create_project(ai_project_name=ai_project_name, description=description, version=version)
    if response:
        logger.info(f"Project '{ai_project_name}' created successfully.")
        return response
    else:
        logger.error(f"Failed to create project '{ai_project_name}'.")
    logger.debug('Exiting create_usr_prj')

@staiotcraft_server.tool()
@time_tool
async def clone_usr_prj(ai_project_name: str, project_name_to_clone: str):
    '''Clone a user project in STAIoT Craft tool's workspace.
    
    Args: 'ai_project_name', 'project_name_to_clone'.
    '''

    logger.debug('Entered create_usr_prj')
    response = await clone_project(ai_project_name=ai_project_name, project_name_to_clone=project_name_to_clone, is_user_project=True)
    if response == 200:
        fstr = f"Project '{ai_project_name}' created successfully."
        logger.info(fstr)
        return fstr
    elif response == 409:
        fstr = f"it seems project '{ai_project_name}' already exists."
        logger.info(fstr)
        return fstr        
    else:
        logger.error(f"Failed to create project '{ai_project_name}'.")
    logger.debug('Exiting create_usr_prj')    

@staiotcraft_server.tool()
@time_tool
async def clone_template_prj(ai_project_name: str, project_name_to_clone: str):
    '''Clone a template or an example project in STAIoT Craft tool's workspace.
    
    Args: 'ai_project_name', 'project_name_to_clone'.
    '''

    logger.debug('Entered clone_template_prj')
    response = await clone_project(ai_project_name=ai_project_name, project_name_to_clone=project_name_to_clone, is_user_project=False)
    if response:
        logger.info(f"Project '{ai_project_name}' created successfully.")
        return response
    else:
        logger.error(f"Failed to create project '{ai_project_name}'.")
    logger.debug('Exiting clone_template_prj')     

async def test_delete_usr_prjs():
    '''Test function to delete user projects.'''
    logger.debug('Entered test_delete_usr_prjs')
    ai_project_name = 'test_project'
    response = await delete_usr_prj_using_name(ai_project_name)
    if response:
        logger.info(f"Project '{ai_project_name}' deleted successfully.")
    else:
        logger.error(f"Failed to delete project '{ai_project_name}'.")
    logger.debug('Exiting test_delete_usr_prjs') 
         
async def test_get_usr_prjs():
    '''Test function to delete user projects.'''
    logger.debug('Entered test_get_usr_prjs')
    response = await get_projects()
    if response:
        json_response = json.dumps(response, indent=2)
        logger.debug(f"Fetched {len(json_response)} projects successfully.")
        logger.debug(f"Projects: {json_response}")
        return json_response
    logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting test_get_usr_prjs')
    return None     

         
async def test_get_template_prjs():
    '''Test function to get template projects.'''
    logger.debug('Entered test_get_usr_prjs')
    response = await get_template_projects()
    if response:
        json_response = json.dumps(response, indent=2)
        logger.debug(f"Fetched {len(json_response)} projects successfully.")
        logger.debug(f"Projects: {json_response}")
        return json_response
    logger.error("Failed to fetch projects or no projects found.")
    logger.debug('Exiting test_get_usr_prjs')
    return None   

async def test_create_usr_prj():
    '''Test function to create a user project.'''
    logger.debug('Entered test_create_usr_prj')
    ai_project_name = 'test_project'
    description = 'This is a test project created via API.'
    version = '1.0'
    response = await create_project(ai_project_name=ai_project_name, description=description, version=version)
    if response:
        logger.info(f"Project '{ai_project_name}' created successfully.")
    else:
        logger.error(f"Failed to create project '{ai_project_name}'.")
    logger.debug('Exiting test_create_usr_prj') 
    return response

async def test_clone_usr_prj():
    '''Test function to create a user project.'''
    logger.debug('Entered test_clone_usr_prj')
    project_name_to_clone = 'test_project'
    ai_project_name = 'cloned_test_project_2'
    logger.debug(f"Cloning project '{project_name_to_clone}' as '{ai_project_name}'")
    response = await clone_project(project_name_to_clone=project_name_to_clone, ai_project_name=ai_project_name, is_user_project=True)
    if response:
        logger.info(f"Project '{project_name_to_clone}' cloned successfully.")
        return response
    else:
        logger.error(f"Failed to create project '{ai_project_name}'.")
    logger.debug('Exiting test_clone_usr_prj') 
    return None

async def test_fetch_usr_prj_list():
    '''Test function to create a user project.'''
    logger.debug('Entered test_clone_usr_prj')
    project_name_to_clone = 'test_project'
    ai_project_name = 'cloned_test_project_2'
    logger.debug(f"Cloning project '{project_name_to_clone}' as '{ai_project_name}'")
    response = await fetch_usr_prj_list()
    if response:
        logger.info(f"Project '{project_name_to_clone}' cloned successfully.")
        return response
    else:
        logger.error(f"Failed to create project '{ai_project_name}'.")
    logger.debug('Exiting test_clone_usr_prj') 
    return None


@staiotcraft_server.prompt()
@time_prompt
def explore_staiotcraft_templates() -> str:
    """
    Prompt template exported by the MCP server to help users explore
    the STAIoT Craft online platform using the `fetch_template_prjs` tool.

    MCP clients can invoke this prompt to get an instruction text that
    tells the model how to use the tool and how to present the results.
    """
    return (
        "You are helping a user explore and understand the capabilities of "
        "the STAIoT Craft online platform.\n\n"
        "You have access to an MCP tool named `fetch_template_prjs` which, "
        "when called with no arguments, returns the list of available "
        "STAIoT Craft template projects as JSON.\n\n"
        "First, call the `fetch_template_prjs` tool (no arguments) to obtain "
        "the latest template projects. Then, based on the tool output:\n"
        "- Identify each template project and briefly describe its purpose and "
        "  likely use cases.\n"
        "- Infer what kinds of applications, workflows, or domains STAIoT "
        "  Craft supports from these templates.\n"
        "- Provide a concise summary of the overall capabilities of STAIoT "
        "  Craft, organized with clear bullet points or short sections.\n\n"
        "Always ground your explanation in the actual data returned by "
        "`fetch_template_prjs`, and explicitly mention any assumptions you "
        "need to make if the data is incomplete or ambiguous."
    )


@staiotcraft_server.prompt()
@time_prompt
def delete_projects_with_confirmation() -> str:
    """
    Prompt template exported by the MCP server to help users safely delete
    projects from their STAIoT Craft workspace, one by one, with explicit
    confirmation before each deletion.
    """
    return (
        "You are assisting a user in managing (and potentially deleting) AI "
        "projects in their STAIoT Craft workspace.\n\n"
        "Available MCP tools that you should use:\n"
        "- `fetch_usr_prj_list`: returns a list of existing user project names.\n"
        "- `delete_usr_prj_using_name(ai_project_name)`: deletes the given "
        "  user project from the workspace.\n\n"
        "Your behavior MUST follow this protocol:\n"
        "1. Start by calling `fetch_usr_prj_list` to show the user the current "
        "   projects in their workspace.\n"
        "2. Ask the user which project they want to delete (by name). Do not "
        "   call the delete tool yet.\n"
        "3. Once the user specifies a project name, clearly restate it and ask "
        "   for an explicit confirmation, e.g. "
        "   \"Please confirm: delete project '<name>' from your STAIoT Craft "
        "   workspace? (yes/no)\".\n"
        "4. ONLY IF the user replies with an unambiguous confirmation (such as "
        "   \"yes\", \"confirm\", or \"delete it\"), call "
        "   `delete_usr_prj_using_name` with that exact project name.\n"
        "5. After the tool responds, inform the user whether the deletion "
        "   succeeded or failed.\n"
        "6. Ask the user if they want to delete another project; if they do, "
        "   repeat steps 1–5 for each project, one at a time.\n\n"
        "Under no circumstances should you delete a project without the user’s "
        "explicit confirmation for that specific project name."
    )


@staiotcraft_server.prompt()
@time_prompt
def clone_example_project_with_filtering(
    application_area: str | None = None,
    project_description: str | None = None,
) -> str:
    """
    Prompt template exported by the MCP server to help users clone an
    example/template project, chosen based on selection criteria such as
    application/target area, description, or both.

    Parameters:
    - application_area: a short phrase describing the desired domain or
      target area (e.g., \"predictive maintenance\", \"energy optimization\").
    - project_description: free-text description of what the user wants
      the example project to cover.
    """
    return (
        "You are helping a user clone an example (template) project in the "
        "STAIoT Craft online platform.\n\n"
        f"User selection criteria provided by the client:\n"
        f"- Application / target area: {application_area or 'not specified'}\n"
        f"- Desired project description: {project_description or 'not specified'}\n\n"
        "Available MCP tools that you should use:\n"
        "- `fetch_template_prjs`: returns detailed information about all "
        "  available template/example projects.\n"
        "- `clone_template_prj(ai_project_name, project_name_to_clone)`: "
        "  creates a new user project by cloning a chosen template.\n\n"
        "Your behavior MUST follow this protocol:\n"
        "1. Use the selection criteria already provided above "
        "   (application area and/or desired description) as the primary "
        "   filter for candidate templates.\n"
        "2. Call `fetch_template_prjs` to retrieve the full list of templates.\n"
        "3. Filter the templates locally according to these criteria "
        "   (by matching target area fields, description text, or both).\n"
        "4. Present the user with a short, ranked list of the best-matching "
        "   templates. For each candidate, show at least:\n"
        "   - the template’s `ai_project_name`,\n"
        "   - its target area (if available),\n"
        "   - a brief summary of its description.\n"
        "5. Ask the user which specific template they want to clone, and what "
        "   name they would like for the new cloned project (`ai_project_name`).\n"
        "6. Once the user has selected a template and provided a new project "
        "   name, restate both and ask for explicit confirmation, e.g. "
        "   \"Please confirm: clone template '<template_name>' as new project "
        "   '<new_project_name>' (yes/no)\".\n"
        "7. ONLY IF the user confirms unambiguously, call "
        "   `clone_template_prj` with:\n"
        "   - `ai_project_name` = the new project name provided by the user,\n"
        "   - `project_name_to_clone` = the chosen template’s `ai_project_name`.\n"
        "8. Report the result of the cloning operation back to the user, "
        "   including any status messages or errors.\n\n"
        "You must never call `clone_template_prj` without a clear user choice "
        "of template and explicit confirmation of the new project name."
    )

if __name__ == "__main__":
    # Initialize and run the server
    staiotcraft_server.run(transport='stdio')    

# async def main():
#     await test_fetch_usr_prj_list()
#     # await test_get_usr_prjs()
#     # await test_get_template_prjs()
#     # await test_delete_usr_prjs()
#     # await test_create_usr_prj()
#     # await test_clone_usr_prj()
    
# if __name__ == "__main__":
#     asyncio.run(main())
#     logger.info("Script executed directly, running test_get_usr_projects()")    

