
from typing import List, Any
from uuid import uuid4
import logging

from project_api.vespucciprjmng.dao.filesystem.json_data_connector import JSONDataConnector
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import ProjectFileDAO
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.deployment_dao import DeploymentDAO
from project_api.vespucciprjmng.domain.deployment import Deployment, Device

logger = logging.getLogger(__name__)

class DeploymentFileDAO(DeploymentDAO):
    """Deployment data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)

    def get_all(self, project_name: str) -> List[Deployment]:
        """Get all stored deployments (without details) inside a project"""
        
        self.data_session.connect(get_project_file_name(project_name))

        deployment_domain_objs = []
        for json_deployment_obj in self.data_session.json_file["deployments"]:
            deployment_domain_obj = self.__deserialize_deployment(project_ref=project_name, json_deployment_obj=json_deployment_obj)
            deployment_domain_objs.append(deployment_domain_obj)
        
        self.data_session.dispose()
        
        return deployment_domain_objs

    def get(self, project_name: str, deployment_uuid_or_name: str) -> Deployment:
        """Get deployment (with all details) given a deployment ID"""

        self.data_session.connect(get_project_file_name(project_name))

        deployment_domain_obj = None

        for json_deployment_obj in self.data_session.json_file["deployments"]:
            if json_deployment_obj["uuid"] == deployment_uuid_or_name or json_deployment_obj["display_name"] == deployment_uuid_or_name:
                deployment_domain_obj = self.__deserialize_deployment(project_ref=project_name, json_deployment_obj=json_deployment_obj)
        
        self.data_session.dispose()

        return deployment_domain_obj
    
    def delete(self, project_name: str, deployment_uuid_or_name: str) -> None:
        """Delete deployment from related project"""
        self.data_session.connect(get_project_file_name(project_name))

        filtered_json_deployment_objs = []
        selected_json_deployment_obj = None
        for json_deployment_obj in self.data_session.json_file["deployments"]:
            if json_deployment_obj["uuid"] != deployment_uuid_or_name:
                filtered_json_deployment_objs.append(json_deployment_obj)
            else:
                selected_json_deployment_obj = json_deployment_obj
        self.data_session.json_file["deployments"] = filtered_json_deployment_objs

        # Delete all related applications
        referenced_uuids = set()
        for gateway in selected_json_deployment_obj["gateway"]:
            referenced_uuids.add(gateway["application"])
        for leaf in selected_json_deployment_obj["leaf"]:
            if "datalogging" in leaf:
                referenced_uuids.add(leaf["datalogging"]["application"])
            if "inference" in leaf:
                referenced_uuids.add(leaf["inference"]["application"])

        filtered_json_application_objs = []
        for json_application_obj in self.data_session.json_file["applications"]:
            if json_application_obj["uuid"] not in referenced_uuids:
                filtered_json_application_objs.append(json_application_obj)
        self.data_session.json_file["applications"] = filtered_json_application_objs

        self.data_session.save()
        self.data_session.dispose()

    def save(self, project_name: str, deployment: Deployment) -> None:
        """Save new deployment or update existing deployment"""
    
        self.data_session.connect(get_project_file_name(project_name))

        selected_json_deployment_obj = None
        for json_deployment_obj in self.data_session.json_file["deployments"]:
            if json_deployment_obj["display_name"] == deployment.display_name:
                selected_json_deployment_obj = json_deployment_obj
                break

        patched_json_deployment_obj = self.__serialize_deployment(deployment)

        if selected_json_deployment_obj:
            selected_json_deployment_obj.update(patched_json_deployment_obj)
        else:  
            self.data_session.json_file["deployments"].append(patched_json_deployment_obj)

        self.data_session.save()
        self.data_session.dispose()


    def __deserialize_deployment(self, project_ref, json_deployment_obj) -> Deployment:
        deployment_domain_obj = Deployment()        
       
        # General section.
        deployment_domain_obj.project_ref = project_ref
        deployment_domain_obj.uuid          = json_deployment_obj["uuid"]
        deployment_domain_obj.display_name  = json_deployment_obj["display_name"]
        deployment_domain_obj.description   = json_deployment_obj["description"]
        deployment_domain_obj.last_update_time    = json_deployment_obj["last_update_time"]
        deployment_domain_obj.last_deploy_result    = json_deployment_obj["last_deploy_result"]
        deployment_domain_obj.cloud_type    = json_deployment_obj["cloud_params"]["type"]
        deployment_domain_obj.cloud_app_url    = json_deployment_obj["cloud_params"]["app_url"]

        # Leaf device section.
        deployment_domain_obj.leaf_devices = []
        if "leaf" in json_deployment_obj:
            for leaf_device_obj in json_deployment_obj["leaf"]:
                device_domain_obj = self.__deserialize_device(leaf_device_obj)
                deployment_domain_obj.leaf_devices.append(device_domain_obj)
            
        # Gateway device section.
        deployment_domain_obj.gateway_devices = []
        if "gateway" in json_deployment_obj:
            for gw_device_obj in json_deployment_obj["gateway"]:
                device_domain_obj = self.__deserialize_device(gw_device_obj)
                deployment_domain_obj.gateway_devices.append(device_domain_obj)
        
        return deployment_domain_obj
    

    def __deserialize_device(self, json_device_obj) -> Device:
        device = Device()

        device.device_id       = json_device_obj["device_id"]
        device.description     = json_device_obj["description"]
        
        if "display_name" in json_device_obj:
            device.display_name = json_device_obj["display_name"]
        else:
            device.display_name = "Device-Display-Name"
        if "gateway_id" in json_device_obj:
            device.gateway_id = json_device_obj["gateway_id"]
        if "wifi_mode" in json_device_obj:
            device.wifi_mode = json_device_obj["wifi_mode"]
        if "application" in json_device_obj:
            device.application = json_device_obj["application"]

        if "datalogging" in json_device_obj:
            device.datalogging_app = {}
            device.datalogging_app["application"] = json_device_obj["datalogging"]["application"]
            device.datalogging_app["firmware_update"] = json_device_obj["datalogging"]["firmware_update"]

        if "inference" in json_device_obj:
            device.inference_app = {}
            device.inference_app["application"] = json_device_obj["inference"]["application"]
            device.inference_app["firmware_update"] = json_device_obj["inference"]["firmware_update"]

            if "models" in json_device_obj["inference"]:
                device.inference_app["models"] = []
                for model in json_device_obj["inference"]["models"]:
                    devmodel = {}
                    devmodel["model_name_reference"]=model["model_name_reference"]
                    devmodel["artifact_type"] = model["artifact_type"]
                    devmodel["component_name"] = model["component_name"]
                    device.inference_app["models"].append(devmodel)

        return device

    def __serialize_deployment(self, deployment_domain_obj: Deployment) -> Any:
        json_deployment_domain_obj = dict({})

        if not deployment_domain_obj.uuid:
            deployment_domain_obj.uuid = str(uuid4())

        # General section.
        json_deployment_domain_obj["uuid"]           = deployment_domain_obj.uuid
        json_deployment_domain_obj["description"]    = deployment_domain_obj.description
        json_deployment_domain_obj["display_name"]   = deployment_domain_obj.display_name
        json_deployment_domain_obj["cloud_params"] = {
            "type": deployment_domain_obj.cloud_type,
            "app_url": deployment_domain_obj.cloud_app_url
        }
        json_deployment_domain_obj["last_update_time"]    = deployment_domain_obj.last_update_time
        json_deployment_domain_obj["last_deploy_result"]  = deployment_domain_obj.last_deploy_result

        # Leaf device section.
        json_deployment_domain_obj["leaf"] = []
        for leaf_device_obj in deployment_domain_obj.leaf_devices:
            json_device_domain_obj = self.__serialize_device(leaf_device_obj)
            json_deployment_domain_obj["leaf"].append(json_device_domain_obj)

        # Gateway device section.
        json_deployment_domain_obj["gateway"] = []
        for gateway_device_obj in deployment_domain_obj.gateway_devices:
            json_device_domain_obj = self.__serialize_device(gateway_device_obj)
            json_deployment_domain_obj["gateway"].append(json_device_domain_obj)        
        
        return json_deployment_domain_obj
    
    def __serialize_device(self, device_domain_obj: Device) -> Any:
        json_device_domain_obj = dict({})

        if device_domain_obj.application:
            json_device_domain_obj["application"] = device_domain_obj.application
        if device_domain_obj.gateway_id:
            json_device_domain_obj["gateway_id"] = device_domain_obj.gateway_id
        json_device_domain_obj["description"] = device_domain_obj.description
        json_device_domain_obj["display_name"] = device_domain_obj.display_name
        json_device_domain_obj["device_id"] = device_domain_obj.device_id
        if device_domain_obj.wifi_mode:
            json_device_domain_obj["wifi_mode"] = device_domain_obj.wifi_mode
        
        # Datalogging and Inference Leaf device section.
        json_device_domain_obj["datalogging"] = {}
        json_device_domain_obj["datalogging"]["application"] = device_domain_obj.datalogging_app
        json_device_domain_obj["datalogging"]["firmware_update"] = device_domain_obj.datalogging_fwupdate
        
        json_device_domain_obj["inference"] = {}
        json_device_domain_obj["inference"]["application"] = device_domain_obj.inference_app
        json_device_domain_obj["inference"]["firmware_update"] = device_domain_obj.inference_fwupdate

        json_device_domain_obj["inference"]["models"] = []
        for _model in device_domain_obj.inference_models:            
            model = dict({})

            model["artifact_type"] = _model.artifact_type
            model["component_name"] = _model.component_name
            model["model_name_reference"] = _model.model_name_reference

            json_device_domain_obj["inference"]["models"].append(model)

        return json_device_domain_obj