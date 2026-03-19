from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import project_api_client
from project_api_client.rest import ApiException
from pprint import pprint
import logging

logger = logging.getLogger("prjapi-tools")
logger.setLevel(logging.INFO)

# Initialize FastMCP server
mcp = FastMCP("prjapi-mcp")
remote_dev_url = 'https://dev.stm-vespucci.com:443/svc/project-api/3'

# Configure Bearer authorization (JWT): bearerAuth
configuration = project_api_client.Configuration(
    host = remote_dev_url,
    access_token = ''
)

pprint(f'configuration: {configuration}')

# Constants
@mcp.tool()
async def create_project(prj_name: str) -> str:
    '''Create a new project with the given name.'''
    logger.debug(f"Creating project: {prj_name}")
    try:
        pass  # Here you would implement the logic to create a project
        return f"Project '{prj_name}' created successfully."
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return f"Failed to create project '{prj_name}': {str(e)}" 

@mcp.tool()
async def list_projects_1():
    '''List all staiot craft projects for given user'''
    logger.debug("Listing projects")
    remote_dev_url = 'https://dev.stm-vespucci.com:443/svc/project-api/3'

    print(f"Using remote_dev_url: {remote_dev_url}")

    # Configure Bearer authorization (JWT): bearerAuth
    configuration = project_api_client.Configuration(
        host = remote_dev_url,
        access_token = ''
    )

    # Enter a context with an instance of the API client
    with project_api_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        projects_api_instance = project_api_client.ProjectsApi(api_client)

        #api_instance = project_api_client.ActivityApi(api_client)
        # project_name = 'project_name_example' # str | Project `name` identifier
        # model_name = 'model_name_example' # str | Model `name` identifier
        # activity_type = 'activity_type_example' # str | Activity `name` identifier
        # new_training = project_api_client.NewTraining() # NewTraining | The activity to be added.
        # as_org = '8s28038jgmf8cn8a7ka2hzhj10' # str | sometimes a user will share a project with an org  (optional)

        prjs = []
        try:
            # Create new Activity
            #api_instance.app_create_activity(project_name, model_name, activity_type, new_training, as_org=as_org)
            prjs = projects_api_instance.app_get_projects()
        except ApiException as e:
            print("Exception when calling ActivityApi->app_get_projects: %s\n" % e)
        except Exception as e:
            print("Exception when calling ActivityApi->app_get_projects: %s\n" % e)
        pprint(prjs)
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
 