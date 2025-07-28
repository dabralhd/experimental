from functools import wraps
import connexion
from flask import Response
from project_api.utils.orgs_api_wrapper import(is_user_org_member)
from project_api.utils.error_types import (client_side_error, ErrorType)
import logging
from http import HTTPStatus
from project_api.utils.error_helper import (user_prj_exists, get_prj_path, get_prj_json_path)
import os
from project_api.utils.project_model_helper import (get_model_owner_uuid)

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def with_effective_user_id(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        as_org = connexion.request.args.get('as_org')
        effective_user_id = user
        if as_org:
            status, rights = is_user_org_member(user, as_org)
            if status:
                logger.debug(f'{user} is a member of {as_org}')                
                effective_user_id = as_org
            else:
                logger.error(f'user {user} is not a member of org {as_org}')
                return Response(status=client_side_error(ErrorType.FORBIDDEN))
        # Pass effective_user_id to the view functiond
        return func(user=effective_user_id, *args, **kwargs)
    return wrapper

def with_org_admin_access(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        as_org = connexion.request.args.get('as_org')
        effective_user_id = user
        if as_org:
            status, rights = is_user_org_member(user, as_org)
            if status and rights=='Admin':
                logger.debug(f'{user} is an admin of {as_org}')
                effective_user_id = as_org
            else:
                logger.error(f'user {user} is not an admin of org {as_org}')
                return Response(status=client_side_error(ErrorType.FORBIDDEN))
        # Pass effective_user_id to the view functiond
        return func(user=effective_user_id, *args, **kwargs)
    return wrapper

def with_model_owner_uuid(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        as_org = connexion.request.args.get('as_org')
        effective_user_id = user
        if as_org:
            status, rights = is_user_org_member(user, as_org)
            model_owner_uuid = get_model_owner_uuid(user, kwargs.get('project_name'), kwargs.get('model_name'))
            if status and user == model_owner_uuid:
                logger.debug(f'{user} is a member of {as_org} and is the model owner')                
                effective_user_id = as_org
            elif status and user != model_owner_uuid:
                logger.debug(f'{user} is a member of {as_org}\n is not owner of the model, model_owner_uuid: {model_owner_uuid}')  
                return Response(status=client_side_error(ErrorType.FORBIDDEN))
            else:
                logger.error(f'user {user} is not a member of org {as_org}')
                return Response(status=client_side_error(ErrorType.FORBIDDEN))
        # Pass effective_user_id to the view functiond
        return func(user=effective_user_id, *args, **kwargs)
    return wrapper

def not_supported_for_org(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        as_org = connexion.request.args.get('as_org')
        effective_user_id = user
        if as_org:
            logging.error(f'this operation is not implemented for project sharing usecase.\n i.e. as_org query param not suported! \n as_org: {as_org}')
            return Response(status=HTTPStatus.NOT_IMPLEMENTED)     
        return func(user=effective_user_id, *args, **kwargs)   
    
    return wrapper

def default_except(func):
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