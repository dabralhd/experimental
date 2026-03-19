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
    access_token = ''
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
 