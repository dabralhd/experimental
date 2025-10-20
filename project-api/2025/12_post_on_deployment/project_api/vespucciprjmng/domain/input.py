from enum import Enum
from typing import List

from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ
from project_api.vespucciprjmng.domain.log import Log
from project_api.vespucciprjmng.domain.model import Model
from project_api.vespucciprjmng.domain.tool import Tool


class InputType(Enum):
    BINARY_HSD      = "binary_hsd"
    IMAGE           = "image"
    CSV_SENSORTILE  = "csv_sensortile"
    CSV_UNICO       = "csv_unico"
    CSV_CARTESIAM   = "csv_cartesiam"

class Input(DomainOBJ):
    """Input data model"""

    @property
    def uuid(self) -> str:
        return self.__uuid

    @uuid.setter 
    def uuid(self, value:str):
        self.__uuid = value

    @property
    def model_ref(self) -> Model:
        return self.__model_ref

    @model_ref.setter 
    def model_ref(self, value: Model):
        self.__model_ref = value

    @property
    def input_type(self) -> InputType:
        return self.__input_type

    @input_type.setter 
    def input_type(self, value: InputType):
        self.__input_type = value

    @property
    def augmentations(self) -> List[str]:
        return self.__augmentations

    @augmentations.setter 
    def augmentations(self, value: List[str]):
        self.__augmentations = value

    @property
    def logs(self) -> List[Log]:
        return self.__logs

    @logs.setter 
    def logs(self, value: List[Log]):
        self.__logs = value

    @property
    def tools(self) -> List[Tool]:
        return self.__tools

    @tools.setter 
    def tools(self, value: List[Tool]):
        self.__tools = value

    def __init__(self, uuid: str = None, model_ref: Model = None, input_type: InputType = None, augmentations: List[str] = None, logs: List[Log] = None, tools: List[Tool] = None):
        self.__uuid         = uuid
        self.__model_ref    = model_ref
        self.__input_type   = input_type
        self.__augmentations= augmentations
        self.__logs         = logs
        self.__tools        = tools
    
