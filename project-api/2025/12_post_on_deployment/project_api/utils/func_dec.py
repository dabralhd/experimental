from functools import wraps
import connexion
from flask import Response
from project_api.utils.orgs_api_wrapper import(is_user_org_member)
from project_api.utils.error_types import (client_side_error, ErrorType)
import logging
from http import HTTPStatus
from project_api.utils.error_helper import (user_prj_exists, get_prj_path, get_prj_json_path)
import os
from project_api.utils.project_model_helper import (get_project_owner_uuid, get_model_owner_uuid)

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def ws_userid(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        as_org = connexion.request.args.get('as_org')
        ws_userid = user
        if as_org:
            status, _ = is_user_org_member(user, as_org)
            if status:
                logger.debug(f'{user} is a member of {as_org}')                
                ws_userid = as_org
            else:
                logger.error(f'user {user} is not a member of org {as_org}')
                return Response(status=client_side_error(ErrorType.FORBIDDEN))
        # Pass ws_userid to the view functiond
        return func(ws_userid, *args, **kwargs)
    return wrapper

def with_org_admin_access(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        as_org = connexion.request.args.get('as_org')
        ws_userid = user
        if as_org:
            status, rights = is_user_org_member(user, as_org)
            if status and rights=='Admin':
                logger.debug(f'{user} is an admin of {as_org}')
                ws_userid = as_org
            else:
                logger.error(f'user {user} is not an admin of org {as_org}')
                return Response(status=client_side_error(ErrorType.FORBIDDEN))
        # Pass ws_userid to the view functiond
        return func(ws_userid, *args, **kwargs)
    return wrapper

def with_model_owner_uuid(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        ws_userid = user    
        as_org = connexion.request.args.get('as_org')
        logger.debug(f'user: {user}\nas_org: {as_org}')
        if as_org and ws_userid != as_org:
            status, _ = is_user_org_member(user, as_org)
            if status:
                ws_userid = as_org
                model_owner_uuid = get_model_owner_uuid(ws_userid, kwargs.get('project_name'), kwargs.get('model_name'))
                logger.debug(f'model_owner_uuid: {model_owner_uuid}')
                if user != model_owner_uuid:
                    logger.debug(f'{user} is a member of {as_org}\n user is not owner of the model, \nmodel_owner_uuid: {model_owner_uuid}')  
                    return Response(status=client_side_error(ErrorType.FORBIDDEN))
            else:
                logger.error(f'user {user} is not a member of org {as_org}')
                return Response(status=client_side_error(ErrorType.FORBIDDEN))
        # Pass ws_userid to the view functiond
        logger.debug(f'{user} is a member of {as_org} and is the model owner')
        return func(ws_userid, *args, **kwargs)
    return wrapper

def check_admin_or_proj_owner(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        ws_userid = user    
        as_org = connexion.request.args.get('as_org')
        if as_org: 
            if ws_userid != as_org:
                ws_userid = as_org               
                project_owner_uuid = get_project_owner_uuid(ws_userid, kwargs.get('project_name'))              
                status, rights = is_user_org_member(user, as_org)
                
                if status: 
                    logger.debug(f'{user} is a member of {as_org}')                
                    if rights=='Admin': 
                        logger.debug(f'user has org admin rights')  
                        return func(ws_userid, *args, **kwargs)                   
                    elif user == project_owner_uuid:
                        logger.debug(f'user is project owner: {project_owner_uuid}')  
                        return func(ws_userid, *args, **kwargs)
                    else:
                        logger.debug(f'user: {user} is neither project-owner nor admin')
                        pass
        else:
            logger.debug(f'Not a project-sharing scenario\nuser: {ws_userid}, org= {as_org}')
            return func(ws_userid, *args, **kwargs)                    
                
        logger.error(f'user {user} is not a member of org {as_org} ')
        return Response(status=client_side_error(ErrorType.FORBIDDEN))

    return wrapper

def not_supported_for_org(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        as_org = connexion.request.args.get('as_org')
        if as_org:
            logging.error(f'this operation is not implemented for project sharing usecase.\n i.e. as_org query param not suported! \n as_org: {as_org}')
            return Response(status=HTTPStatus.NOT_IMPLEMENTED)     
        return func(user, *args, **kwargs)   
    
    return wrapper

def default_except(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        try:
            return func(user, *args, **kwargs)  
        except Exception as e:
            logger.error(f'exception occurred {e}')
            return Response('bad request', status=400)              
    
    return wrapper

def default_public_projects_except(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)  
        except Exception as e:
            logger.error(f'exception occurred {e}')
            return Response('bad request', status=400)              
    
    return wrapper

def verify_project_exists(func):
    @wraps(func)
    def wrapper(user: str, project_name: str, *args, **kwargs):
        logger.debug(f'verifying if project {project_name} exists for user {user}')
        if not os.path.isdir(get_prj_path(user, project_name)) or not os.path.isfile(get_prj_json_path(user, project_name)):    
            logging.error(f'project {project_name} doe not exists for user {user}')
            return Response(status=HTTPStatus.NOT_FOUND)     
        return func(user, project_name, *args, **kwargs)   
    
    return wrapper    