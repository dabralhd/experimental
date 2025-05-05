from typing import List

from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ
from datetime import datetime

class Job():
    @property
    def name(self) -> str:
        return self.__name

    @name.setter 
    def type(self, value: str):
        self.__name = value
    
    @property
    def version(self) -> str:
        return self.__version

    @version.setter 
    def version(self, value: str):
        self.__version = value
    
    @property
    def template_id(self) -> str:
        return self.__template_id

    @template_id.setter 
    def template_id(self, value: str):
        self.__template_id = value

    def __init__(self, name: str, version: str = None, template_id: str = None):
        self.__name = name
        self.__version = version
        self.__template_id = template_id
        pass

class Runtime():
    @property
    def type(self) -> str:
        return self.__type

    @type.setter 
    def type(self, value: str):
        self.__type = value
    
    @property
    def jobs(self) -> List[Job]:
        return self.__jobs

    @jobs.setter 
    def jobs(self, value: List[Job]):
        self.__jobs = value
    
    def __init__(self, type: str, jobs: List[Job] = None):
        self.__type = type
        self.__jobs = jobs
        pass

class Training(DomainOBJ):
    @property
    def last_update_time(self) -> str:
        return self.__last_update_time

    @last_update_time.setter
    def last_update_time(self, value: datetime):
        self.__last_update_time = str(value)
        
    @property
    def creation_time(self) -> str:
        return self.__creation_time
    
    @creation_time.setter
    def creation_time(self, value: datetime):
        self.__creation_time = str(value)
    
    @property
    def runtime(self) -> Runtime:
        return self.__runtime
    
    @property
    def configuration(self) -> str:
        return self.__configuration
    
    @property
    def reports(self) -> List[str]:
        return self.__reports
    
    @property
    def artifacts(self) -> List[str]:
        return self.__artifacts

    @runtime.setter 
    def runtime(self, value: Runtime):
        self.__runtime = value

    @configuration.setter
    def configuration(self, value: str):
        self.__configuration = value
    
    @reports.setter
    def reports(self, value: List[str]):
        self.__reports = value

    @artifacts.setter
    def artifacts(self, value: List[str]):
        self.__artifacts = value

    def __init__(self, runtime: Runtime, configuration: str, reports: List[str] = None, artifacts: List[str]=None, creation_time: datetime = None, last_update_time: datetime = None):
        self.__runtime = runtime
        self.__configuration = configuration
        self.__reports = reports
        self.__artifacts = artifacts
        self.__creation_time = str(creation_time)
        self.__last_update_time = str(last_update_time)
        return
