from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.db_service.http_connector import (
    HTTPDataConnector,
)
from project_api.vespucciprjmng.dao.db_service.service_specs import (
    DBServiceSpecs,
)
from project_api.vespucciprjmng.dao.project_dao import ProjectDAO
from project_api.vespucciprjmng.domain.project import Project


class ProjectDBDAO(ProjectDAO):
    """Project data access object for DB Service"""
    
    @property
    def user_id(self) -> str:
        return self.__user_id


    def __init__(self, user_id: str, service_uri: str):
        self.__user_id        = user_id
        self.__http_connector = HTTPDataConnector(service_uri)

    def get_all(self) -> List[Project]:
        """Get all stored projects without details"""

        project_domain_objs = []
        # project_db_objs: List[DBProject]     = self.__db_client.get_projects().get()
        project_json_objs = self.__http_connector.get(DBServiceSpecs.getProjectsPath())
        for project_json_obj in project_json_objs:
            if self.user_id == project_json_obj["owner"]:
                project_domain_objs.append(self.__deserialize_project(project_json_obj))

        return project_domain_objs

    def get(self, uuid: str) -> Project:
        """Get stored project with attributes and references details"""
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=uuid))
        if self.user_id == project_json_obj["owner"]:
            project_domain_obj = self.__deserialize_project(project_json_obj)

        return project_domain_obj

    def delete(self, uuid: str) -> None:
        """Delete existing project"""
        self.__http_connector.delete(DBServiceSpecs.getProjectPath(project_uuid=uuid))

    def update(self, project: Project) -> None:
        """Update existing project"""
        project_json_obj = self.__serialize_project(project_domain_obj=project)
        self.__http_connector.put(DBServiceSpecs.getProjectPath(project_uuid=project.uuid), project_json_obj)
        
    def save(self, project: Project) -> None:
        """Save new project project"""
        if not project.uuid:
            project.uuid = str(uuid4())
        project_json_obj = self.__serialize_project(project_domain_obj=project)
        self.__http_connector.post(DBServiceSpecs.getProjectsPath(), project_json_obj)

    def __deserialize_project(self, project_json_obj) -> Project:
        return Project(
            uuid=project_json_obj["uuid"],
            name=project_json_obj["ai_project_name"],
            description=project_json_obj["description"],
            version=project_json_obj["version"],
            inputs=[],
            models=[],
            outputs=[]
        )

    def __serialize_project(self, project_domain_obj: Project) -> Any:
        return {
            "uuid": project_domain_obj.uuid,
            "ai_project_name": project_domain_obj.name,
            "description": project_domain_obj.description,
            "version": project_domain_obj.version,
            "owner": self.user_id
        }