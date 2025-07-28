from project_api.vespucciprjmng.repository.filesystem.project_file_repo import (
    ProjectFileRepo,
)
import logging
from project_api.utils.vespucci_to_controller_model_converters import (
    convert_project,
)
from project_api.globals import GlobalObjects

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def get_project_owner_uuid(user, project_name):
    """
    Get the owner UUID of the project.
    
    :param user: The user ID.
    :param project_name: The name of the project.
    :return: The owner UUID of the project.
    """
    logger.debug(f'Getting project owner UUID for user: {user}, project: {project_name}')
    project_repo = ProjectFileRepo(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user))
    project_domain_obj = project_repo.get_project(project_name=project_name)
    
    if not project_domain_obj:
        logger.error(f'Project {project_name} does not exist for user {user}')
        return None
    
    project_api_obj = convert_project(project_domain_obj)
    logger.info(f'project_api_obj: {project_api_obj}')
    
    return project_api_obj.project_owner_uuid

def get_model_owner_uuid(user, project_name, model_name):
    """
    Get the owner UUID of the model within a project.
    
    :param user: The user ID.
    :param project_name: The name of the project.
    :param model_name: The name of the model.
    :return: The owner UUID of the model.
    """
    logger.debug(f'get_model_owner_uuid: user: {user}, project_name: {project_name}, model_name: {model_name}')
    project_repo = ProjectFileRepo(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user))
    project_domain_obj = project_repo.get_project(project_name=project_name)
    
    if not project_domain_obj:
        logger.error(f'Project {project_name} does not exist for user {user}')
        return None

    project_api_obj = convert_project(project_domain_obj)

    for model in project_api_obj.models:
        if model.name == model_name:
            logger.info(f'Model owner UUID: {model.model_owner_uuid}')
            return model.model_owner_uuid
    
    return None