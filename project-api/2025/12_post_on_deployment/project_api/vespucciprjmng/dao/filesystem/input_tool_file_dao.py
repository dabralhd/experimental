
from typing import Any, List

from project_api.vespucciprjmng.dao.filesystem.json_data_connector import (
    JSONDataConnector,
)
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import (
    ProjectFileDAO,
)
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.tool_dao import ToolDAO
from project_api.vespucciprjmng.domain.tool import Tool
from project_api.vespucciprjmng.utils import read_json_attribute


class InputToolFileDAO(ToolDAO):
    """Input tool data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)

    def get_all(self, project_name: str, model_uuid_or_name_or_input_uuid: str = None) -> List[Tool]:
        """Get all stored input tools (without details) inside a project/model or input"""
        
        if not model_uuid_or_name_or_input_uuid:
            raise Exception("'get_all' tools for all models/inputs is not implemented")
        
        self.data_session.connect(get_project_file_name(project_name))

        tool_domain_objs = []

        selected_json_input_obj = self.__get_input_json_obj(model_uuid_or_name_or_input_uuid)

        for json_tool_obj in selected_json_input_obj["tools"]:
            tool_domain_obj = self.__deserialize_tool(project_ref=project_name, json_tool_obj=json_tool_obj)
            tool_domain_objs.append(tool_domain_obj)
        
        self.data_session.dispose()

        return tool_domain_objs

    def get(self, project_name: str, model_uuid_or_name_or_input_uuid: str, tool_name: str) -> Tool:
        """Get tool (with all details) given project/model or input"""
        
        self.data_session.connect(get_project_file_name(project_name))

        tool_domain_obj = None

        selected_json_input_obj = self.__get_input_json_obj(model_uuid_or_name_or_input_uuid)
        for json_tool_obj in selected_json_input_obj["tools"]:
            if json_tool_obj["name"] == tool_name:
                tool_domain_obj = self.__deserialize_tool(project_ref=project_name, json_tool_obj=json_tool_obj)
                break
        
        self.data_session.dispose()

        return tool_domain_obj
    
    def delete(self, project_name: str, model_uuid_or_name_or_input_uuid: str, tool_name: str) -> None:
        """Delete tool from related project/model/input"""
        self.data_session.connect(get_project_file_name(project_name))

        filtered_tool_domain_objs = []
        selected_json_input_obj = self.__get_input_json_obj(model_uuid_or_name_or_input_uuid)
        for json_tool_obj in selected_json_input_obj["tools"]:
            if not (json_tool_obj["name"] == tool_name) :
                filtered_tool_domain_objs.append(json_tool_obj)
                break
        selected_json_input_obj["tools"] = filtered_tool_domain_objs
        
        self.data_session.save()
        self.data_session.dispose()

    def save(self, project_name: str, model_uuid_or_name_or_input_uuid: str, old_tool_name:str, tool: Tool) -> None:
        """Save new tool or update existing tool for given model/input"""
    
        self.data_session.connect(get_project_file_name(project_name))

        selected_tool_json_obj = None
        selected_json_input_obj = self.__get_input_json_obj(model_uuid_or_name_or_input_uuid)

        for json_tool_obj in selected_json_input_obj["tools"]:
            if old_tool_name == json_tool_obj["name"]:
                selected_tool_json_obj = json_tool_obj
                break

        patched_json_tool_obj = self.__serialize_tool(tool)

        if selected_tool_json_obj:
            selected_tool_json_obj.update(patched_json_tool_obj) 
        else:
            selected_json_input_obj["tools"].append(patched_json_tool_obj)

        self.data_session.save()
        self.data_session.dispose()


    def __get_input_json_obj(self, model_uuid_or_name_or_input_uuid: str) -> Any:
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name_or_input_uuid or json_model_obj["name"] == model_uuid_or_name_or_input_uuid:
                selected_model_uuid = json_model_obj["uuid"]

        for json_input_obj in self.data_session.json_file["inputs"]:
            if json_input_obj["uuid"] == model_uuid_or_name_or_input_uuid or json_input_obj["model_ref"] == model_uuid_or_name_or_input_uuid or json_input_obj["model_ref"] == selected_model_uuid:
                return json_input_obj


    def __deserialize_tool(self, project_ref, json_tool_obj) -> Tool:
        tool_domain_obj = Tool()
        tool_domain_obj.project_ref  = project_ref
        tool_domain_obj.name         = json_tool_obj["name"]
        tool_domain_obj.version      = json_tool_obj["version"]
        tool_domain_obj.parameters    = read_json_attribute(json_tool_obj, "parameters")

        return tool_domain_obj

    def __serialize_tool(self, tool_domain_obj: Tool) -> Any:
        json_tool_obj = dict({})

        json_tool_obj["name"]        = tool_domain_obj.name
        json_tool_obj["version"]     = tool_domain_obj.version
        json_tool_obj["parameters"]  = tool_domain_obj.parameters
        
        return json_tool_obj