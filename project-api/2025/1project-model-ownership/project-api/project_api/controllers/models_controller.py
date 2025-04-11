import os

import connexion
from flask import Response

from project_api.globals import GlobalObjects
from project_api.models.new_model import NewModel  # noqa: E501
from project_api.services.project_models import create_model_fs_copy
from project_api.vespucciprjmng.domain.dataset import Dataset
from project_api.vespucciprjmng.domain.model import (
    ModelMetadata,
    ModelTarget,
    ModelType,
)
from project_api.vespucciprjmng.repository.filesystem.project_file_repo import (
    ProjectFileRepo,
)
from project_api.utils.resource_allocation import (
    is_efs_size_ok
)
from project_api.globals import VESPUCCI_ENVIRONMENT
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


def app_create_model(user, body, project_name):  # noqa: E501
    """Create new model

     # noqa: E501

    :param body: The model to be added.
    :type body: dict | bytes
    :param project_name: Project &#x60;name&#x60; identifier
    :type project_name: str

    :rtype: None
    """
    if connexion.request.is_json:
        new_model = NewModel.from_dict(connexion.request.get_json())  # noqa: E501
        
        if  new_model.model_name_to_clone != None:
            # Clone model
            model_name_to_clone = new_model.model_name_to_clone
            new_model_name = new_model.name
            
            user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
            user_project_models_path_folder = os.path.join(user_workspace_path, project_name, "models")

            # Copy/create a new model entry in project-json with new model name
            project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)            
            project_repo = ProjectFileRepo(user_workspace_path)

            try:
                project_repo.clone_model(project_name=project_name, clone_model_uuid_or_name=model_name_to_clone, model_uuid_or_name=new_model_name, model_owner_uuid=user)
            except Exception as e:
                print(e)
                return Response(status=409)

            # Copy file-system contents
            create_model_fs_copy(model_name_to_copy=model_name_to_clone, new_model_name=new_model_name, dest_folder=user_project_models_path_folder)

            return Response(status=201)
        else:

            project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=user)

            project_repo.create_model(
                project_name=project_name,
                model_name=new_model.name,
                dataset_ref=Dataset(new_model.dataset.name, new_model.dataset.dataset_id),
                model_metadata=ModelMetadata(new_model.classes, ModelType(new_model.model_type)),
                model_target=ModelTarget(new_model.target.type, new_model.target.component, new_model.target.device),
                model_owner_uuid=user
            )

            user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=user)
            user_project_models_path_folder = os.path.join(user_workspace_path, project_name, "models")
            user_project_model_path_folder = os.path.join(user_project_models_path_folder, new_model.name)
            user_project_training_path_folder = os.path.join(user_project_model_path_folder, "training")
            
            os.makedirs(user_project_models_path_folder, exist_ok=True)
            os.makedirs(user_project_model_path_folder, exist_ok=True)
            os.makedirs(user_project_training_path_folder, exist_ok=True)

            project_repo.update(project_name=project_name)

            return Response(status=201)

    return Response(status=400)