
from typing import Any
from uuid import uuid4
from project_api.vespucciprjmng.dao.filesystem.json_data_connector import JSONDataConnector
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import ProjectFileDAO
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.training_dao import TrainingDAO
from project_api.vespucciprjmng.domain.training import Training, Runtime
from datetime import datetime
from project_api.vespucciprjmng.utils import read_json_attribute


class TrainingFileDAO(TrainingDAO):
    """Training data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)    

    def get(self, project_name: str, model_uuid_or_name: str) -> Training:
        """Get training (with all details) given project/model"""
        
        self.data_session.connect(get_project_file_name(project_name))

        training_json_obj = None
        
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                if "training" in json_model_obj:
                    training_json_obj = self.__deserialize_training(json_model_obj["training"])
                break

        self.data_session.dispose()

        return training_json_obj
    
    def delete(self, project_name: str, model_uuid_or_name: str) -> None:
        """Delete training from related project/model"""
        self.data_session.connect(get_project_file_name(project_name))

        filtered_training_domain_objs = []
        # selected_json_output_obj = self.__get_output_json_obj(model_uuid_or_name)
        # selected_json_experiment_obj = self.__get_json_experiment_by_model(self.data_session.json_file, selected_json_output_obj["model_ref"], experiment_uuid_or_name)

        # for json_test_obj in selected_json_output_obj["tests"]:
        #     if not (selected_json_experiment_obj["uuid"] == json_test_obj["experiment_ref"] and (json_test_obj["name"] == test_name_or_uuid or json_test_obj["uuid"] == test_name_or_uuid)) :
        #         filtered_test_domain_objs.append(json_test_obj)
        #         break
        # selected_json_output_obj["tests"] = filtered_test_domain_objs
        
        self.data_session.save()
        self.data_session.dispose()

    def patch(self, project_name: str, model_uuid_or_name: str, training: Training):
        """Patch and Update existing training for given model"""
        """Only update configuration, reports and artifacts"""

        self.data_session.connect(get_project_file_name(project_name))

        selected_training_json_obj = None
        selected_json_model_obj = None

        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                selected_json_model_obj =  json_model_obj
                if "training" in json_model_obj:
                    selected_training_json_obj = json_model_obj["training"]
                break
        
        patched_json_training_obj = self.__serialize_training(training)

        # Check update contents
        if training.artifacts:
            selected_training_json_obj["artifacts"] = patched_json_training_obj["artifacts"]
        if training.reports:
            selected_training_json_obj["reports"] = patched_json_training_obj["reports"]
        if training.configuration:
            selected_training_json_obj["configuration"] = patched_json_training_obj["configuration"]
        patched_json_training_obj["last_update_time"] = datetime.now()    
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

        if "training" in selected_json_model_obj:
            cloned_json_training_obj = self.__copy_training(selected_json_model_obj["training"])
            cloned_json_model_obj["training"] = cloned_json_training_obj

        self.data_session.save()
        self.data_session.dispose()

    def save(self, project_name: str, model_uuid_or_name: str, training: Training) -> None:
        """Save new training or update existing training for given model"""
    
        self.data_session.connect(get_project_file_name(project_name))

        selected_training_json_obj = None
        selected_json_model_obj = None
        
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                selected_json_model_obj =  json_model_obj
                if "training" in json_model_obj:
                    selected_training_json_obj = json_model_obj["training"]
                break

        patched_json_training_obj = self.__serialize_training(training)

        if selected_training_json_obj:
            selected_training_json_obj.update(patched_json_training_obj) 
        else:
            selected_json_model_obj["training"] = patched_json_training_obj

        # self.data_session.json_file["last_update_time"]      = selected_json_model_obj.last_update_time
        # self.data_session.json_file["creation_time"]          = selected_json_model_obj.creation_time

        self.data_session.save()
        self.data_session.dispose()
            
    def __deserialize_training(self, json_training_obj) -> Training:
        runtime = Runtime(type="None", jobs=[])
        training_domain_obj = Training(runtime=runtime, configuration="None", reports=[], artifacts=[])
        # training_domain_obj = Training(training=pipeline)
        
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
        training_domain_obj.creation_time = read_json_attribute(json_training_obj, "creation_time")
        training_domain_obj.last_update_time = read_json_attribute(json_training_obj, "last_update_time")
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
        json_training_obj["last_update_time"] = training_domain_obj.last_update_time
        json_training_obj["creation_time"] = training_domain_obj.creation_time
        
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
        copy_json_training_obj["last_update_time"] = json_training_obj["last_update_time"]
        copy_json_training_obj["creation_time"] = json_training_obj["creation_time"]
        
        return copy_json_training_obj