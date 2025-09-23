

import logging
from project_api.utils.error_helper import (user_prj_exists, get_prj_api_log_level)
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
logger.setLevel(get_prj_api_log_level())

class ProjectFileRepo(ProjectRepo):

    def __init__(self, projects_folder_path: str):
        self.dao_factory = FileDAOFactory(projects_folder_uri=projects_folder_path)

    def get_projects(self) -> List[Project]:
        logger.debug("ProjectFileRepo.get_projects: fetching all projects")
        return self.dao_factory.get_project_dao_instance().get_all()
    
    def get_project(self, project_name: str) -> Project:        
        logger.debug(f"ProjectFileRepo.get_project: project_name={project_name}")
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

        logger.debug(
            f"ProjectFileRepo.get_project: assembled project with models={len(models)}, "
            f"applications={len(applications)}, deployments={len(deploys)}"
        )
        return project

    def create_project(self, name: str, type: str="", description: str = "", version: str = "0.0.1", uuid = None,project_owner_uuid: str = None) -> Project:
        logger.debug(
            f"ProjectFileRepo.create_project: name={name}, type={type}, version={version}, project_owner_uuid={project_owner_uuid}"
        )
        existing_projects = self.dao_factory.get_project_dao_instance().get_all()
        for existing_project in existing_projects:
            if existing_project.name == name:
                raise ResourceAlreadyExisting(existing_project.uuid, existing_project.name, ResourceKind.PROJECT)

        new_project = Project(uuid=uuid, name=name, type=type, description=description, version=version, project_owner_uuid=project_owner_uuid)
        self.dao_factory.get_project_dao_instance().save(new_project)
        logger.debug(f"ProjectFileRepo.create_project: project created name={name}")
        return self.dao_factory.get_project_dao_instance().get(name=name)

    def create_model(self, project_name:str, model_name: str, dataset_ref: Dataset, model_metadata: ModelMetadata, model_target: ModelTarget, input_type: InputType = None, output_type: OutputType = None, model_uuid: str = None, model_owner_uuid: str = None) -> Model:
        logger.debug(
            f"ProjectFileRepo.create_model: project_name={project_name}, model_name={model_name}, model_owner_uuid={model_owner_uuid}"
        )
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
        logger.debug(f"ProjectFileRepo.create_model: model saved model_name={model_name}")
        
        return self.dao_factory.get_model_dao_instance().get(project_name=project_name, model_uuid_or_name=model_name)

    def clone_model(self, project_name: str, clone_model_uuid_or_name: str, model_uuid_or_name: str, model_owner_uuid: str) -> Model:
        logger.debug(
            f"ProjectFileRepo.clone_model: project_name={project_name}, clone_from={clone_model_uuid_or_name}, new_model={model_uuid_or_name}, model_owner_uuid={model_owner_uuid}"
        )
        existing_models = self.dao_factory.get_model_dao_instance().get_all(project_name=project_name)
        for existing_model in existing_models:
            if existing_model.name == model_uuid_or_name:
                raise ResourceAlreadyExisting(existing_model.uuid, existing_model.name, ResourceKind.MODEL)
            
        self.dao_factory.get_model_dao_instance().clone(project_name=project_name, clone_model_uuid_or_name=clone_model_uuid_or_name, model_uuid_or_name=model_uuid_or_name, model_owner_uuid=model_owner_uuid)
        self.dao_factory.get_training_dao_instance().clone(project_name=project_name, clone_model_uuid_or_name=clone_model_uuid_or_name, model_uuid_or_name=model_uuid_or_name)
        logger.debug("ProjectFileRepo.clone_model: clone completed")
        return self.dao_factory.get_model_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)
    
    def patch_model(self, project_name: str, model_uuid_or_name: str, dataset_ref: Dataset, model_metadata: ModelMetadata) -> Model:
        logger.debug(
            f"ProjectFileRepo.patch_model: project_name={project_name}, model_uuid_or_name={model_uuid_or_name}"
        )
        
        updated_model = Model(
            dataset=dataset_ref,
            model_metadata=model_metadata
        )

        self.dao_factory.get_model_dao_instance().patch(project_name=project_name, model_uuid_or_name=model_uuid_or_name, model=updated_model)
        logger.debug("ProjectFileRepo.patch_model: patch applied")
        return self.dao_factory.get_model_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)
    
    def create_training(self, project_name: str, model_uuid_or_name: str, type: str, configuration: str=None, reports: List=None, artifacts: List=None) -> Training:
        logger.debug(
            f"ProjectFileRepo.create_training: project_name={project_name}, model_uuid_or_name={model_uuid_or_name}, type={type}"
        )
        runtime = Runtime(type=type, jobs=[])
        new_training = Training(runtime=runtime, configuration=configuration, reports=reports, artifacts=artifacts, creation_time=datetime.now(), last_update_time=datetime.now())
        self.dao_factory.get_training_dao_instance().save(project_name=project_name, model_uuid_or_name=model_uuid_or_name, training=new_training)
        logger.debug("ProjectFileRepo.create_training: training saved")
        return self.dao_factory.get_training_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)
    
    def get_training(self, project_name: str, model_uuid_or_name: str) -> Training:
        logger.debug(
            f"ProjectFileRepo.get_training: project_name={project_name}, model_uuid_or_name={model_uuid_or_name}"
        )
        return self.dao_factory.get_training_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)

    def get_datasuff(self, project_name: str, model_uuid_or_name: str) -> Training:
        logger.debug(
            f"ProjectFileRepo.get_datasuff: project_name={project_name}, model_uuid_or_name={model_uuid_or_name}"
        )
        return self.dao_factory.get_data_sufficiency_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)

    def patch_training(self, project_name: str, model_uuid_or_name: str, type: str, configuration: str=None, reports: List=None, artifacts: List=None) -> Training:
        logger.debug(
            f"ProjectFileRepo.patch_training: project_name={project_name}, model_uuid_or_name={model_uuid_or_name}, type={type}"
        )
        runtime = Runtime(type=type, jobs=[])
        updated_training = Training(runtime=runtime, configuration=configuration, reports=reports, artifacts=artifacts)
        self.dao_factory.get_training_dao_instance().patch(project_name=project_name, model_uuid_or_name=model_uuid_or_name, training=updated_training)
        logger.debug("ProjectFileRepo.patch_training: training patched")
        return self.dao_factory.get_training_dao_instance().get(project_name=project_name, model_uuid_or_name=model_uuid_or_name)
    
    def create_job(self, project_name: str, model_uuid_or_name: str, name: str, version: str, template_id: str) -> Training:
        logger.debug(
            f"ProjectFileRepo.create_job: project_name={project_name}, model_uuid_or_name={model_uuid_or_name}, name={name}, version={version}, template_id={template_id}"
        )
        job = Job(name=name, version=version, template_id=template_id)
        self.dao_factory.get_job_dao_instance().save(project_name=project_name, 
                                                     model_uuid_or_name=model_uuid_or_name, 
                                                     job=job)
        logger.debug("ProjectFileRepo.create_job: job saved")
        return self.dao_factory.get_training_dao_instance().get(project_name=project_name, 
                                                           model_uuid_or_name=model_uuid_or_name)
    
    def create_deployment(self, project_name: str, deployment_name: str, description: str=None, cloud_type: str=None, cloud_app_url: str=None,
                          leaf_devices: dict=None, gw_devices: dict=None, applications: Any=None):
        logger.debug(
            f"ProjectFileRepo.create_deployment: project_name={project_name}, deployment_name={deployment_name}, cloud_type={cloud_type}"
        )
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
        logger.debug("ProjectFileRepo.create_deployment: deployment saved")
        return self.dao_factory.get_deployment_dao_instance().get(project_name=project_name, deployment_uuid_or_name=deployment_name)
    
    def update(self, project_name: str):
        logger.debug(f"ProjectFileRepo.update: setting last update time, project_name={project_name}")
        project = self.dao_factory.get_project_dao_instance().get(name=project_name)
        logger.debug(f"ProjectFileRepo.update: project fetched: {project}")
        logger.debug(f"ProjectFileRepo.update: project_name: {project_name}")

        project.last_update_time = str(datetime.now())
        self.dao_factory.get_project_dao_instance().save(project)
    
    def get_project_owner_uuid(self, project_name: str):
        logger.debug(f"ProjectFileRepo.get_project_owner_uuid: project_name={project_name}")
        obj = self.dao_factory.get_project_dao_instance().get(name=project_name)
        logger.debug(f'project_owner_uuid: {obj["project_owner_uuid"]}')
        return obj["project_owner_uuid"]
    
    def get_model_owner_uuid(self, project_name: str, model_name: str):
        logger.debug(f"ProjectFileRepo.get_model_owner_uuid: project_name={project_name}, model_name={model_name}")
        obj = self.dao_factory.get_model_dao_instance().save(project_name=project_name, model=model_name)
        logger.debug(f'model_owner_uuid: {obj["model_owner_uuid"]}')
        return obj["model_owner_uuid"]    
