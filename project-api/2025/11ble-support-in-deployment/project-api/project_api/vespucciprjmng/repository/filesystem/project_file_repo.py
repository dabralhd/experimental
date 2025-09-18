

import logging
from typing import List, Any
from datetime import date, datetime  # noqa: F401

from project_api.vespucciprjmng.dao.filesystem.file_dao_factory import (
    FileDAOFactory,
)
from project_api.vespucciprjmng.domain.dataset import Dataset
from project_api.vespucciprjmng.domain.deployment import Deployment, Device, Application, InfModel
from project_api.vespucciprjmng.domain.input import InputType
from project_api.vespucciprjmng.domain.model import (
    Model,
    ModelMetadata,
    ModelTarget,
)
from project_api.vespucciprjmng.domain.output import OutputType
from project_api.vespucciprjmng.domain.project import Project
from project_api.vespucciprjmng.domain.training import Job, Runtime, Training
from project_api.vespucciprjmng.repository.exceptions.resource_already_exist import (
    ResourceAlreadyExisting,
    ResourceKind,
)
from project_api.vespucciprjmng.repository.project_repo import ProjectRepo
import os

logger = logging.getLogger(__name__)

class ProjectFileRepo(ProjectRepo):

    def __init__(self, projects_folder_path: str):
        self.dao_factory = FileDAOFactory(projects_folder_uri=projects_folder_path)

    def get_projects(self) -> List[Project]:
        return self.dao_factory.get_project_dao_instance().get_all()
    
    def get_project(self, project_name: str) -> Project:        
        project: Project    = self.dao_factory.get_project_dao_instance().get(name=project_name)

        # TODO: Support Project Schema and Check supported project schemas by the main-api?
        
        models: List[Model] = self.dao_factory.get_model_dao_instance().get_all(project_name=project_name)
        deploys: List[Deployment] = self.dao_factory.get_deployment_dao_instance().get_all(project_name=project_name)
        applications: List[Application] = self.dao_factory.get_deployment_app_dao_instance().get_all(project_name=project_name)
        
        for model in models:
            training = self.dao_factory.get_training_dao_instance().get(project_name=project.name, model_uuid_or_name=model.uuid)
            model.training = training
            data_sufficiency = self.dao_factory.get_data_sufficiency_dao_instance().get(project_name=project.name, model_uuid_or_name=model.uuid)
            model.data_sufficiency = data_sufficiency
            
        project.models  = models
        project.applications = applications
        project.deployments = deploys

        return project

    def create_project(self, name: str, type: str="", description: str = "", version: str = "0.0.1", uuid = None,project_owner_uuid: str = None) -> Project:
        existing_projects = self.dao_factory.get_project_dao_instance().get_all()
        for existing_project in existing_projects:
            if existing_project.name == name:
                raise ResourceAlreadyExisting(existing_project.uuid, existing_project.name, ResourceKind.PROJECT)

        new_project = Project(uuid=uuid, name=name, type=type, description=description, version=version, project_owner_uuid=project_owner_uuid)
        self.dao_factory.get_project_dao_instance().save(new_project)
        return self.dao_factory.get_project_dao_instance().get(name=name)

    def create_model(self, project_name:str, model_name: str, dataset_ref: Dataset, model_metadata: ModelMetadata, model_target: ModelTarget, input_type: InputType = None, output_type: OutputType = None, model_uuid: str = None, model_owner_uuid: str = None) -> Model:
        existing_models = self.dao_factory.get_model_dao_instance().get_all(project_name=project_name)
        for existing_model in existing_models:
            if existing_model.name == model_name:
                raise ResourceAlreadyExisting(existing_model.uuid, existing_model.name, ResourceKind.MODEL)

        new_model = Model(
            uuid=model_uuid,
            name=model_name,
            dataset=dataset_ref,
            model_metadata=model_metadata,
            model_target=model_target,
            creation_time=str(datetime.now()),
            last_update_time=str(datetime.now()),
            model_owner_uuid=model_owner_uuid
        )        
        self.dao_factory.get_model_dao_instance().save(project_name=project_name, model=new_model)
        
        return self.dao_factory.get_model_dao_instance().get(project_name=project_name, model_uuid_or_name=model_name)

    def clone_model(self, project_name: str, clone_model_uuid_or_name: str, model_uuid_or_name: str, model_owner_uuid: str) -> Model:
        existing_models = self.dao_factory.get_model_dao_instance().get_all(project_name=project_name)
        for existing_model in existing_models:
            if existing_model.name == model_uuid_or_name:
                raise ResourceAlreadyExisting(existing_model.uuid, existing_model.name, ResourceKind.MODEL)
            
        self.dao_factory.get_model_dao_instance().clone(project_name=project_name, clone_model_uuid_or_name=clone_model_uuid_or_name, model_uuid_or_name=model_uuid_or_name, model_owner_uuid=model_owner_uuid)
        self.dao_factory.get_training_dao_instance().clone(project_name=project_name, clone_model_uuid_or_name=clone_model_uuid_or_name, model_uuid_or_name=model_uuid_or_name)
        return self.dao_factory.get_model_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)
    
    def patch_model(self, project_name: str, model_uuid_or_name: str, dataset_ref: Dataset, model_metadata: ModelMetadata) -> Model:
        
        updated_model = Model(
            dataset=dataset_ref,
            model_metadata=model_metadata
        )

        self.dao_factory.get_model_dao_instance().patch(project_name=project_name, model_uuid_or_name=model_uuid_or_name, model=updated_model)
        return self.dao_factory.get_model_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)
    
    def create_training(self, project_name: str, model_uuid_or_name: str, type: str, configuration: str=None, reports: List=None, artifacts: List=None) -> Training:
        runtime = Runtime(type=type, jobs=[])
        new_training = Training(runtime=runtime, configuration=configuration, reports=reports, artifacts=artifacts, creation_time=datetime.now(), last_update_time=datetime.now())
        self.dao_factory.get_training_dao_instance().save(project_name=project_name, model_uuid_or_name=model_uuid_or_name, training=new_training)
        return self.dao_factory.get_training_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)
    
    def get_training(self, project_name: str, model_uuid_or_name: str) -> Training:
        return self.dao_factory.get_training_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)

    def get_datasuff(self, project_name: str, model_uuid_or_name: str) -> Training:
        return self.dao_factory.get_data_sufficiency_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)

    def patch_training(self, project_name: str, model_uuid_or_name: str, type: str, configuration: str=None, reports: List=None, artifacts: List=None) -> Training:
        runtime = Runtime(type=type, jobs=[])
        updated_training = Training(runtime=runtime, configuration=configuration, reports=reports, artifacts=artifacts)
        self.dao_factory.get_training_dao_instance().patch(project_name=project_name, model_uuid_or_name=model_uuid_or_name, training=updated_training)
        return self.dao_factory.get_training_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)
    
    def create_job(self, project_name: str, model_uuid_or_name: str, name: str, version: str, template_id: str) -> Training:
        job = Job(name=name, version=version, template_id=template_id)
        self.dao_factory.get_job_dao_instance().save(project_name=project_name, 
                                                     model_uuid_or_name=model_uuid_or_name, 
                                                     job=job)
        return self.dao_factory.get_training_dao_instance().get(project_name=project_name, 
                                                           model_uuid_or_name=model_uuid_or_name)
    
    def create_deployment(self, project_name: str, deployment_name: str, description: str=None, cloud_type: str=None, cloud_app_url: str=None,
                          leaf_devices: dict=None, gw_devices: dict=None, applications: Any=None):
        existing_deployments = self.dao_factory.get_deployment_dao_instance().get_all(project_name=project_name)
        for existing_deployment in existing_deployments:
            if existing_deployment.display_name == deployment_name:
                raise ResourceAlreadyExisting(existing_deployment.uuid, existing_deployment.display_name, ResourceKind.DEPLOYMENT)
        
        _leaf_devices = []
        _gw_devices = []

        for leaf in leaf_devices:
            _inf_models = []
            for model in leaf.inference.models:
                model = InfModel(artifact_type=model.artifact_type, component_name=model.component_name,model_name_reference=model.model_name_reference)
                _inf_models.append(model)

            _leaf = Device(gateway_id=leaf.gateway_id, device_id=leaf.device_id, 
                          display_name=leaf.display_name, description=leaf.description, 
                          application=leaf.application, inference_app=leaf.inference.application,
                          inference_fwupdate=leaf.inference.firmware_update, datalogging_app=leaf.datalogging.application, 
                          datalogging_fwupdate=leaf.datalogging.firmware_update, inference_models=_inf_models
                          )
            _leaf_devices.append(_leaf)

        for gw in gw_devices:
            _gw = Device(device_id=gw.device_id, display_name=gw.display_name, 
                         description=gw.description, application=gw.application, 
                         wifi_mode=gw.wifi_mode
                          )
            _gw_devices.append(_gw)

        new_deployment = Deployment(uuid=None,
                                    display_name=deployment_name,
                                    description=description,
                                    cloud_type=cloud_type,
                                    cloud_app_url=cloud_app_url,
                                    leaf_devices=_leaf_devices,
                                    gateway_devices=_gw_devices
        )

        for app in applications:
            _app = Application(uuid=app.uuid, type=app.type, module_id=app.module_id,
                              device_template_uri=app.device_template_uri, 
                              device_template_id=app.device_template_id, 
                              device_manifest_uri=app.device_manifest_uri,
                              binary_id=app.binary_id, binary_uri=app.binary_uri,
                              protocol=app.protocol, image_uri=app.image_uri)
            self.dao_factory.get_deployment_app_dao_instance().save(project_name=project_name, application=_app)

        self.dao_factory.get_deployment_dao_instance().save(project_name=project_name, deployment=new_deployment)
        return self.dao_factory.get_deployment_dao_instance().get(project_name=project_name, deployment_uuid_or_name=deployment_name)
    
    def update(self, project_name: str):
        print(f'setting last update time: obtained project {project_name}')
        project = self.dao_factory.get_project_dao_instance().get(name=project_name)
        print(f'project: {project}')
        print(f'project_name: {project_name}')

        project.last_update_time = str(datetime.now())
        self.dao_factory.get_project_dao_instance().save(project)
    
    def get_project_owner_uuid(self, project_name: str):
        obj = self.dao_factory.get_project_dao_instance().get(name=project_name)
        logger.debug(f'project_owner_uuid: {obj["project_owner_uuid"]}')
        return obj["project_owner_uuid"]
    
    def get_model_owner_uuid(self, project_name: str, model_name: str):
        obj = self.dao_factory.get_model_dao_instance().save(project_name=project_name, model=model_name)
        logger.debug(f'model_owner_uuid: {obj["model_owner_uuid"]}')
        return obj["model_owner_uuid"]    
