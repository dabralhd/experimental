
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.db_service.http_connector import (
    HTTPDataConnector,
)
from project_api.vespucciprjmng.dao.db_service.service_specs import (
    DBServiceSpecs,
)
from project_api.vespucciprjmng.dao.output_dao import OutputDAO
from project_api.vespucciprjmng.domain.model import Model
from project_api.vespucciprjmng.domain.output import Output, OutputType
from project_api.vespucciprjmng.domain.test import Test
from project_api.vespucciprjmng.domain.tool import Tool
from project_api.vespucciprjmng.utils import read_json_attribute


class OutputDBDAO(OutputDAO):
    """Output data access object for DB service"""
    
    
    def __init__(self, service_uri: str):
        self.__http_connector = HTTPDataConnector(service_uri)


    def get_all(self, project_uuid: str) -> List[Output]:
        """Get all stored outputs (without details) inside a project"""
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        output_domain_objs = []
        for json_output_obj in project_json_obj["outputs"]:
            input_domain_obj = self.__deserialize_output(project_ref=project_uuid, json_output_obj=json_output_obj)
            output_domain_objs.append(input_domain_obj)

        return output_domain_objs

    def get(self, project_uuid: str, model_uuid_or_name: str = None, output_uuid: str = None) -> Output:
        """Get output (with all details) given a model or output ID"""
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))

        output_domain_obj = None

        if model_uuid_or_name:
            selected_json_model = self.__get_model_json_by_name_or_uuid(project_json_obj["models"], model_uuid_or_name)
            for json_output_obj in project_json_obj["outputs"]:
                if json_output_obj["model_ref"] == selected_json_model["uuid"]:
                    output_domain_obj = self.__deserialize_output(project_ref=project_uuid, json_output_obj=json_output_obj)
        else: 
            if output_uuid:
                for json_output_obj in project_json_obj["outputs"]:
                    if json_output_obj["uuid"] == output_uuid:
                        output_domain_obj = self.__deserialize_output(project_ref=project_uuid, json_output_obj=json_output_obj)
        return output_domain_obj
    
    def delete(self, project_uuid: str, model_uuid_or_name: str = None, output_uuid: str = None) -> None:
        """Delete output from related project"""
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        seleted_output_uuid = output_uuid
        if not seleted_output_uuid:
            if model_uuid_or_name:
                selected_json_obj_model = self.__get_model_json_by_name_or_uuid(project_json_obj["models"],model_uuid_or_name)
                for json_output_obj in project_json_obj["outputs"]:
                    if json_output_obj["model_ref"] == selected_json_obj_model["uuid"]:
                        seleted_output_uuid = json_output_obj["uuid"]
                        break
        self.__http_connector.delete(DBServiceSpecs.getOutputPath(project_uuid=project_uuid, output_uuid=seleted_output_uuid))

    def update(self, project_uuid: str, output: Output) -> None:
        """Update existing output"""
        output_json_obj = self.serialize_output(output_domain_obj=output)
        self.__http_connector.put(subpath=DBServiceSpecs.getOutputPath(project_uuid=project_uuid, output_uuid=output.uuid), body=output_json_obj)        

    
    def save(self, project_uuid: str, output: Output) -> None:
        """Save new output or update existing output"""
        if not output.uuid:
            output.uuid = str(uuid4())
        output_json_obj = self.serialize_output(output_domain_obj=output)
        self.__http_connector.post(subpath=DBServiceSpecs.getOutputsPath(project_uuid=project_uuid), body=output_json_obj)

    def __get_model_json_by_name_or_uuid(self, json_model_objs, model_uuid_or_name: str):
        for json_model_obj in json_model_objs:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                return json_model_obj

    def __deserialize_output(self, project_ref, json_output_obj) -> Model:
        output_domain_obj = Output()
        output_domain_obj.project_ref    = project_ref
        output_domain_obj.uuid           = json_output_obj["uuid"]
        output_domain_obj.model_ref      = Model(uuid=json_output_obj["model_ref"])
        output_domain_obj.output_type    = OutputType(json_output_obj["output_type"])
 
        output_domain_obj.tests = []
        for test_obj in json_output_obj["tests"]:
            test = Test()
            test.uuid = test_obj["uuid"]
            test.name = test_obj["name"]
            output_domain_obj.tests.append(test)

            if test.uuid == read_json_attribute(json_output_obj, "best_test"):
                output_domain_obj.best_test = test

        output_domain_obj.tools = []
        for tool_obj in json_output_obj["tools"]:
            tool = Tool()
            tool.name = tool_obj["name"]
            tool.version = tool_obj["version"]
            output_domain_obj.tools.append(tool)

        return output_domain_obj

    def serialize_output(self, output_domain_obj: Output) -> Any:
        json_output_obj = dict({})

        if not output_domain_obj.uuid:
            output_domain_obj.uuid = str(uuid4())

        json_output_obj["uuid"]          = output_domain_obj.uuid
        json_output_obj["model_ref"]     = output_domain_obj.model_ref.uuid
        json_output_obj["output_type"]   = output_domain_obj.output_type
        
        json_output_obj["events"] = []
        json_output_obj["output_version"] = ""
        json_output_obj["ui"] = {}

        return json_output_obj