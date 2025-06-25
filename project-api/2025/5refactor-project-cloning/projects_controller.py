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
)
from project_api.services.templates_repo import (copy_get_started_project, copy_prj, copy_project_for_user)
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
from project_api.utils.error_helper import (
    model_exists, 
    example_prj_exists,
    user_prj_exists,
    is_valid_name,
    is_valid_new_prj_for_user,
    )
import logging
from project_api.utils.orgs_api_wrapper import(is_user_org_member)

from project_api.globals import (
    GET_STARTED_PROJECTS_PATH,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def app_create_project(user: str, body=None, is_user_project=False):  # noqa: E501
    """Create new user project

    Create a new project in the user space  # noqa: E501

    :param body: New project model
    :type body: dict | bytes

    :rtype: None
    """

    if not is_efs_size_ok(user):
        logger.debug('EFS size limit has been breached for this user.')
        if VESPUCCI_ENVIRONMENT != "dev":
            logger.error('Refusing this request')
            return response_error(msg="Storage limit exceeded", status_code=507) # 507 == Insufficient Storage

    if connexion.request.is_json:
        new_project = NewProject.from_dict(connexion.request.get_json())  # noqa: E501

        effective_user_id = user        
        as_org = connexion.request.args.get('as_org')                   
        if as_org: 
            logger.debug(f'attempting POST using as_org credentials.\n as_org: {as_org}')
            if is_user_org_member(user, as_org):
                effective_user_id = as_org
                logger.debug(f'switched effective_user_id to the organization: {as_org}')
            else:
                logger.error(f'user {user} is not a member of org {as_org}')
                return Response(status=client_side_error(ErrorType.FORBIDDEN))

        dest_workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=effective_user_id)
        logger.debug(f'post using effective_user_id: {effective_user_id}\ndest_workspace: {dest_workspace}')

        # TODO: error check for template project
        logger.debug(f'Verifying if src and target project names are valid for user.\n {effective_user_id}, project name: {new_project.ai_project_name}')
        if user_prj_exists(user, new_project.project_name_to_clone) and is_valid_new_prj_for_user(user, new_project.ai_project_name): 
            pass
        else:   
            logger.error(f'Invalid project name for user: {user}, project name: {new_project.ai_project_name}')
            return Response(status=client_side_error(ErrorType.CONFLICT))                

        if  new_project.project_name_to_clone is None:    
            logger.debug(f'creating new project.\neffective_user_id: {effective_user_id}\ntarget-prj-name: {new_project.ai_project_name}')
            project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=effective_user_id)
            
            project_repo.create_project(name=new_project.ai_project_name, type=new_project.type, description=new_project.description, version=new_project.version)
            
            user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=effective_user_id)
            user_project_models_path_folder = os.path.join(user_workspace_path, new_project.ai_project_name, "models")
            os.makedirs(user_project_models_path_folder, exist_ok=True)

            # Create project icon
            icon_path = os.path.join(user_workspace_path, new_project.ai_project_name, "icons")
            generate_icon(new_project.ai_project_name, out_dir=icon_path)
                
            return Response(status=201)
        elif is_user_project:                  
            logger.debug(f'cloning user project.')   
            src_workspace = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=effective_user_id)    
        else: 
            logger.debug(f'cloning get-started project.')   
            src_workspace = GET_STARTED_PROJECTS_PATH

        if not os.path.exists(os.path.join(src_workspace, new_project.project_name_to_clone)):
            return Response(status=client_side_error(ErrorType.NOT_FOUND))
        if os.path.exists(os.path.join(dest_workspace, new_project.ai_project_name)):
            return Response(status=client_side_error(ErrorType.CONFLICT))

        logger.info(f"src-prjname {new_project.project_name_to_clone} dest-prjname {new_project.ai_project_name}")
        [project_folder, project_file_path, error_code] = copy_prj(new_project.project_name_to_clone, new_project.ai_project_name, src_workspace, dest_workspace)
        if error_code != 200:
            return Response(status=400)

        logger.info(f"Project folder: {project_folder}, Project file path: {project_file_path}")
        if is_user_project:
            generate_project_uuid_custom_project(project_file_path)
        else:
            generate_project_uuid(project_file_path)
        substitute_artifacts_project_name(project_folder, project_file_path, new_project.ai_project_name)

        return Response(status=201)

    return Response(status=400)


def app_get_projects(user: str):  # noqa: E501
    """Projects list

    Return project list from user workspace  # noqa: E501


    :rtype: List[Project]
    """   
    as_org = connexion.request.args.get('as_org')              
    if as_org:
        if not is_user_org_member(user, as_org):
            logger.error(f'user {user} is not a member of org {as_org}')
            return Response(status=client_side_error(ErrorType.FORBIDDEN))
        logger.debug(f'Getting projects for org: {as_org}')
        user = as_org
    logger.debug(f'Getting projects for user/group: {user}')
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
