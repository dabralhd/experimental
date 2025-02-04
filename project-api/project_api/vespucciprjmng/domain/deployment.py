from typing import List
from enum import Enum
from datetime import datetime

from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ

class InfModel():
    @property
    def artifact_type(self) -> str:
        return self._artifact_type

    @artifact_type.setter
    def artifact_type(self, artifact_type: str):
        self._artifact_type = artifact_type

    @property
    def component_name(self) -> str:
        return self._component_name

    @component_name.setter
    def type(self, component_name: str):
        self._component_name = component_name

    @property
    def model_name_reference(self) -> str:
        return self._model_name_reference

    @model_name_reference.setter
    def model_name_reference(self, model_name_reference: str):
        self._model_name_reference = model_name_reference

    def __init__(self, 
                 artifact_type: str = "", 
                 component_name: str = "", 
                 model_name_reference: str = ""):
        self._artifact_type: str = artifact_type
        self._component_name: str = component_name
        self._model_name_reference: str = model_name_reference


class Application():

    @property
    def uuid(self) -> str:
        return self._uuid

    @uuid.setter
    def uuid(self, uuid: str):
        self._uuid = uuid

    @property
    def type(self) -> bool:
        return self._type

    @type.setter
    def type(self, type: bool):
        self._type = type

    @property
    def device_template_uri(self) -> str:
        return self._device_template_uri

    @device_template_uri.setter
    def device_template_uri(self, device_template_uri: str):
        self._device_template_uri = device_template_uri

    @property
    def device_template_id(self) -> str:
        return self._device_template_id

    @device_template_id.setter
    def device_template_id(self, device_template_id: str):
        self._device_template_id = device_template_id

    @property
    def device_manifest_uri(self) -> str:
        return self._device_manifest_uri

    @device_manifest_uri.setter
    def device_manifest_uri(self, device_manifest_uri: str):
        self._device_manifest_uri = device_manifest_uri   

    @property
    def image_uri(self) -> str:
        return self._image_uri

    @image_uri.setter
    def image_uri(self, image_uri: str):
        self._image_uri = image_uri  
    
    @property
    def module_id(self) -> str:
        return self._module_id

    @module_id.setter
    def module_id(self, module_id: str):
        self._module_id = module_id
    
    @property
    def binary_uri(self) -> str:
        return self._binary_uri

    @binary_uri.setter
    def binary_uri(self, binary_uri: str):
        self._binary_uri = binary_uri
    
    @property
    def binary_id(self) -> int:
        return self._binary_id

    @binary_id.setter
    def binary_id(self, binary_id: int):
        self._binary_id = binary_id
    
    @property
    def protocol(self) -> int:
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: int):
        self._protocol = protocol

    def __init__(self, uuid: str = "", type: bool = True, device_template_uri: str = "", device_template_id: str = "", 
                 device_manifest_uri: str = "", image_uri: str = "", module_id: str = "", binary_uri: str = "", 
                 binary_id: int = 0, protocol: int = 0):
        self._uuid = uuid
        self._type = type
        self._device_template_uri = device_template_uri
        self._device_template_id = device_template_id
        self._device_manifest_uri = device_manifest_uri
        self._image_uri = image_uri
        self._module_id = module_id
        self._binary_uri = binary_uri
        self._binary_id = binary_id
        self._protocol = protocol

        
class Device():

    @property
    def gateway_id(self) -> str:
        return self.__gateway_id

    @gateway_id.setter 
    def gateway_id(self, value: str):
        self.__gateway_id = value

    @property
    def device_id(self) -> str:
        return self.__device_id

    @device_id.setter 
    def device_id(self, value: str):
        self.__device_id = value

    @property
    def display_name(self) -> str:
        return self.__display_name

    @display_name.setter
    def display_name(self, value: str):
        self.__display_name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter 
    def description(self, value: str):
        self.__description = value

    @property
    def application(self) -> str:
        return self.__application

    @application.setter 
    def application(self, value: str):
        self.__application = value

    @property
    def wifi_mode(self) -> str:
        return self.__wifi_mode

    @wifi_mode.setter 
    def wifi_mode(self, value: str):
        self.__wifi_mode = value

    @property
    def inference_app(self) -> str:
        return self.__inference_app

    @inference_app.setter 
    def inference_app(self, value: str):
        self.__inference_app = value

    @property
    def inference_fwupdate(self) -> str:
        return self.__inference_fwupdate

    @inference_fwupdate.setter 
    def inference_fwupdate(self, value: str):
        self.__inference_fwupdate = value

    @property
    def datalogging_app(self) -> str:
        return self.__datalogging_app
    
    @datalogging_app.setter 
    def datalogging_app(self, value: str):
        self.__datalogging_app = value

    @property
    def datalogging_fwupdate(self) -> str:
        return self.__datalogging_fwupdate
    
    @datalogging_fwupdate.setter 
    def datalogging_fwupdate(self, value: str):
        self.__datalogging_fwupdate = value
    
    @property
    def inference_models(self) -> List[InfModel]:
        return self.__inference_models
    
    @inference_models.setter 
    def inference_models(self, value: List[InfModel]):
        self.__inference_models = value

    def __init__(self, 
                 gateway_id: str = "", 
                 device_id: str = "", 
                 display_name: str = "", 
                 description: str = "", 
                 application: str = "", 
                 wifi_mode: str = "", 
                 inference_app: str = "", 
                 inference_fwupdate: str = "", 
                 datalogging_app: str = "", 
                 datalogging_fwupdate: str = "", 
                 inference_models: List[InfModel] = []):
        self.__gateway_id: str = gateway_id
        self.__device_id: str = device_id
        self.__display_name: str = display_name
        self.__description: str = description
        self.__application: str = application
        self.__wifi_mode: str = wifi_mode
        self.__inference_app: str = inference_app
        self.__inference_fwupdate: str = inference_fwupdate
        self.__datalogging_app: str = datalogging_app
        self.__datalogging_fwupdate: str = datalogging_fwupdate
        self.__inference_models: List[InfModel] = inference_models if inference_models is not None else []


class Deployment(DomainOBJ):
    """Deployment data model"""
    
    @property
    def uuid(self) -> str:
        return self.__uuid

    @uuid.setter 
    def uuid(self, value: str):
        self.__uuid = value

    @property
    def display_name(self) -> str:
        return self.__display_name

    @display_name.setter 
    def display_name(self, value: str):
        self.__display_name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter 
    def description(self, value: str):
        self.__description = value

    # TODO: maybe this should be a structured data type?
    @property
    def last_update_time(self) -> str:
        return self.__last_update_time

    @last_update_time.setter
    def last_update_time(self, value: str):
        self.__last_update_time = value

    @property
    def last_deploy_result(self) -> str:
        return self.__last_deploy_result

    @last_deploy_result.setter
    def last_deploy_result(self, value: str):
        self.__last_deploy_result = value

    @property
    def cloud_type(self) -> str:
        return self.__cloud_type

    @cloud_type.setter 
    def cloud_type(self, value: str):
        self.__cloud_type = value

    @property
    def cloud_app_url(self) -> str:
        return self.__cloud_app_url

    @cloud_app_url.setter 
    def cloud_app_url(self, value: str):
        self.__cloud_app_url = value

    @property
    def leaf_devices(self) -> List[Device]:
        return self.__leaf_devices

    @leaf_devices.setter 
    def leaf_devices(self, value: List[Device]):
        self.__leaf_devices = value

    @property
    def gateway_devices(self) -> List[Device]:
        return self.__gateway_devices

    @gateway_devices.setter 
    def gateway_devices(self, value: List[Device]):
        self.__gateway_devices = value

    def __init__(self, uuid: str = None, display_name: str = None, description: str = None, cloud_type: str = None, cloud_app_url: str=None, leaf_devices: List[Device] = None, gateway_devices: List[Device] = None):
        self.__uuid             = uuid
        self.__display_name     = display_name
        self.__description      = description
        self.__cloud_type       = cloud_type
        self.__cloud_app_url    = cloud_app_url
        self.__last_update_time = str(datetime.now()) 
        self.__last_deploy_result = "success"
        self.__leaf_devices     = leaf_devices
        self.__gateway_devices  = gateway_devices