
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.db_service.http_connector import (
    HTTPDataConnector,
)
from project_api.vespucciprjmng.dao.db_service.service_specs import (
    DBServiceSpecs,
)
from project_api.vespucciprjmng.dao.experiment_dao import ExperimentDAO
from project_api.vespucciprjmng.domain.experiment import Experiment
from project_api.vespucciprjmng.utils import read_json_attribute


class ExperimentDBDAO(ExperimentDAO):
    """Experiment data access object for DB Service"""
    
    def __init__(self, service_uri: str):
        self.__http_connector = HTTPDataConnector(service_uri)


    def get_all(self, project_uuid: str, model_uuid_or_name: str = None) -> List[Experiment]:
        """Get all stored inputs (without details) inside a project"""

        if not model_uuid_or_name:
            raise Exception("'get_all' experiments with model_id=" +model_uuid_or_name+ " is not implemented")
        
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        experiment_domain_objs = []
        model_json_obj = self.__get_model_json_by_name_or_uuid(json_project_obj=project_json_obj, model_uuid_or_name=model_uuid_or_name)
        
        for json_experiment_obj in model_json_obj["experiments"]:    
            experiment_domain_objs.append(self.__deserialize_experiment(project_ref=project_uuid, json_experiment_obj=json_experiment_obj))
    
        return experiment_domain_objs

    def get(self, project_uuid: str, model_uuid_or_name: str = None, experiment_uuid_or_name: str = None) -> Experiment:
        """Get experiment (with all details) given a model or input ID"""
        project_json_obj        = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        experiment_domain_obj   = None
        model_json_obj          = self.__get_model_json_by_name_or_uuid(json_project_obj=project_json_obj, model_uuid_or_name=model_uuid_or_name)
        experiment_json_obj     = self.__get_experiment_json_by_name_or_uuid(json_model_obj=model_json_obj, experiment_uuid_or_name=experiment_uuid_or_name)

        experiment_domain_obj = self.__deserialize_experiment(project_ref=project_uuid, json_experiment_obj=experiment_json_obj)
        return experiment_domain_obj
    
    def delete(self, project_uuid: str, model_uuid_or_name: str, experiment_uuid_or_name: str) -> None:
        """Delete experiment from related project"""
        project_json_obj    = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        model_json_obj      = self.__get_model_json_by_name_or_uuid(json_project_obj=project_json_obj, model_uuid_or_name=model_uuid_or_name)
        experiment_json_obj = self.__get_experiment_json_by_name_or_uuid(json_model_obj=model_json_obj, experiment_uuid_or_name=experiment_uuid_or_name)
        self.__http_connector.delete(DBServiceSpecs.getExperimentPath(project_uuid=project_uuid, model_uuid=model_json_obj["uuid"], experiment_uuid=experiment_json_obj["uuid"]))

    def update(self, project_uuid: str, model_uuid_or_name: str, experiment: Experiment) -> None:
        """Save new experiment or update existing input"""
        project_json_obj= self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        model_json_obj  = self.__get_model_json_by_name_or_uuid(json_project_obj=project_json_obj, model_uuid_or_name=model_uuid_or_name)
        model_uuid      = model_json_obj["uuid"]
        experiment_json_obj = self.__serialize_experiment(experiment_domain_obj=experiment)
        self.__http_connector.put(DBServiceSpecs.getExperimentPath(project_uuid=project_uuid, model_uuid=model_uuid, experiment_uuid=experiment.uuid), experiment_json_obj)

    def save(self, project_uuid: str, model_uuid_or_name: str, experiment: Experiment) -> None:
        """Save new experiment or update existing input"""
        if not experiment.uuid:
            experiment.uuid = str(uuid4())
        project_json_obj= self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        model_json_obj  = self.__get_model_json_by_name_or_uuid(json_project_obj=project_json_obj, model_uuid_or_name=model_uuid_or_name)
        model_uuid      = model_json_obj["uuid"]
        experiment_json_obj = self.__serialize_experiment(experiment_domain_obj=experiment)
        self.__http_connector.post(DBServiceSpecs.getExperimentsPath(project_uuid=project_uuid, model_uuid=model_uuid), experiment_json_obj)

    def __get_model_json_by_name_or_uuid(self, json_project_obj, model_uuid_or_name: str):
        for json_model_obj in json_project_obj["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                return json_model_obj

    def __get_experiment_json_by_name_or_uuid(self, json_model_obj, experiment_uuid_or_name: str):
        for json_experiment_obj in json_model_obj["experiments"]:
            if json_experiment_obj["uuid"] == experiment_uuid_or_name or json_experiment_obj["name"] == experiment_uuid_or_name:
                return json_experiment_obj

    def __deserialize_experiment(self, project_ref, json_experiment_obj: Any) -> Experiment:
        experiment_domain_obj = Experiment()
        experiment_domain_obj.project_ref    = project_ref
        experiment_domain_obj.uuid           = json_experiment_obj["uuid"]
        experiment_domain_obj.name           = json_experiment_obj["name"]
        experiment_domain_obj.description    = read_json_attribute(json_experiment_obj, "description")
        experiment_domain_obj.model_dev_file = read_json_attribute(json_experiment_obj, "model_dev_file")

        return experiment_domain_obj

    def __serialize_experiment(self, experiment_domain_obj: Experiment) -> Any:
        json_experiment_obj = dict({})

        if not experiment_domain_obj.uuid:
            experiment_domain_obj.uuid = str(uuid4())

        json_experiment_obj["uuid"]          = experiment_domain_obj.uuid
        json_experiment_obj["name"]          = experiment_domain_obj.name
        json_experiment_obj["description"]    = experiment_domain_obj.description
        json_experiment_obj["model_dev_file"] = experiment_domain_obj.model_dev_file
        
        return json_experiment_obj