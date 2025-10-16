
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.filesystem.json_data_connector import (
    JSONDataConnector,
)
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import (
    ProjectFileDAO,
)
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.test_dao import TestDAO
from project_api.vespucciprjmng.domain.experiment import Experiment
from project_api.vespucciprjmng.domain.test import Test


class TestFileDAO(TestDAO):
    """Test data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)

    def get_all(self, project_name: str, model_uuid_or_name_or_output_uuid: str, experiment_uuid_or_name: str = None) -> List[Test]:
        """Get all stored tests (without details) inside a project/model or output"""
        
        self.data_session.connect(get_project_file_name(project_name))

        test_domain_objs = []
        
        selected_json_output_obj = self.__get_output_json_obj(model_uuid_or_name_or_output_uuid)
        selected_json_experiment_obj = self.__get_json_experiment_by_model(self.data_session.json_file, selected_json_output_obj["model_ref"], experiment_uuid_or_name)
        
        for json_test_obj in selected_json_output_obj["tests"]:
            if not experiment_uuid_or_name:
                test_domain_obj = self.__deserialize_test(project_ref=project_name, json_test_obj=json_test_obj)
                test_domain_objs.append(test_domain_obj)
            else:
                if json_test_obj["experiment_ref"] == selected_json_experiment_obj["uuid"]:
                    test_domain_obj = self.__deserialize_test(project_ref=project_name, json_test_obj=json_test_obj)
                    test_domain_objs.append(test_domain_obj)
        
        self.data_session.dispose()

        return test_domain_objs

    def get(self, project_name: str, model_uuid_or_name_or_output_uuid: str, experiment_uuid_or_name: str, test_name_or_uuid: str) -> Test:
        """Get test (with all details) given project/model or output"""
        
        self.data_session.connect(get_project_file_name(project_name))

        test_domain_obj = None

        selected_json_output_obj = self.__get_output_json_obj(model_uuid_or_name_or_output_uuid)
        selected_json_experiment_obj = self.__get_json_experiment_by_model(self.data_session.json_file, selected_json_output_obj["model_ref"], experiment_uuid_or_name)

        for json_test_obj in selected_json_output_obj["tests"]:
            if (selected_json_experiment_obj["uuid"] == json_test_obj["experiment_ref"] or selected_json_experiment_obj["name"] == experiment_uuid_or_name) and (json_test_obj["name"] == test_name_or_uuid or json_test_obj["uuid"] == test_name_or_uuid):
                test_domain_obj = self.__deserialize_test(project_ref=project_name, json_test_obj=json_test_obj)
                break
        
        self.data_session.dispose()

        return test_domain_obj
    
    def delete(self, project_name: str, model_uuid_or_name_or_output_uuid: str, experiment_uuid_or_name: str, test_name_or_uuid: str) -> None:
        """Delete test from related project/model/output"""
        self.data_session.connect(get_project_file_name(project_name))

        filtered_test_domain_objs = []
        selected_json_output_obj = self.__get_output_json_obj(model_uuid_or_name_or_output_uuid)
        selected_json_experiment_obj = self.__get_json_experiment_by_model(self.data_session.json_file, selected_json_output_obj["model_ref"], experiment_uuid_or_name)

        for json_test_obj in selected_json_output_obj["tests"]:
            if not (selected_json_experiment_obj["uuid"] == json_test_obj["experiment_ref"] and (json_test_obj["name"] == test_name_or_uuid or json_test_obj["uuid"] == test_name_or_uuid)) :
                filtered_test_domain_objs.append(json_test_obj)
                break
        selected_json_output_obj["tests"] = filtered_test_domain_objs
        
        self.data_session.save()
        self.data_session.dispose()

    def save(self, project_name: str, model_uuid_or_name_or_output_uuid: str, experiment_uuid_or_name:str, test: Test) -> None:
        """Save new test or update existing test for given model/output"""
    
        self.data_session.connect(get_project_file_name(project_name))

        selected_test_json_obj = None
        selected_json_output_obj = self.__get_output_json_obj(model_uuid_or_name_or_output_uuid)
        selected_json_experiment_obj = self.__get_json_experiment_by_model(self.data_session.json_file, selected_json_output_obj["model_ref"], experiment_uuid_or_name)

        test.experiment_ref = Experiment(uuid=selected_json_experiment_obj["uuid"])
        
        for json_test_obj in selected_json_output_obj["tests"]:
            if selected_json_experiment_obj["uuid"] == json_test_obj["experiment_ref"] and (json_test_obj["name"] == test.name or json_test_obj["uuid"] == test.uuid):
                selected_test_json_obj = json_test_obj
                break

        patched_json_test_obj = self.__serialize_test(test)
        patched_json_test_obj["experiment_ref"] = selected_json_experiment_obj["uuid"]

        if selected_test_json_obj:
            selected_test_json_obj.update(patched_json_test_obj) 
        else:
            selected_json_output_obj["tests"].append(patched_json_test_obj)

        self.data_session.save()
        self.data_session.dispose()


    def __get_output_json_obj(self, model_uuid_or_name_or_output_uuid: str) -> Any:
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name_or_output_uuid or json_model_obj["name"] == model_uuid_or_name_or_output_uuid:
                selected_model_uuid = json_model_obj["uuid"]

        for json_output_obj in self.data_session.json_file["outputs"]:
            if json_output_obj["uuid"] == model_uuid_or_name_or_output_uuid or json_output_obj["model_ref"] == model_uuid_or_name_or_output_uuid or json_output_obj["model_ref"] == selected_model_uuid:
                return json_output_obj

    def __get_json_experiment_by_model(self, project_json_obj, model_uuid: str, experiment_uuid_or_name: str) -> List[Any]:
        for model_json_obj in project_json_obj["models"]:
            if model_json_obj["uuid"] == model_uuid:
                for experiment_json_obj in model_json_obj["experiments"]:
                    if experiment_json_obj["uuid"] == experiment_uuid_or_name or experiment_json_obj["name"] == experiment_uuid_or_name:
                        return  experiment_json_obj

    def __deserialize_test(self, project_ref, json_test_obj) -> Test:
        test_domain_obj = Test()
        test_domain_obj.project_ref     = project_ref
        test_domain_obj.uuid            = json_test_obj["uuid"]
        test_domain_obj.name            = json_test_obj["name"]
        test_domain_obj.experiment_ref  = Experiment(uuid=json_test_obj["experiment_ref"])
        test_domain_obj.model_file      = json_test_obj["model_file"]
        test_domain_obj.outputs         = [] 
        for output in json_test_obj["outputs"]:
            test_domain_obj.outputs.append(output)
        test_domain_obj.reports         = [] 
        for report in json_test_obj["reports"]:
            test_domain_obj.reports.append(report)
        test_domain_obj.parameters      = json_test_obj["parameters"]
        
        return test_domain_obj

    def __serialize_test(self, test_domain_obj: Test) -> Any:
        json_test_obj = dict({})

        if not test_domain_obj.uuid:
            test_domain_obj.uuid = str(uuid4())

        json_test_obj["uuid"]           = test_domain_obj.uuid
        json_test_obj["name"]           = test_domain_obj.name
        json_test_obj["experiment_ref"] = test_domain_obj.experiment_ref.uuid
        json_test_obj["model_file"]     = test_domain_obj.model_file
        json_test_obj["outputs"]        = test_domain_obj.outputs
        json_test_obj["reports"]        = test_domain_obj.reports
        json_test_obj["parameters"]     = test_domain_obj.parameters
        
        return json_test_obj