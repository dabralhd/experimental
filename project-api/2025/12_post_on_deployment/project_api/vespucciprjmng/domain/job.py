from enum import Enum

from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ


class JobType(Enum):
    JOB                 = "job"
    JUPYTER_NOTEBOOK    = "jupyter_notebook"
    UNKNOWN             = "unknown"

class OperationType(Enum):
    LOG_UPLOADING       = "log_uploading"
    LOG_CONVERSION      = "log_conversion"
    MODEL_ANALYSIS      = "model_training"
    OUTPUT_GENERATION   = "output_generation"
    UNKNOWN             = "unknown"

class State(Enum):
    ON_GOING                = "ongoing"
    TERMINATED_WITH_SUCCESS = "success"
    TERMINATED_WITH_FAILURE = "failure"

class Job(DomainOBJ):
    """Job data model"""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter 
    def name(self, value: str):
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

    def __init__(self, name: str = None, version: str = None, template_id: str = None):
        self.__name         = name
        self.__version         = version
        self.__template_id  = template_id
    