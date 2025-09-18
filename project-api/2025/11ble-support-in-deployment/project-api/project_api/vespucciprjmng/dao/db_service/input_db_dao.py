
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.db_service.http_connector import (
    HTTPDataConnector,
)
from project_api.vespucciprjmng.dao.db_service.service_specs import (
    DBServiceSpecs,
)
from project_api.vespucciprjmng.dao.input_dao import InputDAO
from project_api.vespucciprjmng.domain.input import Input, InputType
from project_api.vespucciprjmng.domain.log import Log
from project_api.vespucciprjmng.domain.model import Model
from project_api.vespucciprjmng.domain.tool import Tool


class InputDBDAO(InputDAO):
    """Input data access object for DB service"""
    
    def __init__(self, service_uri: str):
        self.__http_connector = HTTPDataConnector(service_uri)


    def get_all(self, project_uuid: str) -> List[Input]:
        """Get all stored inputs (without details) inside a project"""
        
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        input_domain_objs = []
        for json_input_obj in project_json_obj["inputs"]:
            input_domain_obj = self.__deserialize_input(project_ref=project_uuid, json_input_obj=json_input_obj)
            input_domain_objs.append(input_domain_obj)

        return input_domain_objs

    def get(self, project_uuid: str, model_uuid_or_name: str = None, input_uuid: str = None) -> Input:
        """Get input (with all details) given a model or input ID"""  
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))

        input_domain_obj = None

        if model_uuid_or_name:
            selected_json_model = self.__get_model_json_by_name_or_uuid(project_json_obj["models"], model_uuid_or_name)
            for json_input_obj in project_json_obj["inputs"]:
                if json_input_obj["model_ref"] == selected_json_model["uuid"]:
                    input_domain_obj = self.__deserialize_input(project_ref=project_uuid, json_input_obj=json_input_obj)
        else: 
            if input_uuid:
                for json_input_obj in project_json_obj["inputs"]:
                    if json_input_obj["uuid"] == input_uuid:
                        input_domain_obj = self.__deserialize_input(project_ref=project_uuid, json_input_obj=json_input_obj)
        
        return input_domain_obj

    def delete(self, project_uuid: str, model_uuid_or_name: str = None, input_uuid: str = None) -> None:
        """Delete input from related project"""
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        seleted_input_uuid = input_uuid
        if not seleted_input_uuid:
            if model_uuid_or_name:
                selected_json_obj_model = self.__get_model_json_by_name_or_uuid(project_json_obj["models"],model_uuid_or_name)
                for json_input_obj in project_json_obj["inputs"]:
                    if json_input_obj["model_ref"] == selected_json_obj_model["uuid"]:
                        seleted_input_uuid = json_input_obj["uuid"]
                        break
        self.__http_connector.delete(DBServiceSpecs.getInputPath(project_uuid=project_uuid, input_uuid=seleted_input_uuid))


    def update(self, project_uuid: str , input: Input) -> None:
        """Update existing input"""
        input_json_obj = self.serialize_input(input_domain_obj=input)
        self.__http_connector.put(subpath=DBServiceSpecs.getInputPath(project_uuid=project_uuid, input_uuid=input.uuid), body=input_json_obj)        


    def save(self, project_uuid: str , input: Input) -> None:
        """Save new input"""
        if not input.uuid:
            input.uuid = str(uuid4())
        input_json_obj = self.serialize_input(input_domain_obj=input)
        self.__http_connector.post(subpath=DBServiceSpecs.getInputsPath(project_uuid=project_uuid), body=input_json_obj)
        
    def __get_model_json_by_name_or_uuid(self, json_model_objs, model_uuid_or_name: str):
        for json_model_obj in json_model_objs:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                return json_model_obj

    def __deserialize_input(self, project_ref, json_input_obj) -> Input:
        input_domain_obj = Input()
        input_domain_obj.project_ref    = project_ref
        input_domain_obj.uuid           = json_input_obj["uuid"]
        input_domain_obj.model_ref      = Model(uuid=json_input_obj["model_ref"])
        input_domain_obj.input_type     = InputType(json_input_obj["input_type"])
        input_domain_obj.augmentations  = []
        for augmentation_file_name in json_input_obj["augmentation"]:
            input_domain_obj.augmentations.append(augmentation_file_name)

        input_domain_obj.logs = []
        for log_obj in json_input_obj["logs"]:
            log = Log()
            log.uuid = log_obj["uuid"]
            log.name = log_obj["name"]
            input_domain_obj.logs.append(log)

        input_domain_obj.tools = []
        for tool_obj in json_input_obj["tools"]:
            tool = Tool()
            tool.name = tool_obj["name"]
            tool.version = tool_obj["version"]
            input_domain_obj.tools.append(tool)

        return input_domain_obj

    def serialize_input(self, input_domain_obj: Input) -> Any:
        json_input_obj = dict({})

        if not input_domain_obj.uuid:
            input_domain_obj.uuid = str(uuid4())

        json_input_obj["uuid"]          = input_domain_obj.uuid
        json_input_obj["model_ref"]     = input_domain_obj.model_ref.uuid
        json_input_obj["input_type"]    = input_domain_obj.input_type.value
        if not input_domain_obj.augmentations:
            input_domain_obj.augmentations = []
        json_input_obj["augmentation"] = input_domain_obj.augmentations
        
        return json_input_obj