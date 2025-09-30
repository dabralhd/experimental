from tracemalloc import start
from project_api.vespucciprjmng.domain.project import Project as VespucciProject
from project_api.vespucciprjmng.domain.model import Model as VespucciModel
from project_api.vespucciprjmng.domain.training import Training as VespucciTraining
from project_api.vespucciprjmng.domain.job import Job as VespucciJob
from project_api.vespucciprjmng.domain.deployment import Deployment as VespucciDeployment
from project_api.vespucciprjmng.domain.deployment import Application as VespucciDeploymentApplication

from project_api.models.project import Project as APIProject
from project_api.models.model import Model as APIModel
from project_api.models.model import Dataset as APIDataset
from project_api.models.training import Training as APITraining
from project_api.models.runtime import Runtime as APIRuntime
from project_api.models.model_target import ModelTarget as APIModelTarget
from project_api.models.job import Job as APIJob
from project_api.models.model_model_metadata import ModelModelMetadata as APIModelMetadata
from project_api.models.deployment import Deployment as APIDeployment
from project_api.models.deployment_application import DeploymentApplication as APIDeploymentApplication
from project_api.models.deployment_cloud_params import DeploymentCloudParams
from project_api.models.device import Device as APIDevice
from project_api.models.device_models import DeviceModels
from project_api.models.device_application import DeviceApplication
from typing import List

def convert_project(project: VespucciProject) -> APIProject:
    api_project = APIProject(
        uuid=project.uuid,
        ai_project_name=project.name,
        ai_project_type=project.type,
        display_name=project.display_name,
        version=project.version,
        description=project.description,
        models=[],
        applications=[],
        deployments=[],
        creation_time=project.creation_time,
        last_update_time=project.last_update_time,
        project_owner_uuid=project.project_owner_uuid
    )
    
    # Set project_owner_uuid after creation to handle None values
    if project.project_owner_uuid:
        api_project.project_owner_uuid = project.project_owner_uuid

    for model in project.models:
        api_project.models.append(convert_model(model=model))

    for application in project.applications:
        api_project.applications.append(convert_application(application=application))

    for deployment in project.deployments:
        api_project.deployments.append(convert_deployment(deploy=deployment))
        
    return api_project



def convert_application(application=VespucciDeploymentApplication):
    deployment_application=APIDeploymentApplication(
                            uuid=application.uuid,
                            type=application.type,
                            device_template_id=application.device_template_id,
                            device_template_uri=application.device_template_uri,
                            device_manifest_uri=application.device_manifest_uri,
                            image_uri=application.image_uri,
                            module_id=application.module_id,
                            binary_uri=application.binary_uri,
                            binary_id=application.binary_id,
                            protocol=application.protocol,
                            bluestv3_payload = application.bluestv3_payload
                            ) if application else None
    
    return deployment_application

def convert_deployment (deploy : VespucciDeployment):

    gateways : List[APIDevice] = []

    for gw in deploy.gateway_devices:
        gwNew = APIDevice(
            device_id=gw.device_id,
            description=gw.description,
            display_name=gw.display_name,
            gateway_id=gw.gateway_id,
            wifi_mode=gw.wifi_mode,
            application=gw.application
        )
        gateways.append(gwNew)

    leaves : List[APIDevice] = []

    for lf in deploy.leaf_devices:

        infModels : List[DeviceModels] = []
        for model in lf.inference_app["models"]:
            infModel = DeviceModels(
                model_name_reference=model["model_name_reference"], 
                artifact_type=model["artifact_type"], 
                component_name=model["component_name"]
            )
            infModels.append(infModel)

        lfNew = APIDevice(
            device_id=lf.device_id,
            description=lf.description,
            display_name=lf.display_name,
            gateway_id=lf.gateway_id,
            inference=DeviceApplication(application=lf.inference_app["application"], firmware_update=lf.inference_app["firmware_update"], models=infModels),
            datalogging=DeviceApplication(application=lf.datalogging_app["application"], firmware_update=lf.datalogging_app["firmware_update"], models=None)
        )
        leaves.append(lfNew)

    api_deploy = APIDeployment (
        uuid=deploy.uuid,
        display_name=deploy.display_name,
        description=deploy.description,
        last_update_time=deploy.last_update_time,
        last_deploy_result=deploy.last_deploy_result,

        cloud_params= DeploymentCloudParams(
        app_url=deploy.cloud_app_url,
        type=deploy.cloud_type
        ),        
        leaf=leaves,
        gateway=gateways
    )
    
    return api_deploy

def convert_model(model: VespucciModel) -> APIModel:

    api_model = APIModel(
        uuid=model.uuid,
        name=model.name,
        dataset=APIDataset(model.dataset.name, 
                           model.dataset.dataset_id),
        model_metadata=APIModelMetadata(classes=model.model_metadata.classes, 
                                        type=model.model_metadata.type.value),
        model_target=APIModelTarget(model.target.type, 
                                    model.target.component, 
                                    model.target.device),
        model_training=convert_training(model.training),
        data_sufficiency=convert_training(model.data_sufficiency),
        creation_time=model.creation_time,
        last_update_time=model.last_update_time,
        model_owner_uuid=model.model_owner_uuid
    )

    return api_model

def convert_training(training: VespucciTraining) -> APITraining:
    
    model_training=APITraining(runtime=APIRuntime(training.runtime.type, 
                                                  training.runtime.jobs),
                                configuration=training.configuration, 
                                artifacts=training.artifacts,
                                reports=training.reports,
                                creation_time=training.creation_time,
                                last_update_time=training.last_update_time
                                ) if training else None
    
    return model_training

def convert_job(job: VespucciJob) -> APIJob:
    api_job = APIJob(   
    )
    return api_job

