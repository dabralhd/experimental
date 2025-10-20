
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.filesystem.json_data_connector import (
    JSONDataConnector,
)
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import (
    ProjectFileDAO,
)
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.output_dao import OutputDAO
from project_api.vespucciprjmng.domain.model import Model
from project_api.vespucciprjmng.domain.output import Output, OutputType
from project_api.vespucciprjmng.domain.test import Test
from project_api.vespucciprjmng.domain.tool import Tool
from project_api.vespucciprjmng.utils import read_json_attribute


class OutputFileDAO(OutputDAO):
    """Output data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)

    def get_all(self, project_name: str) -> List[Output]:
        """Get all stored outputs (without details) inside a project"""

        self.data_session.connect(get_project_file_name(project_name))

        output_domain_objs = []
        for json_output_obj in self.data_session.json_file["outputs"]:
            output_domain_obj = self.__deserialize_output(project_ref=project_name, json_output_obj=json_output_obj)
            output_domain_objs.append(output_domain_obj)
        
        self.data_session.dispose()

        return output_domain_objs

    def get(self, project_name: str, model_uuid_or_name: str = None, output_uuid: str = None) -> Output:
        """Get output (with all details) given a model or output ID"""

        self.data_session.connect(get_project_file_name(project_name))

        output_domain_obj = None

        if model_uuid_or_name:
            for json_model_obj in self.data_session.json_file["models"]:
                if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                    for json_output_obj in self.data_session.json_file["outputs"]:
                        if json_output_obj["model_ref"] == json_model_obj["uuid"]:
                            output_domain_obj = self.__deserialize_output(project_ref=project_name, json_output_obj=json_output_obj)
        else: 
            if output_uuid:
                for json_output_obj in self.data_session.json_file["outputs"]:
                    if json_output_obj["uuid"] == output_uuid:
                        output_domain_obj = self.__deserialize_output(project_ref=project_name, json_output_obj=json_output_obj)
        
        self.data_session.dispose()

        return output_domain_obj
    
    def delete(self, project_name: str, model_uuid_or_name: str = None, output_uuid: str = None) -> None:
        """Delete output from related project"""
        self.data_session.connect(get_project_file_name(project_name))

        if output_uuid:
            filtered_json_output_objs = []
            for json_output_obj in self.data_session.json_file["outputs"]:
                if json_output_obj["uuid"] != output_uuid:
                    filtered_json_output_objs.append(json_output_obj)
            self.data_session.json_file["outputs"] = filtered_json_output_objs
        else:
            if model_uuid_or_name:
                selected_json_obj_model = self.__get_model_json_by_name_or_uuid(self.data_session.json_file["models"],model_uuid_or_name)
                filtered_json_output_objs = []
                for json_output_obj in self.data_session.json_file["outputs"]:
                    if json_output_obj["model_ref"] != selected_json_obj_model["uuid"]:
                        filtered_json_output_objs.append(json_output_obj)
                self.data_session.json_file["outputs"] = filtered_json_output_objs

        self.data_session.save()
        self.data_session.dispose()

    def save(self, project_name: str, model_uuid_or_name: str, output: Output) -> None:
        """Save new output or update existing output"""
        self.data_session.connect(get_project_file_name(project_name))

        selected_json_output_obj = None
        for json_output_obj in self.data_session.json_file["outputs"]:
            if json_output_obj["uuid"] == output.uuid:
                selected_json_output_obj = json_output_obj
                break

        selected_model_json_obj = self.__get_model_json_by_name_or_uuid(self.data_session.json_file["models"], model_uuid_or_name)
        output.model_ref = Model(uuid=selected_model_json_obj["uuid"])
        patched_json_output_obj = self.__serialize_output(output)

        if selected_json_output_obj:
            selected_json_output_obj.update(patched_json_output_obj)
            if "tests" not in selected_json_output_obj:
                selected_json_output_obj["tests"] = []   
            if "tools" not in selected_json_output_obj:
                selected_json_output_obj["tools"] = []   
        else:
            if "tests" not in patched_json_output_obj:
                patched_json_output_obj["tests"] = []   
            if "tools" not in patched_json_output_obj:
                patched_json_output_obj["tools"] = []   
            self.data_session.json_file["outputs"].append(patched_json_output_obj)

        self.data_session.save()
        self.data_session.dispose()

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

    def __serialize_output(self, output_domain_obj: Output) -> Any:
        json_output_obj = dict({})

        if not output_domain_obj.uuid:
            output_domain_obj.uuid = str(uuid4())

        json_output_obj["uuid"]          = output_domain_obj.uuid
        json_output_obj["model_ref"]     = output_domain_obj.model_ref.uuid
        json_output_obj["output_type"]   = output_domain_obj.output_type
        if output_domain_obj.best_test is not None:
            json_output_obj["best_test"] = output_domain_obj.best_test.uuid
        else:
            json_output_obj["best_test"] = None

        return json_output_obj