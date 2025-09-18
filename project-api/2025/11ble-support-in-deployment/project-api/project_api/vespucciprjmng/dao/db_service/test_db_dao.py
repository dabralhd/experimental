
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.db_service.http_connector import (
    HTTPDataConnector,
)
from project_api.vespucciprjmng.dao.db_service.service_specs import (
    DBServiceSpecs,
)
from project_api.vespucciprjmng.dao.test_dao import TestDAO
from project_api.vespucciprjmng.domain.experiment import Experiment
from project_api.vespucciprjmng.domain.test import Test


class TestDBDAO(TestDAO):
    """Test data access object for DB Service"""
    
    def __init__(self, service_uri: str):
        self.__http_connector = HTTPDataConnector(service_uri)

    def get_all(self, project_uuid: str, model_uuid_or_name_or_output_uuid: str, experiment_uuid_or_name: str = None) -> List[Test]:
        """Get all stored tests (without details) inside a project/model or output"""
        
        if not experiment_uuid_or_name:
            raise Exception("'get_all' tests with experiment_id=" +experiment_uuid_or_name+ " is not implemented")
        
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        selected_json_output_obj = self.__get_output_json_obj(project_json_obj, model_uuid_or_name_or_output_uuid)
        selected_json_experiment_obj = self.__get_json_experiment_by_model(project_json_obj, selected_json_output_obj["model_ref"], experiment_uuid_or_name)
        test_domain_objs = []

        for json_test_obj in selected_json_output_obj["tests"]:
            if not experiment_uuid_or_name:
                test_domain_obj = self.__deserialize_test(project_ref=project_uuid, json_test_obj=json_test_obj)
                test_domain_objs.append(test_domain_obj)
            else:
                if json_test_obj["experiment_ref"] == selected_json_experiment_obj["uuid"]:
                    test_domain_obj = self.__deserialize_test(project_ref=project_uuid, json_test_obj=json_test_obj)
                    test_domain_objs.append(test_domain_obj)
        
        return test_domain_objs

    def get(self, project_uuid: str, model_uuid_or_name_or_output_uuid: str, experiment_uuid_or_name: str, test_uuid_or_name: str) -> Test:
        """Get test (with all details) given project/model or output"""
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        test_domain_obj = None
        selected_json_output_obj = self.__get_output_json_obj(project_json_obj, model_uuid_or_name_or_output_uuid)
        selected_json_experiment_obj = self.__get_json_experiment_by_model(project_json_obj, selected_json_output_obj["model_ref"], experiment_uuid_or_name)

        for json_test_obj in selected_json_output_obj["tests"]:
            if selected_json_experiment_obj["uuid"] == json_test_obj["experiment_ref"] or selected_json_experiment_obj["name"] == experiment_uuid_or_name and (json_test_obj["name"] == test_uuid_or_name or json_test_obj["uuid"] == test_uuid_or_name):
                test_domain_obj = self.__deserialize_test(project_ref=project_uuid, json_test_obj=json_test_obj)
                break

        return test_domain_obj
    
    def delete(self, project_uuid: str, model_uuid_or_name_or_output_uuid: str, experiment_uuid_or_name: str, test_uuid_or_name: str) -> None:
        """Delete test from related project/model/output"""

        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        selected_json_output_obj = self.__get_output_json_obj(project_json_obj, model_uuid_or_name_or_output_uuid=model_uuid_or_name_or_output_uuid)
        selected_json_experiment_obj = self.__get_json_experiment_by_model(project_json_obj, selected_json_output_obj["model_ref"], experiment_uuid_or_name)

        for json_test_obj in selected_json_output_obj["tests"]:
            if selected_json_experiment_obj["uuid"] == json_test_obj["experiment_ref"] or selected_json_experiment_obj["name"] == experiment_uuid_or_name and (json_test_obj["name"] == test_uuid_or_name or json_test_obj["uuid"] == test_uuid_or_name):
                self.__http_connector.delete(DBServiceSpecs.getTestPath(project_uuid=project_uuid, output_uuid=selected_json_output_obj["uuid"], test_uuid=json_test_obj["uuid"]))

    def update(self, project_uuid: str, model_uuid_or_name_or_output_uuid: str, experiment_uuid_or_name:str, test: Test) -> None:
        """Update existing test for given model/output"""
    
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))

        selected_json_output_obj    = self.__get_output_json_obj(project_json_obj, model_uuid_or_name_or_output_uuid)        
        selected_json_experiment_obj = self.__get_json_experiment_by_model(project_json_obj, selected_json_output_obj["model_ref"], experiment_uuid_or_name)

        test.experiment_ref = Experiment(uuid=selected_json_experiment_obj["uuid"])
        body = self.__serialize_test(test)
        self.__http_connector.put(DBServiceSpecs.getTestPath(project_uuid=project_uuid, output_uuid=selected_json_output_obj["uuid"], test_uuid=test.uuid), body)

    def save(self, project_uuid: str, model_uuid_or_name_or_output_uuid: str, experiment_uuid_or_name:str, test: Test) -> None:
        """Save new test for given model/output"""
        if not test.uuid:
            test.uuid = str(uuid4())
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        selected_json_output_obj    = self.__get_output_json_obj(project_json_obj, model_uuid_or_name_or_output_uuid)        
        selected_json_experiment_obj = self.__get_json_experiment_by_model(project_json_obj, selected_json_output_obj["model_ref"], experiment_uuid_or_name)
        test.experiment_ref = Experiment(uuid=selected_json_experiment_obj["uuid"])
        body = self.__serialize_test(test)
        self.__http_connector.post(DBServiceSpecs.getTestsPath(project_uuid=project_uuid, output_uuid=selected_json_output_obj["uuid"]), body)
        
    def __get_output_json_obj(self, project_json_obj, model_uuid_or_name_or_output_uuid: str) -> Any:
        for json_model_obj in project_json_obj["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name_or_output_uuid or json_model_obj["name"] == model_uuid_or_name_or_output_uuid:
                selected_model_uuid = json_model_obj["uuid"]

        for json_output_obj in project_json_obj["outputs"]:
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
        json_test_obj["description"]    = ""
        json_test_obj["experiment_ref"] = test_domain_obj.experiment_ref.uuid
        json_test_obj["model_file"]     = test_domain_obj.model_file
        json_test_obj["outputs"]        = test_domain_obj.outputs
        json_test_obj["reports"]        = test_domain_obj.reports
        json_test_obj["parameters"]     = test_domain_obj.parameters
        
        return json_test_obj