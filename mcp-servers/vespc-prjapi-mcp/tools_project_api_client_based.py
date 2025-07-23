from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import project_api_client
from project_api_client.rest import ApiException
from pprint import pprint
import logging
from project_api_client.models.new_project import NewProject


logger = logging.getLogger("prjapi-tools")
logger.setLevel(logging.DEBUG)

# Initialize FastMCP server
mcp = FastMCP("prjapi-mcp")
remote_dev_url = 'https://dev.stm-vespucci.com:443/svc/project-api/3'

logging.debug(f"Using remote_dev_url: {remote_dev_url}")

# Configure Bearer authorization (JWT): bearerAuth
configuration = project_api_client.Configuration(
    host = remote_dev_url,
    access_token = 'eyJraWQiOiJcL3JIS3FCbG5JVldiU2RqdEJqODRQaDNyUk5SWWh4cnR6RFwvOXFTK0Q3aWc9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzMzRjNjVhNS0xNDk1LTQ1M2EtYTZkZS00ZDM4NGE3ODEwMDAiLCJjb2duaXRvOmdyb3VwcyI6WyJ3aGl0ZWxpc3QiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfOXdlbnNFNVJaIiwidmVyc2lvbiI6MiwiY2xpZW50X2lkIjoiNHNoYjE3OGdsbWxsc3I3NWdmb2JoZmRzYmEiLCJvcmlnaW5fanRpIjoiZDk4OTE1MzgtMjcyYy00NWM2LWFmNzQtZjJhN2UyNjI4ZjcyIiwiZXZlbnRfaWQiOiI1NWNmY2UxNi03ZWMzLTQzZWEtYTMyMi03ODQ3Nzg3YTgwMzEiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIGh0dHBzOlwvXC9vYXV0aDIuZGV2LnN0bS12ZXNwdWNjaS5jb21cL3Rlc3QgcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3NTMyMDU4MDIsImV4cCI6MTc1MzI5MjIwMiwiaWF0IjoxNzUzMjA1ODAyLCJqdGkiOiI4NmMzMzA5ZS02NDhjLTQ5ZDAtOTIyMS0wYjJjODcwOWU5Y2UiLCJ1c2VybmFtZSI6IjMzNGM2NWE1LTE0OTUtNDUzYS1hNmRlLTRkMzg0YTc4MTAwMCJ9.kC0g3NSSUdMxRyjW6Bav-c-aibndM7T_3ayqxUd-KFA5hkFZHbwr7aCcTgYNdKz7Gt5EL0GWPr2Pq3Vn2HstJ6O_mglyquNWP-z_RjM9v59sKsDY-VtrnhcsZ7h3o_VQB9EvFdwq0f5AEYQJnrqHhQWicsjbn400EOVEraYti7oeX-oiyD8_FpPFbbqSBGBgHD9Du3SDBLQDyDylykGCo0mofr9G6iRq-uIkdElUwabTweX-sbDg_1fR6ejYkmJsHVH-KwpKxdS6rkoWss8cl8T1sWk5bcw2QGpn53_L2QAXrBRjI_J1zBNMAZirDeVm952zc0ZURB-qljm0-tkxXg'
)

# Create an instance of the API client
# This is used to make API calls to the project API
api_client = project_api_client.ApiClient(configuration)

# Create an instance of the Projects API
# This is used to interact with project-related endpoints
projects_api_instance = project_api_client.ProjectsApi(api_client)

# Constants
@mcp.tool()
async def create_project(prj_name: str) -> str:
    '''Create a new project with the given name.'''
    logger.debug(f"Creating project: {prj_name}")
    try:
        new_project = NewProject(
            # fill in required fields, e.g.
            ai_project_name=prj_name,
            description="An MCP tools generated project called" + prj_name
        )

        response = projects_api_instance.app_create_project(is_user_project=True, new_project=new_project)

        return f"Project '{prj_name}' created successfully."
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return f"Failed to create project '{prj_name}': {str(e)}" 

@mcp.tool()
async def list_projects():
    '''List all staiot craft projects for given user'''
    logger.debug("Listing projects")

    prjs = []
    try:
        # Create new Activity
        #api_instance.app_create_activity(project_name, model_name, activity_type, new_training, as_org=as_org)
        prjs = projects_api_instance.app_get_projects()
    except ApiException as e:
        logger.error(f"Exception when calling ActivityApi->app_get_projects: %s\n" % e)
    except Exception as e:
        logger.error(f"Exception when calling ActivityApi->app_get_projects: %s\n" % e)
    logger.info(f'prjs')
    return prjs

@mcp.tool()
async def clone_project(project_name: str):
    '''Clone a project with the given name.'''
    logger.debug(f"Cloning project: {project_name}")
    try:
        pass  # Here you would implement the logic to clone a project
        return f"Project '{project_name}' cloned successfully."
    except Exception as e:
        logger.error(f"Error cloning project: {e}")
        return f"Failed to clone project '{project_name}': {str(e)}" 

@mcp.tool()
async def delete_project(project_name: str):
    '''Delete a project with the given name.'''
    logger.debug(f"Deleting project: {project_name}")
    try:
        pass  # Here you would implement the logic to delete a project
        return f"Project '{project_name}' deleted successfully."
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        return f"Failed to delete project '{project_name}': {str(e)}"   

@mcp.tool()
async def describe_project(project_name: str):
    '''Describe a project with the given name.'''
    logger.debug(f"Describing project: {project_name}")
    try:
        pass  # Here you would implement the logic to describe a project
        return f"Project '{project_name}' described successfully."
    except Exception as e:
        logger.error(f"Error describing project: {e}")
        return f"Failed to describe project '{project_name}': {str(e)}"     

@mcp.tool()
async def list_models(project_name: str):
    '''List all models for a given project.'''
    logger.debug(f"Listing models for project: {project_name}")
    try:
        pass  # Here you would implement the logic to list models
        return f"Models for project '{project_name}' listed successfully."
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        return f"Failed to list models for project '{project_name}': {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
 