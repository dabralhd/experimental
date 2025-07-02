from os import path
import os
from typing import List
from uuid import uuid4
from re import search

from project_api.vespucciprjmng.dao.filesystem.json_data_connector import JSONDataConnector
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name, get_project_name_from_filename, is_project_file
from project_api.vespucciprjmng.dao.project_dao import ProjectDAO
from project_api.vespucciprjmng.domain.deployment import Deployment
from project_api.vespucciprjmng.domain.input import Input
from project_api.vespucciprjmng.domain.model import Model
from project_api.vespucciprjmng.domain.output import Output
from project_api.vespucciprjmng.domain.project import Project
from project_api.vespucciprjmng.utils import read_json_attribute


class ProjectFileDAO(ProjectDAO):
    """Project data access object for JSON file"""
    
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)

    def get_all(self) -> List[Project]:
        """Get all stored projects without details"""

        file_names = self.data_session.list_files()
        projects = []
        for name in file_names:
            try:
                os.path.exists(os.path.join(self.data_session._uri, name, "ai_" + name + ".json"))
                project             = Project()
                project.name        = name
                project.project_ref = project.name
                projects.append(project)
            except:
                pass
            
        return projects
    
    def get(self, name: str) -> Project:
        """Get stored project with attributes and references details"""
        self.data_session.connect(get_project_file_name(name))
        
        project = Project()
        project.uuid        = self.data_session.json_file["uuid"]
        project.name        = self.data_session.json_file["ai_project_name"]
        if "type" in self.data_session.json_file:
            project.type = self.data_session.json_file["type"]
        if "display_name" in self.data_session.json_file:
            project.display_name = self.data_session.json_file["display_name"]
        project.project_ref = project.name
        project.description = read_json_attribute(self.data_session.json_file, "description")
        project.version     = read_json_attribute(self.data_session.json_file, "version")
        project.creation_time     = read_json_attribute(self.data_session.json_file, "creation_time")
        project.last_update_time     = read_json_attribute(self.data_session.json_file, "last_update_time")
        if "project_owner_uuid" in self.data_session.json_file:
            project.project_owner_uuid = self.data_session.json_file["project_owner_uuid"]
        
        project.models       = []
        project.deployments  = []

        for model_obj in self.data_session.json_file["models"]:
            model_domain_obj                = Model()
            model_domain_obj.project_ref    = project.name
            model_domain_obj.uuid           = model_obj["uuid"]

            project.models.append(model_domain_obj)

        for deployment_obj in self.data_session.json_file["deployments"]:
            deployment_domain_obj                = Deployment()
            deployment_domain_obj.project_ref    = project.name
            deployment_domain_obj.uuid           = deployment_obj["uuid"]

            project.deployments.append(deployment_domain_obj)

        self.data_session.dispose()
        
        return project
    
    def delete(self, name: str) -> None:
        """Delete project from filesystem"""
        
        self.data_session.delete(get_project_file_name(name))


    def save(self, project: Project) -> None:
        """Save new project or update existing project"""

        if not project.uuid:
            project.uuid = str(uuid4())
            self.data_session.init(get_project_file_name(project.name))

        self.data_session.connect(get_project_file_name(project.name))

        self.data_session.json_file["uuid"]             = project.uuid
        self.data_session.json_file["ai_project_name"]  = project.name
        self.data_session.json_file["type"]             = project.type
        self.data_session.json_file["display_name"]     = project.display_name
        self.data_session.json_file["description"]      = project.description
        self.data_session.json_file["version"]          = project.version
        self.data_session.json_file["last_update_time"]      = project.last_update_time
        self.data_session.json_file["creation_time"]          = project.creation_time
        if project.project_owner_uuid:
            self.data_session.json_file["project_owner_uuid"] = project.project_owner_uuid

        if not "models" in self.data_session.json_file:
            self.data_session.json_file["models"] = []

        if not "deployments" in self.data_session.json_file:
            self.data_session.json_file["deployments"] = []

        if not "applications" in self.data_session.json_file:
            self.data_session.json_file["applications"] = []

        self.data_session.save()
        self.data_session.dispose()
        
