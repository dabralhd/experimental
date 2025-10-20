import os
import requests
import logging

from flask import send_from_directory

from project_api.globals import GET_STARTED_PROJECTS_PATH
from project_api.services.templates_repo import get_started_projects
from project_api.util import response_error
from project_api.utils.error_helper import (get_prj_api_log_level)
import json

logger = logging.getLogger(__name__)
logger.setLevel(get_prj_api_log_level())

def app_get_templates_projects():  # noqa: E501
    """Project templates list
    
    Return the list of available get started project templates
    
    :rtype: List[Project]
    """
    logger.debug(f'get_started_projects')
    api_projects = get_started_projects()
    logger.debug(f'api_projects: {json.dumps(api_projects, indent=4, sort_keys=True)}')
    
    return api_projects

def app_get_template_project_icon(project_name: str):
    """Project template icon

    Return the project image/icon of the  get started project template
    
    :rtype: img/png
    """
    logger.debug(f'get_started_projects')
    
    icon_path = os.path.join(GET_STARTED_PROJECTS_PATH, 
                                project_name,
                                "icons")
    logger.debug(f'icon_path: {icon_path}')
    
    jpg_file  = os.path.join(icon_path, "icon.jpg")
    jpeg_file = os.path.join(icon_path, "icon.jpeg")
    png_file  = os.path.join(icon_path, "icon.png")

    if os.path.exists(png_file):
            return send_from_directory(icon_path, "icon.png", as_attachment=True)
    elif os.path.exists(jpg_file):
            return send_from_directory(icon_path, "icon.jpg", as_attachment=True)
    elif os.path.exists(jpeg_file):
            return send_from_directory(icon_path, "icon.jpeg", as_attachment=True)
    
    return response_error("Icon file not found in project", status_code=404)
