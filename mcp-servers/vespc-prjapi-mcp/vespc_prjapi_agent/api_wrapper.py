import httpx
import json
from fastmcp.prompts import Message
import asyncio
from pydantic import BaseModel
import logging

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
