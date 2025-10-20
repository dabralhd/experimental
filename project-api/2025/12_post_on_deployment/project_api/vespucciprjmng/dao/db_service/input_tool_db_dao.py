
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.db_service.domain.db_tool import DBTool
from project_api.vespucciprjmng.dao.db_service.http_connector import (
    HTTPDataConnector,
)
from project_api.vespucciprjmng.dao.db_service.service_specs import (
    DBServiceSpecs,
)
from project_api.vespucciprjmng.dao.tool_dao import ToolDAO
from project_api.vespucciprjmng.utils import read_json_attribute


class InputToolDBDAO(ToolDAO):
    """Input tool data access object for DB service"""
    
    def __init__(self, service_uri: str):
        self.__http_connector = HTTPDataConnector(service_uri)

    def get_all(self, project_uuid: str, model_uuid_or_name_or_input_uuid: str = None) -> List[DBTool]:
        """Get all stored input tools (without details) inside a project/model or input"""
        
        if not model_uuid_or_name_or_input_uuid:
            raise Exception("'get_all' tools for all models/inputs is not implemented")
        
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))

        tool_domain_objs = []

        selected_json_input_obj = self.__get_input_json_obj(project_json_obj, model_uuid_or_name_or_input_uuid)

        for json_tool_obj in selected_json_input_obj["tools"]:
            tool_domain_obj = self.__deserialize_tool(project_ref=project_uuid, json_tool_obj=json_tool_obj)
            tool_domain_objs.append(tool_domain_obj)

        return tool_domain_objs

    def get(self, project_uuid: str, model_uuid_or_name_or_input_uuid: str, tool_name_or_uuid: str) -> DBTool:
        """Get tool (with all details) given project/model or input"""
        
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))

        tool_domain_obj = None

        selected_json_input_obj = self.__get_input_json_obj(project_json_obj, model_uuid_or_name_or_input_uuid)
        for json_tool_obj in selected_json_input_obj["tools"]:
            if json_tool_obj["name"] == tool_name_or_uuid or json_tool_obj["uuid"] == tool_name_or_uuid:
                tool_domain_obj = self.__deserialize_tool(project_ref=project_uuid, json_tool_obj=json_tool_obj)
                break

        return tool_domain_obj
    
    def delete(self, project_uuid: str, model_uuid_or_name_or_input_uuid: str, tool_name_or_uuid: str) -> None:
        """Delete tool from related project/model/input"""
        
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        selected_json_input_obj = self.__get_input_json_obj(project_json_obj, model_uuid_or_name_or_input_uuid)
        for tool_json_obj in selected_json_input_obj["tools"]:
            if tool_name_or_uuid == tool_json_obj["name"] or tool_name_or_uuid == tool_json_obj["uuid"]:
                self.__http_connector.delete(DBServiceSpecs.getInputToolPath(project_uuid=project_uuid, input_uuid=selected_json_input_obj["uuid"], tool_uuid=tool_json_obj["uuid"]))
                break

    def update(self, project_uuid: str, model_uuid_or_name_or_input_uuid: str, tool: DBTool) -> None:
        """Update existing tool for given model/input"""
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        selected_json_input_obj = self.__get_input_json_obj(project_json_obj, model_uuid_or_name_or_input_uuid)
        updated_json_tool = self.serialize_tool(tool_domain_obj=tool)
        self.__http_connector.put(DBServiceSpecs.getInputToolPath(project_uuid=project_uuid, input_uuid=selected_json_input_obj["uuid"], tool_uuid=tool.uuid), updated_json_tool)

    def save(self, project_uuid: str, model_uuid_or_name_or_input_uuid: str, tool: DBTool) -> None:
        """Save new tool for given model/input"""
        if not tool.uuid:
            tool.uuid = str(uuid4())
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        selected_json_input_obj = self.__get_input_json_obj(project_json_obj, model_uuid_or_name_or_input_uuid)
        new_json_tool = self.serialize_tool(tool_domain_obj=tool)
        self.__http_connector.post(DBServiceSpecs.getInputToolsPath(project_uuid=project_uuid, input_uuid=selected_json_input_obj["uuid"]), new_json_tool)
        
    def __get_input_json_obj(self, project_json_obj: Any, model_uuid_or_name_or_input_uuid: str) -> Any:
        for json_model_obj in project_json_obj["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name_or_input_uuid or json_model_obj["name"] == model_uuid_or_name_or_input_uuid:
                selected_model_uuid = json_model_obj["uuid"]

        for json_input_obj in project_json_obj["inputs"]:
            if json_input_obj["uuid"] == model_uuid_or_name_or_input_uuid or json_input_obj["model_ref"] == model_uuid_or_name_or_input_uuid or json_input_obj["model_ref"] == selected_model_uuid:
                return json_input_obj


    def __deserialize_tool(self, project_ref, json_tool_obj) -> DBTool:
        tool_domain_obj = DBTool()
        tool_domain_obj.project_ref  = project_ref
        tool_domain_obj.uuid         = json_tool_obj["uuid"]
        tool_domain_obj.name         = json_tool_obj["name"]
        tool_domain_obj.version      = json_tool_obj["version"]
        tool_domain_obj.parameters    = read_json_attribute(json_tool_obj, "parameters")

        return tool_domain_obj

    def serialize_tool(self, tool_domain_obj: DBTool) -> Any:
        json_tool_obj = dict({})

        if not tool_domain_obj.uuid:
            tool_domain_obj.uuid = str(uuid4())
            
        json_tool_obj["uuid"]        = tool_domain_obj.uuid
        json_tool_obj["name"]        = tool_domain_obj.name
        json_tool_obj["version"]     = tool_domain_obj.version
        json_tool_obj["parameters"]  = tool_domain_obj.parameters
        json_tool_obj["description"]        = ""
        json_tool_obj["container_name"]     = ""
        json_tool_obj["container_version"]  = ""

        return json_tool_obj