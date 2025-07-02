from typing import Iterable, List, Optional

from project_api.vespucciprjmng.domain.deployment import Deployment, Application
from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ
from project_api.vespucciprjmng.domain.model import Model
from datetime import datetime

class Project(DomainOBJ):
    """Project data model"""

    @property
    def uuid(self) -> Optional[str]:
        return self.__uuid

    @uuid.setter 
    def uuid(self, value: Optional[str]):
        self.__uuid = value

    @property
    def name(self) -> Optional[str]:
        return self.__name

    @name.setter 
    def name(self, value: Optional[str]):
        self.__name = value

    @property
    def type(self) -> Optional[str]:
        return self.__type

    @type.setter 
    def type(self, value: Optional[str]):
        self.__type = value

    @property
    def display_name(self) -> Optional[str]:
        return self.__display_name

    @property
    def creation_time(self) -> Optional[str]:
        return self.__creation_time
    
    @creation_time.setter
    def creation_time(self, creation_time: Optional[str]=None):
        self.__creation_time = creation_time
        
    @property
    def last_update_time(self) -> Optional[str]:
        return self.__last_update_time
    
    @last_update_time.setter
    def last_update_time(self, last_update_time: Optional[str]=None):
        self.__last_update_time = last_update_time 
   
    @display_name.setter 
    def display_name(self, value: Optional[str]):
        self.__display_name = value

    @property
    def description(self) -> Optional[str]:
        return self.__description

    @description.setter 
    def description(self, value: Optional[str]):
        self.__description = value

    @property
    def version(self) -> Optional[str]:
        return self.__version

    @version.setter 
    def version(self, value: Optional[str]):
        self.__version = value

    @property
    def models(self) -> List[Model]:
        return self.__models
    
    @models.setter 
    def models(self, value: List[Model]):
        self.__models = value

    @property
    def applications(self) -> List[Application]:
        return self.__applications
    
    @applications.setter 
    def applications(self, value: List[Application]):
        self.__applications = value

    @property
    def deployments(self) -> List[Deployment]:
        return self.__deployments

    @deployments.setter 
    def deployments(self, value: List[Deployment]):
        self.__deployments = value

    @property
    def project_owner_uuid(self) -> Optional[str]:
        return self.__project_owner_uuid

    @project_owner_uuid.setter
    def project_owner_uuid(self, value: Optional[str]):
        self.__project_owner_uuid = value

    def __init__(self, uuid: Optional[str] = None, name: Optional[str] = None, type: Optional[str] = None, description: Optional[str] = None, version: Optional[str] = None, models: List[Model] = [], applications: List[Application] = [], deployments: List[Deployment] = [], display_name: Optional[str] = None, project_owner_uuid: Optional[str] = None):
        self.__uuid         = uuid
        self.__name         = name
        self.__type         = type
        self.__description  = description
        self.__version      = version
        self.__models       = models
        self.__applications = applications
        self.__deployments  = deployments
        self.__display_name  = display_name
        self.__project_owner_uuid = project_owner_uuid
        self.__creation_time = str(datetime.now()) 
        self.__last_update_time = self.__creation_time
