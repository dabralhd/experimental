
from typing import Any

from project_api.vespucciprjmng.dao.filesystem.json_data_connector import (
    JSONDataConnector,
)
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import (
    ProjectFileDAO,
)
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.training_dao import TrainingDAO
from project_api.vespucciprjmng.domain.training import Runtime, Training


class DataSufficiencyFileDAO(TrainingDAO):
    """Data Sufficiency data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)    

    def get(self, project_name: str, model_uuid_or_name: str) -> Training:
        """Get data sufficiency (with all details) given project/model"""
        
        self.data_session.connect(get_project_file_name(project_name))
        training_json_obj = None
        
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                if "data_sufficiency" in json_model_obj and json_model_obj["data_sufficiency"]:
                    training_json_obj = self.__deserialize_training(json_model_obj["data_sufficiency"])
                break

        self.data_session.dispose()
        return training_json_obj
    
    def delete(self, project_name: str, model_uuid_or_name: str) -> None:
        """Delete data sufficiency from related project/model"""
        self.data_session.connect(get_project_file_name(project_name))

        filtered_training_domain_objs = []
        
        self.data_session.save()
        self.data_session.dispose()

    def patch(self, project_name: str, model_uuid_or_name: str, data_sufficiency: Training):
        """Patch and Update existing data sufficiency for given model"""
        """Only update configuration, reports and artifacts"""

        self.data_session.connect(get_project_file_name(project_name))

        selected_data_sufficiency_json_obj = None
        selected_json_model_obj = None

        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                selected_json_model_obj =  json_model_obj
                if "data_sufficiency" in json_model_obj:
                    selected_data_sufficiency_json_obj = json_model_obj["data_sufficiency"]
                break
        
        patched_json_training_obj = self.__serialize_training(data_sufficiency)

        # Check update contents
        if data_sufficiency.artifacts:
            selected_data_sufficiency_json_obj["artifacts"] = patched_json_training_obj["artifacts"]
        if data_sufficiency.reports:
            selected_data_sufficiency_json_obj["reports"] = patched_json_training_obj["reports"]
        if data_sufficiency.configuration:
            selected_data_sufficiency_json_obj["configuration"] = patched_json_training_obj["configuration"]
        
        self.data_session.save()
        self.data_session.dispose()

    def clone(self, project_name: str, clone_model_uuid_or_name: str, model_uuid_or_name: str) -> None:
        self.data_session.connect(get_project_file_name(project_name))

        selected_json_model_obj = None
        cloned_json_model_obj = None
        
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == clone_model_uuid_or_name or json_model_obj["name"] == clone_model_uuid_or_name:
                selected_json_model_obj = json_model_obj
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                cloned_json_model_obj = json_model_obj

        if "data_sufficiency" in selected_json_model_obj:
            cloned_json_training_obj = self.__copy_training(selected_json_model_obj["data_sufficiency"])
            cloned_json_model_obj["data_sufficiency"] = cloned_json_training_obj

        self.data_session.save()
        self.data_session.dispose()

    def save(self, project_name: str, model_uuid_or_name: str, data_sufficiency: Training) -> None:
        """Save new data sufficiency or update existing ds for given model"""
    
        self.data_session.connect(get_project_file_name(project_name))

        selected_training_json_obj = None
        selected_json_model_obj = None
        
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                selected_json_model_obj =  json_model_obj
                if "data_sufficiency" in json_model_obj:
                    selected_training_json_obj = json_model_obj["data_sufficiency"]
                break

        patched_json_training_obj = self.__serialize_training(data_sufficiency)

        if selected_training_json_obj:
            selected_training_json_obj.update(patched_json_training_obj) 
        else:
            selected_json_model_obj["data_sufficiency"] = patched_json_training_obj

        self.data_session.save()
        self.data_session.dispose()
            
    def __deserialize_training(self, json_training_obj) -> Training:
        runtime = Runtime(type="None", jobs=[])
        training_domain_obj = Training(runtime=runtime, configuration="None", reports=[], artifacts=[])
        
        training_domain_obj.runtime.type = json_training_obj["runtime"]["type"]
        training_domain_obj.runtime.jobs = []
        for job in json_training_obj["runtime"]["jobs"]:
            training_domain_obj.runtime.jobs.append(job)

        training_domain_obj.configuration = json_training_obj["configuration"]
        training_domain_obj.artifacts = []
        for artifact in json_training_obj["artifacts"]:
            training_domain_obj.artifacts.append(artifact)
        training_domain_obj.reports = []
        for report in json_training_obj["reports"]:
            training_domain_obj.reports.append(report)
        
        return training_domain_obj

    def __serialize_training(self, training_domain_obj: Training) -> Any:
        json_training_obj = dict({})

        json_training_obj["runtime"] = {
            'type': training_domain_obj.runtime.type,
            'jobs': training_domain_obj.runtime.jobs
        }
        json_training_obj["configuration"] = training_domain_obj.configuration if training_domain_obj.configuration else "None"
        json_training_obj["reports"] = training_domain_obj.reports if training_domain_obj.reports else []
        json_training_obj["artifacts"] = training_domain_obj.artifacts if training_domain_obj.artifacts else []
        
        return json_training_obj
    
    def __copy_training(self, json_training_obj) -> Any:
        copy_json_training_obj = dict({})

        copy_json_training_obj["runtime"] = {
            'type': json_training_obj["runtime"]["type"],
            'jobs': json_training_obj["runtime"]["jobs"]
        }
        copy_json_training_obj["configuration"] = json_training_obj["configuration"]
        copy_json_training_obj["reports"] = json_training_obj["reports"]
        copy_json_training_obj["artifacts"] = json_training_obj["artifacts"]
        
        return copy_json_training_obj