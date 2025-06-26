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
from project_api.utils.error_helper import (model_exists)
from project_api.utils.orgs_api_wrapper import(check_orgs_membership, is_user_org_member)
import logging
from project_api.utils.error_types import (client_side_error, ErrorType)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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

        if os.path.exists(os.path.join(GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=effective_user_id), project_name, "models", new_model.name)):
            logger.error(f'model {new_model.name} already exists in project {project_name}')
            return Response(status=client_side_error(ErrorType.CONFLICT)) # TODO: return a more specific error message

        logger.debug(f'creating new model.\neffective_user_id: {effective_user_id}\nas_org: {as_org}\n new_model.name: {new_model.name}')
        if  new_model.model_name_to_clone != None: # clone model
            model_name_to_clone = new_model.model_name_to_clone
            new_model_name = new_model.name
            logger.debug(f'cloning existing model.\neffective_user_id: {effective_user_id}\nas_org: {as_org}\n model_name_to_clone: {model_name_to_clone}\nnew_model_name: {new_model_name}')
            
            def clone_model(effective_user_id, project_name, model_name_to_clone, new_model_name):
                logger.debug('> clone_model')
                user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=effective_user_id)
                user_project_models_path_folder = os.path.join(user_workspace_path, project_name, "models")
                project_repo_uuid = effective_user_id
                logger.debug(f'user_workspace_path: {user_workspace_path} \nuser_project_models_path_folder: {user_project_models_path_folder}')

                # Copy/create a new model entry in project-json with new model name
                project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=effective_user_id)            
                project_repo = ProjectFileRepo(user_workspace_path)

                try:
                    project_repo.clone_model(project_name=project_name, clone_model_uuid_or_name=model_name_to_clone, model_uuid_or_name=new_model_name, model_owner_uuid=effective_user_id)
                except Exception as e:
                    logger.exception(f'exception occurred: {e}')
                    return Response(status=409)

                # Copy file-system contents
                create_model_fs_copy(model_name_to_copy=model_name_to_clone, new_model_name=new_model_name, dest_folder=user_project_models_path_folder)

                return Response(status=201)                
            
            # Clone model
            if as_org and model_exists(as_org, project_name, model_name_to_clone) and not model_exists(as_org, project_name, new_model_name):
                if is_user_org_member(effective_user_id, as_org):   # verify that uuid is member of the as_org organization using orgs-api, for the time being set to True
                    return clone_model(as_org, project_name, model_name_to_clone, new_model_name)
            elif as_org is None and model_exists(effective_user_id, project_name, model_name_to_clone) and not model_exists(effective_user_id, project_name, new_model_name):   
                    return clone_model(effective_user_id, project_name, model_name_to_clone, new_model_name)
            else:
                return Response(status=409)
        else: # create a new model from scratch
            project_repo = GlobalObjects.getInstance().getFSProjectRepo(user_id=effective_user_id)

            project_repo.create_model(
                project_name=project_name,
                model_name=new_model.name,
                dataset_ref=Dataset(new_model.dataset.name, new_model.dataset.dataset_id),
                model_metadata=ModelMetadata(new_model.classes, ModelType(new_model.model_type)),
                model_target=ModelTarget(new_model.target.type, new_model.target.component, new_model.target.device),
                model_owner_uuid=effective_user_id
            )

            user_workspace_path = GlobalObjects.getInstance().getFSUserWorkspaceFolder(user_id=effective_user_id)
            user_project_models_path_folder = os.path.join(user_workspace_path, project_name, "models")
            user_project_model_path_folder = os.path.join(user_project_models_path_folder, new_model.name)
            user_project_training_path_folder = os.path.join(user_project_model_path_folder, "training")
            
            os.makedirs(user_project_models_path_folder, exist_ok=True)
            os.makedirs(user_project_model_path_folder, exist_ok=True)
            os.makedirs(user_project_training_path_folder, exist_ok=True)

            project_repo.update(project_name=project_name)

            return Response(status=201)

    return Response(status=400)