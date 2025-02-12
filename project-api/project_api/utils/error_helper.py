import json
import os
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

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
    model_dir = os.path.join(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user), 
                                    project_name,
                                    'models',
                                    model_name)
    return os.path.isdir(model_dir)