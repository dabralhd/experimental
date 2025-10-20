from typing import Any, List

from project_api.vespucciprjmng.dao.filesystem.json_data_connector import (
    JSONDataConnector,
)
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import (
    ProjectFileDAO,
)
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.job_dao import JobDAO
from project_api.vespucciprjmng.domain.job import Job


class JobFileDAO(JobDAO):
    """Training data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)    

    def get_all(self, project_name: str, model_uuid_or_name: str) -> List[Job]:
        """Get training jobs given project/model"""
        
        self.data_session.connect(get_project_file_name(project_name))
        jobs = []
        
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                if "training" in json_model_obj:
                    for job in json_model_obj["training"]["runtime"]["jobs"]:
                        jobs.append(self.__deserialize_job(job))
                break        

        self.data_session.dispose()

        return jobs

    def save(self, project_name: str, model_uuid_or_name: str, job: Job) -> None:
        """Append new job to training runtime for given project/model"""
    
        self.data_session.connect(get_project_file_name(project_name))

        selected_training_json_obj = None
        
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                selected_json_model_obj =  json_model_obj
                if "training" in json_model_obj:
                    selected_training_json_obj = json_model_obj["training"]
                break

        patched_json_job_obj = self.__serialize_job(job)

        if selected_training_json_obj:
            job_present = False
            for job in selected_json_model_obj["training"]["runtime"]["jobs"]:
                if job["name"] == patched_json_job_obj["name"] and job["template_id"] == patched_json_job_obj["template_id"]:
                    job_present = True
                    job["version"] == patched_json_job_obj["version"]
            if not job_present:
                selected_json_model_obj["training"]["runtime"]["jobs"].append(patched_json_job_obj)

        self.data_session.save()
        self.data_session.dispose()
            
    def __deserialize_job(self, json_job_obj) -> Job:
        job_domain_obj = Job(name="None", version="", template_id="")
        
        job_domain_obj.name = json_job_obj["name"]
        job_domain_obj.version = json_job_obj["version"]
        job_domain_obj.template_id = json_job_obj["template_id"]
        
        return job_domain_obj

    def __serialize_job(self, job_domain_obj: Job) -> Any:
        json_job_obj = dict({})

        json_job_obj["name"] = job_domain_obj.name
        json_job_obj["version"] = job_domain_obj.version
        json_job_obj["template_id"] = job_domain_obj.template_id
        
        return json_job_obj


