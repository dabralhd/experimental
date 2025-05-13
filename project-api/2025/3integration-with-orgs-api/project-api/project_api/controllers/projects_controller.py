import os
import traceback

import connexion
from flask import Response

from project_api.globals import GlobalObjects
from project_api.models.new_project import NewProject  # noqa: E501
from project_api.services.db import synch_project_into_db
from project_api.services.project_models import (
    generate_project_uuid,
    generate_project_uuid_custom_project,
    substitute_artifacts_project_name,
    user_project_exists,
)
from project_api.services.templates_repo import extract_get_started_project, extract_user_project
from project_api.util import _check_reserved_char, response_error
from project_api.utils.vespucci_to_controller_model_converters import (
    convert_project,
)
from project_api.utils.resource_allocation import (
    is_efs_size_ok
)
from project_api.utils.generate_icon import (
    generate_icon
)
from project_api.globals import VESPUCCI_ENVIRONMENT
from project_api.utils.error_types import (client_side_error, ErrorType)
from project_api.utils.error_helper import (model_exists, example_project_exists)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

def app_create_project(user: str, body=None, is_user_project=False):  # noqa: E501
    """Create new user project

    Create a new project in the user space  # noqa: E501

    :param body: New project model
    :type body: dict | bytes

    :rtype: None
    """

    if is_efs_size_ok(user) == False:
        logger.error('EFS size limit has been breached for this user.')
        if VESPUCCI_ENVIRONMENT != "dev":
            logger.error('Refusing this request')
            return response_error(msg="Storage limit exceeded", status_code=507) # 507 == Insufficient Storage

    if connexion.request.is_json:
        new_project = NewProject.from_dict(connexion.request.get_json())  # noqa: E501
        new_project_name = new_project.ai_project_name
        dest_folder = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
        
        logger.debug(f'Checking if project exists for user: {user}, project name: {new_project_name}')
        if user_project_exists(user, new_project_name):    # check if dest folder already exist
            logger.error(f'destination project already exists - {new_project_name}')
            return Response(status=client_side_error(ErrorType.CONFLICT))
        logger.debug('Project does not exist, proceeding with creation')

        if  new_project.project_name_to_clone != None:            
            logger.info(f"Cloning project {new_project.project_name_to_clone} to {new_project.ai_project_name}")
            project_name_to_clone = new_project.project_name_to_clone
      
            if(_check_reserved_char(new_project_name)):
                return Response(status=400)
            
            #if new_project.project_name_to_clone.startswith('get_started'):
            if  is_user_project==False: 
                logger.debug(f'cloning get_started project, check if source project exists')
                if not example_project_exists(new_project.project_name_to_clone):    
                    logger.error(f'project does not exists - {new_project.project_name_to_clone}')
                    return Response(status=client_side_error(ErrorType.NOT_FOUND))

                [project_folder, project_file_path, error_code] = extract_get_started_project(project_name_to_clone, new_project_name, dest_folder)
                if error_code != 200:
                    return Response(status=400)

                generate_project_uuid(project_file_path)
                substitute_artifacts_project_name(project_folder, project_file_path, new_project_name)
                project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)      
            else:
                logger.debug(f'cloning a user project')
                to_org = connexion.request.args.get('to_org')                   
                
                if to_org:
                    logger.debug(f'to_org: {to_org}')
                    pass
                else:
                    logger.info(f"Cloning project {project_name_to_clone} to {new_project_name}")
                    [project_folder, project_file_path, error_code] = extract_user_project(project_name_to_clone, new_project_name, dest_folder)
                    if error_code != 200:
                        return Response(status=400)

                    logger.info(f"Project folder: {project_folder}, Project file path: {project_file_path}")
                    generate_project_uuid_custom_project(project_file_path)
                    substitute_artifacts_project_name(project_folder, project_file_path, new_project_name)

                    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)      
            return Response(status=201)
            
        else:
            # Create project from scratch
            project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)

            if(_check_reserved_char(new_project.ai_project_name)):
                return Response(status=400)
            
            project_repo.create_project(name=new_project.ai_project_name, type=new_project.type, description=new_project.description, version=new_project.version)
            
            user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
            user_project_models_path_folder = os.path.join(user_workspace_path, new_project.ai_project_name, "models")
            os.makedirs(user_project_models_path_folder, exist_ok=True)

            # Create project icon
            icon_path = os.path.join(user_workspace_path, new_project.ai_project_name, "icons")
            generate_icon(new_project.ai_project_name, out_dir=icon_path)
                
            return Response(status=201)

    return Response(status=400)


def app_get_projects(user: str):  # noqa: E501
    """Projects list

    Return project list from user workspace  # noqa: E501


    :rtype: List[Project]
    """    
    
    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
    project_domain_objs = project_repo.get_projects()
    project_api_objs = []
    for project_domain_obj in project_domain_objs:
        try:
            full_project_domain_obj = project_repo.get_project(project_name=project_domain_obj.name)
            project_api_objs.append(convert_project(full_project_domain_obj))
        except Exception as e:
            logger.error("Invalid project: "+ project_domain_obj.name, exc_info=True)
            traceback.print_exc()

    return project_api_objs
