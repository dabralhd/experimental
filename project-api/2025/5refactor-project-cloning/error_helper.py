import json
import os
import re
from zipfile import ZipFile

import connexion
from flask import Response
from requests import get

from project_api.globals import GlobalObjects
from project_api.models.job import Job
from project_api.models.new_training import NewTraining
from project_api.util import response_error
from project_api.utils.vespucci_to_controller_model_converters import (
    convert_training,
)
from project_api.vespucciprjmng.repository.filesystem.project_file_repo import (
    ProjectFileRepo,
)
import logging
import json
from project_api.utils.zipfolder import zip_directory
import shutil
import tempfile
from project_api.globals import (
    GET_STARTED_PROJECTS_PATH,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

def dir_exists(path):
    """
    Check if a directory exists.
    Args:
        path (str): The path to the directory.
    Returns:
        bool: True if the directory exists, False otherwise.
    """
    return os.path.isdir(path)

def get_prj_path(user, project_name):
    """
    Get the path to the project directory.
    Args:
        user (str): The user ID.
        project_name (str): The name of the project.
    Returns:
        str: The path to the project directory.
    """
    return os.path.join(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user), 
                                    project_name)


def get_prj_json_path(user, project_name):
    """
    Get the path to the project JSON file.
    Args:
        user (str): The user ID.
        project_name (str): The name of the project.
    Returns:
        str: The path to the project JSON file.
    """
    return os.path.join(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user), 
                                    project_name,
                                    f'ai_{project_name}.json')



def model_exists(user, project_name, model_name):
    """
    Checks if a model exists in the user's workspace.
    Args:
        user (str): The user ID.
        project_name (str): The name of the project.
        model_name (str): The name of the model.
    Returns:
        bool: True if the model exists, False otherwise.
    """
    logger.debug(f'checking if model {model_name} exists in project {project_name} for user {user}')
    model_dir = os.path.join(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user), 
                                    project_name,
                                    'models',
                                    model_name)
    return os.path.isdir(model_dir)

def example_prj_exists(get_started_project_name):
    """
    Checks if an example project exists in the workspace.
    Args:
        project_name (str): The name of the project.
    Returns:
        bool: True if the example project exists, False otherwise.
    """
    example_project_dir = os.path.join(os.path.join(GET_STARTED_PROJECTS_PATH, get_started_project_name))
    return os.path.isdir(example_project_dir)

def user_prj_exists(user: str, prj_name: str):
    """
    Check if a project directory exists for a given user.
    Args:
        user (str): The user identifier.
        prj_name (str): The name of the project.
    Returns:
        bool: True if the project directory exists, False otherwise.
    """
    
    if os.path.isdir(get_prj_path(user, prj_name)) and os.path.isfile(get_prj_json_path(user, prj_name)):    
        logger.error(f'project {prj_name} exists for user {user}')
        return True

    return False

def is_valid_name(name: str):
    """
    Check if a given name is valid.

    This function checks if the provided name contains only alphanumeric characters,
    underscores, or hyphens. It returns True if the name is valid, and False otherwise.

    Args:
        name (str): The name to be checked.

    Returns:
        bool: True if the name is valid, False otherwise.
    """
    flag = bool(re.match(r'^[\w-]+$', name))
    if not flag:
        logger.error(f'Invalid name: {name}')
    return flag

def is_valid_new_prj_for_user(user: str, prj_name: str):
    """
    Check if a new project being created is valid project name for a given user.

    This function checks if the project name is valid and if the project exists
    in the user's workspace. It returns True if the project is valid, and False otherwise.

    Args:
        user (str): The user identifier.
        prj_name (str): The name of the project being created.

    Returns:
        bool: True if the project is valid for the user, False otherwise.
    """
    return is_valid_name(prj_name) and not user_prj_exists(user, prj_name)