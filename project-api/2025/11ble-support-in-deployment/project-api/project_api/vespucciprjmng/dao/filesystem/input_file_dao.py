
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.filesystem.json_data_connector import (
    JSONDataConnector,
)
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import (
    ProjectFileDAO,
)
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.input_dao import InputDAO
from project_api.vespucciprjmng.domain.input import Input, InputType
from project_api.vespucciprjmng.domain.log import Log
from project_api.vespucciprjmng.domain.model import Model
from project_api.vespucciprjmng.domain.tool import Tool


class InputFileDAO(InputDAO):
    """Input data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)

    def get_all(self, project_name: str) -> List[Input]:
        """Get all stored inputs (without details) inside a project"""

        self.data_session.connect(get_project_file_name(project_name))

        input_domain_objs = []
        for json_input_obj in self.data_session.json_file["inputs"]:
            input_domain_obj = self.__deserialize_input(project_ref=project_name, json_input_obj=json_input_obj)
            input_domain_objs.append(input_domain_obj)
        
        self.data_session.dispose()

        return input_domain_objs

    def get(self, project_name: str, model_uuid_or_name: str = None, input_uuid: str = None) -> Input:
        """Get input (with all details) given a model or input ID"""

        self.data_session.connect(get_project_file_name(project_name))

        input_domain_obj = None

        if model_uuid_or_name:
            selected_json_model = self.__get_model_json_by_name_or_uuid(self.data_session.json_file["models"], model_uuid_or_name)
            for json_input_obj in self.data_session.json_file["inputs"]:
                if json_input_obj["model_ref"] == selected_json_model["uuid"]:
                    input_domain_obj = self.__deserialize_input(project_ref=project_name, json_input_obj=json_input_obj)
        else: 
            if input_uuid:
                for json_input_obj in self.data_session.json_file["inputs"]:
                    if json_input_obj["uuid"] == input_uuid:
                        input_domain_obj = self.__deserialize_input(project_ref=project_name, json_input_obj=json_input_obj)
        
        self.data_session.dispose()

        return input_domain_obj
    
    def delete(self, project_name: str, model_uuid_or_name: str = None, input_uuid: str = None) -> None:
        """Delete input from related project"""
        self.data_session.connect(get_project_file_name(project_name))

        if input_uuid:
            filtered_json_input_objs = []
            for json_input_obj in self.data_session.json_file["inputs"]:
                if json_input_obj["uuid"] != input_uuid:
                    filtered_json_input_objs.append(json_input_obj)
            self.data_session.json_file["inputs"] = filtered_json_input_objs
        else:
            if model_uuid_or_name:
                selected_json_obj_model = self.__get_model_json_by_name_or_uuid(self.data_session.json_file["models"],model_uuid_or_name)
                filtered_json_input_objs = []
                for json_input_obj in self.data_session.json_file["inputs"]:
                    if json_input_obj["model_ref"] != selected_json_obj_model["uuid"]:
                        filtered_json_input_objs.append(json_input_obj)
                self.data_session.json_file["inputs"] = filtered_json_input_objs

        self.data_session.save()
        self.data_session.dispose()

    def save(self, project_name: str, model_uuid_or_name: str, input: Input) -> None:
        """Save new input or update existing input"""
    
        self.data_session.connect(get_project_file_name(project_name))

        selected_json_input_obj = None
        for json_input_obj in self.data_session.json_file["inputs"]:
            if json_input_obj["uuid"] == input.uuid:
                selected_json_input_obj = json_input_obj
                break
        
        selected_json_obj_model = self.__get_model_json_by_name_or_uuid(self.data_session.json_file["models"],model_uuid_or_name)
        input.model_ref = Model(uuid=selected_json_obj_model["uuid"])
        patched_json_input_obj = self.__serialize_input(input)

        if selected_json_input_obj:
            selected_json_input_obj.update(patched_json_input_obj)
            if "logs" not in selected_json_input_obj:
                selected_json_input_obj["logs"] = []   
            if "tools" not in selected_json_input_obj:
                selected_json_input_obj["tools"] = []   
        else:
            if "logs" not in patched_json_input_obj:
                patched_json_input_obj["logs"] = []   
            if "tools" not in patched_json_input_obj:
                patched_json_input_obj["tools"] = []   
            self.data_session.json_file["inputs"].append(patched_json_input_obj)

        self.data_session.save()
        self.data_session.dispose()

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

    def __serialize_input(self, input_domain_obj: Input) -> Any:
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