import os
import shutil
import logging

import connexion
from flask import Response

from project_api.globals import GlobalObjects
from project_api.models.new_model import NewModel
from project_api.vespucciprjmng.domain.dataset import Dataset
from project_api.vespucciprjmng.domain.model import ModelMetadata, ModelType
from project_api.vespucciprjmng.repository.filesystem.project_file_repo import (
    ProjectFileRepo,
)
from project_api.services.project_models import ( user_project_exists )
from project_api.utils.error_types import (client_side_error, ErrorType)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def app_clone_model(user, project_name, model_name):  # noqa: E501):
    """Clone a model associated to the given name.

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str

    :rtype: None
    """
    return Response(status=200)

def app_delete_model(user, project_name, model_name):  # noqa: E501
    """Delete model associated to the given name.

     # noqa: E501

    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str
    :param model_name: Model &#x60;name&#x60; identifier
    :type model_name: str

    :rtype: None
    """
    
    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)
    project_repo.dao_factory.get_model_dao_instance().delete(project_name=project_name, model_uuid_or_name=model_name)

    user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
    user_project_models_path_folder = os.path.join(user_workspace_path, project_name, "models")
    user_project_model_path_folder = os.path.join(user_project_models_path_folder, model_name)
    
    if os.path.exists(user_project_model_path_folder):
        try:
            shutil.rmtree(user_project_model_path_folder)
        except OSError as e:
            logger.error(f"Error deleting model '{model_name}': {e}")
    else:
        logger.error(f"Model Path '{user_project_model_path_folder}' does not exist.")
        return Response(status=client_side_error(ErrorType.NOT_FOUND))

    return Response(status=200)

def app_patch_model(user, project_name, model_name):  # noqa: E501
    project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)

    if connexion.request.is_json:
        updated_model = NewModel.from_dict(connexion.request.get_json())  # noqa: E501
        user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
        project_repo = ProjectFileRepo(user_workspace_path)

        project_repo.patch_model(project_name=project_name, model_uuid_or_name=model_name,
                                    dataset_ref=Dataset(updated_model.dataset.name, updated_model.dataset.dataset_id),
                                    model_metadata=ModelMetadata(updated_model.classes, ModelType.CLASSIFIER))

        return Response(status=201)

    return Response(status=200)

