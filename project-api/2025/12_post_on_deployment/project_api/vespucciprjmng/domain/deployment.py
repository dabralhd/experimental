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


class Bluest_V3_PayloadDecodingSchemaInstance():
    def __init__(self, component: str = "", telemetry: str = "", type_: str = ""):
        self.component = component
        self.telemetry = telemetry
        self.type = type_
        
    @property
    def component(self) -> str:
        return self._component

    @component.setter
    def component(self, value: str):
        self._component = value

    @property
    def telemetry(self) -> str:
        return self._telemetry

    @telemetry.setter
    def telemetry(self, value: str):
        self._telemetry = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    def to_dict(self) -> dict:
        return {
            "component": self.component,            
            "telemetry": self.telemetry,
            "type": self.type
        }


class Bluest_V3_PayloadDecodingSchema:
    def __init__(self, instances: List[Bluest_V3_PayloadDecodingSchemaInstance] = None):
        self.instances = instances if instances is not None else []

    @property
    def instances(self) -> List[Bluest_V3_PayloadDecodingSchemaInstance]:
        return self._instances

    @instances.setter
    def instances(self, value: List[Bluest_V3_PayloadDecodingSchemaInstance]):
        self._instances = value

    def to_dict(self) -> dict:
        return {
            "instances": [instance.to_dict() for instance in self.instances]
        }


class Bluest_V3_Payload:
    def __init__(
        self,
        device_id: str = "",
        fw_id: str = "",
        payload_id: str = "",
        decoding_schema: list = None
    ):
        self.device_id = device_id
        self.fw_id = fw_id
        self.payload_id = payload_id
        self.decoding_schema = decoding_schema if decoding_schema is not None else []

    @property
    def device_id(self) -> str:
        return self._device_id

    @device_id.setter
    def device_id(self, value: str):
        self._device_id = value

    @property
    def fw_id(self) -> str:
        return self._fw_id

    @fw_id.setter
    def fw_id(self, value: str):
        self._fw_id = value

    @property
    def payload_id(self) -> str:
        return self._payload_id

    @payload_id.setter
    def payload_id(self, value: str):
        self._payload_id = value

    @property
    def decoding_schema(self) -> Bluest_V3_PayloadDecodingSchema:
        return self._decoding_schema

    @decoding_schema.setter
    def decoding_schema(self, value: Bluest_V3_PayloadDecodingSchema):
        self._decoding_schema = value

    def to_dict(self) -> dict:
        return {
            "device_id": self.device_id,
            "fw_id": self.fw_id,
            "payload_id": self.payload_id,
            "decoding_schema": [ds.to_dict() for ds in self.decoding_schema]
        }

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

    @property 
    def bluest_v3_payload(self) -> Bluest_V3_Payload:
        return self._bluest_v3_payload
    
    @bluest_v3_payload.setter
    def bluest_v3_payload(self, bluest_v3_payload: Bluest_V3_Payload):
        self._bluest_v3_payload = bluest_v3_payload   

    def __init__(self, uuid: str = "", type: bool = True, device_template_uri: str = "", device_template_id: str = "", 
                 device_manifest_uri: str = "", image_uri: str = "", module_id: str = "", binary_uri: str = "", 
                 binary_id: int = 0, protocol: int = 0, bluest_v3_payload: Bluest_V3_Payload=  None):
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
        self._bluest_v3_payload = bluest_v3_payload


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
    def inference_fwupdate(self) -> bool:
        return self.__inference_fwupdate

    @inference_fwupdate.setter 
    def inference_fwupdate(self, value: bool):
        self.__inference_fwupdate = value

    @property
    def datalogging_app(self) -> str:
        return self.__datalogging_app
    
    @datalogging_app.setter 
    def datalogging_app(self, value: str):
        self.__datalogging_app = value

    @property
    def datalogging_fwupdate(self) -> bool:
        return self.__datalogging_fwupdate
    
    @datalogging_fwupdate.setter 
    def datalogging_fwupdate(self, value: bool):
        self.__datalogging_fwupdate = value
    
    @property
    def inference_models(self) -> List[InfModel]:
        return self.__inference_models
    
    @inference_models.setter 
    def inference_models(self, value: List[InfModel]):
        self.__inference_models = value
        
    
    @property
    def inference_supported_applications(self) -> List[str]:
        return self.__inference_supported_applications
    
    @inference_supported_applications.setter 
    def inference_supported_applications(self, value: List[str]):
        self.__inference_supported_applications = value

    
    @property
    def datalogging_supported_applications(self) -> List[str]:
        return self.__datalogging_supported_applications
    
    @datalogging_supported_applications.setter 
    def datalogging_supported_applications(self, value: List[str]):
        self.__datalogging_supported_applications = value

    def __init__(self, 
                 gateway_id: str = "", 
                 device_id: str = "", 
                 display_name: str = "", 
                 description: str = "", 
                 application: str = "", 
                 wifi_mode: str = "", 
                 inference_app: str = "", 
                 inference_fwupdate: bool = False, 
                 datalogging_app: str = "", 
                 datalogging_fwupdate: bool = False, 
                 inference_models: List[InfModel] = [],
                 inference_supported_applications: List[str] = [],
                 datalogging_supported_applications: List[str] = []):
        self.__gateway_id: str = gateway_id
        self.__device_id: str = device_id
        self.__display_name: str = display_name
        self.__description: str = description
        self.__application: str = application
        self.__wifi_mode: str = wifi_mode
        self.__inference_app: str = inference_app
        self.__inference_fwupdate: bool = inference_fwupdate
        self.__datalogging_app: str = datalogging_app
        self.__datalogging_fwupdate: bool = datalogging_fwupdate
        self.__inference_models: List[InfModel] = inference_models if inference_models is not None else []
        self.__inference_supported_applications: List[str] = inference_supported_applications if inference_supported_applications is not None else []
        self.__datalogging_supported_applications: List[str] = datalogging_supported_applications if datalogging_supported_applications is not None else []


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

