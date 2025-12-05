import httpx
import json
import prjapi_endpoints
import logging
from mcp.server.fastmcp import FastMCP
import asyncio

mcp_server = FastMCP('prjapi-mcp-server')

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

logger = setup_logger(name='logger_mcp_server', level=logging.DEBUG)
logger.debug("logger test line")

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
                if response.status_code == 200:
                    #logger.debug(f'response: {response.json()}')
                    return response.json()
            elif http_method.lower() == 'post':
                response = await client.post(url, headers=headers, params=params, json=body)
                logger.info("POST request sent.")
                return response.status_code           
            elif http_method.lower() == 'delete':
                response = await client.delete(url, headers=headers, params=params)
                logger.info("DELETE request sent.")  
                return response.status_code           
            else:
                logger.error(f"Unsupported HTTP method: {http_method}")
                raise ValueError(f"Unsupported HTTP method: {http_method}")

            logger.debug(f"Status Code: {response.status_code}")
            logger.debug(f"Response Headers: {response.headers}")
            logger.debug("Response Body:")
    
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

@mcp_server.tool()
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


@mcp_server.tool()
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

@mcp_server.tool()
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


@mcp_server.tool()
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

@mcp_server.tool()
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

@mcp_server.tool()
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

@mcp_server.tool()
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


@mcp_server.tool()
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

@mcp_server.tool()
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

@mcp_server.tool()
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

@mcp_server.tool()
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


if __name__ == "__main__":
    # Initialize and run the server
    mcp_server.run(transport='stdio')    

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