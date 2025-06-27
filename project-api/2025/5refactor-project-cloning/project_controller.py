import os
import traceback
import logging
from flask import Response, send_from_directory

from project_api.globals import GlobalObjects
from project_api.models.project import Project  # noqa: E501
from project_api.utils.vespucci_to_controller_model_converters import (
    convert_project,
)
from project_api.util import response_error
import connexion
from project_api.utils.orgs_api_wrapper import(check_orgs_membership, is_user_org_member)

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

from project_api.utils.error_helper import (user_prj_exists)

from project_api.utils.error_types import (client_side_error, ErrorType)

def app_get_project_icon(user: str, project_name: str):  # noqa: E501
    """Project template icon

    Return the project image/icon of the project
    
    :rtype: image/*
    """
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

    if not user_prj_exists(effective_user_id, project_name):    
        logger.error(f'project does not exists - {project_name} for user {effective_user_id}')
        return Response(status=client_side_error(ErrorType.NOT_FOUND))

    project_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=effective_user_id)
    icon_path = os.path.join(project_path, project_name, "icons")
    jpg_file  = os.path.join(icon_path, "icon.jpg")
    jpeg_file = os.path.join(icon_path, "icon.jpeg")
    png_file  = os.path.join(icon_path, "icon.png")

    logger.debug(f'Checking if project exists for user: {effective_user_id}, project name: {project_name}')
    if not user_prj_exists(effective_user_id, project_name):    
        logger.error(f'project not found - {project_name}')
        return Response(status=client_side_error(ErrorType.NOT_FOUND))
    logger.debug('Project exists, proceeding further')    

    if os.path.exists(png_file):
            return send_from_directory(icon_path, "icon.png", as_attachment=True)
    elif os.path.exists(jpg_file):
            return send_from_directory(icon_path, "icon.jpg", as_attachment=True)
    elif os.path.exists(jpeg_file):
            return send_from_directory(icon_path, "icon.jpeg", as_attachment=True)
    
    return response_error("Icon file not found in project", status_code=404)

def app_delete_project(user, project_name):  # noqa: E501
    """Delete project associated to the given name.

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str

    :rtype: None
    """
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

    if not user_prj_exists(effective_user_id, project_name):    
        logger.error(f'project does not exists - {project_name} for user {effective_user_id}')
        return Response(status=client_side_error(ErrorType.NOT_FOUND))

    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=effective_user_id)
    logger.debug(f'Checking if project exists for user: {effective_user_id}, project name: {project_name}')
    if not user_prj_exists(effective_user_id, project_name):    
        logger.error(f'project not found - {project_name}')
        return Response(status=client_side_error(ErrorType.NOT_FOUND))
    logger.debug('Project exists, proceeding further')  

    project: Project = None
    try:
        project = project_repo.get_project(project_name=project_name)
    except Exception:
        print(traceback.format_exc())
        return Response(status=404)

    project_repo.dao_factory.get_project_dao_instance().delete(name=project_name)

    try:
        GlobalObjects.getInstance().getDBProjectRepo(user_id=effective_user_id).dao_factory.get_project_dao_instance().delete(uuid=project.uuid)
    except Exception as e:
        print(e)
        print("Probably DB is not properly filled")

    return Response(status=200)

def app_get_project(user: str, project_name: str):  # noqa: E501
    """Get project model

    Return selected project model from user workspace  # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str

    :rtype: Project
    """
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

    if not user_prj_exists(effective_user_id, project_name):    
        logger.error(f'project does not exists - {project_name} for user {effective_user_id}')
        return Response(status=client_side_error(ErrorType.NOT_FOUND))

    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=effective_user_id)
    logger.debug(f'Checking if project exists for user: {effective_user_id}, project name: {project_name}')
    if not user_prj_exists(effective_user_id, project_name):    
        logger.error(f'project not found - {project_name}')
        return Response(status=client_side_error(ErrorType.NOT_FOUND))
    logger.debug('Project exists, proceeding further')      

    project_domain_obj = None
    try:
        project_domain_obj = project_repo.get_project(project_name=project_name)
    except Exception:
        print(traceback.format_exc())
        return response_error("Project not found or internal server error", status_code=404)

    project_api_obj = convert_project(project_domain_obj)
    return project_api_obj
