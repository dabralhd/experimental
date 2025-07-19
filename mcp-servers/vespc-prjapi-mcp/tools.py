from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging

logger = logging.getLogger("prjapi-tools").setLevel(logging.INFO)

# Initialize FastMCP server
mcp = FastMCP("prjapi-mcp")

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

 