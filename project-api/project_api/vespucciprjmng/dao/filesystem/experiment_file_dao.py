
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.experiment_dao import ExperimentDAO
from project_api.vespucciprjmng.dao.filesystem.json_data_connector import (
    JSONDataConnector,
)
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import (
    ProjectFileDAO,
)
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.domain.experiment import Experiment
from project_api.vespucciprjmng.utils import read_json_attribute


class ExperimentFileDAO(ExperimentDAO):
    """Experiment data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)

    def get_all(self, project_name: str, model_uuid_or_name: str = None) -> List[Experiment]:
        """Get all stored inputs (without details) inside a project"""

        if not model_uuid_or_name:
            raise Exception("'get_all' experiments with project_id=" +project_name+ " is not implemented")
        
        self.data_session.connect(get_project_file_name(project_name))

        experiment_domain_objs = []

        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                for json_experiment_obj in json_model_obj["experiments"]:    
                    experiment_domain_objs.append(self.__deserialize_experiment(project_ref=project_name, json_experiment_obj=json_experiment_obj))
        
        self.data_session.dispose()

        return experiment_domain_objs

    def get(self, project_name: str, model_uuid_or_name: str = None, experiment_uuid_or_name: str = None) -> Experiment:
        """Get experiment (with all details) given a model or input ID"""

        self.data_session.connect(get_project_file_name(project_name))

        experiment_domain_obj = None

        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                for json_experiment_obj in json_model_obj["experiments"]:
                    if json_experiment_obj["uuid"] == experiment_uuid_or_name or json_experiment_obj["name"] == experiment_uuid_or_name:
                        experiment_domain_obj = self.__deserialize_experiment(project_ref=project_name, json_experiment_obj=json_experiment_obj)
        
        self.data_session.dispose()

        return experiment_domain_obj
    
    def delete(self, project_name: str, model_uuid_or_name: str, experiment_uuid_or_name: str) -> None:
        """Delete experiment from related project"""
        self.data_session.connect(get_project_file_name(project_name))

        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                filtered_json_experiment_objs = []
                for json_experiment_obj in json_model_obj["experiments"]:
                    if json_experiment_obj["uuid"] != experiment_uuid_or_name and json_experiment_obj["name"] != experiment_uuid_or_name:
                        filtered_json_experiment_objs.append(json_experiment_obj)
                json_model_obj["experiments"] = filtered_json_experiment_objs

        self.data_session.save()
        self.data_session.dispose()

    def save(self, project_name: str, model_uuid_or_name: str, experiment: Experiment) -> None:
        """Save new experiment or update existing input"""
    
        self.data_session.connect(get_project_file_name(project_name))
        
        selected_json_model_obj = None
        selected_json_experiment_obj = None
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                selected_json_model_obj = json_model_obj
                for json_experiment_obj in json_model_obj["experiments"]:
                    if json_experiment_obj["uuid"] == experiment.uuid or json_experiment_obj["name"] == experiment.name:
                        selected_json_experiment_obj = json_experiment_obj
                        break

        patched_json_experiment_obj = self.__serialize_experiment(experiment)

        if selected_json_experiment_obj:
            selected_json_experiment_obj.update(patched_json_experiment_obj)
        else:
            selected_json_model_obj["experiments"].append(patched_json_experiment_obj)

        self.data_session.save()
        self.data_session.dispose()

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