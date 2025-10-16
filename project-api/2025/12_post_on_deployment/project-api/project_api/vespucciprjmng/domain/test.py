from typing import List

from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ
from project_api.vespucciprjmng.domain.experiment import Experiment


class Parameters(object):
    pass

class Test(DomainOBJ):
    """Test data model"""

    @property
    def uuid(self) -> str:
        return self.__uuid

    @uuid.setter 
    def uuid(self, value: str):
        self.__uuid = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter 
    def name(self, value: str):
        self.__name = value

    @property
    def experiment_ref(self) -> Experiment:
        return self.__experiment_ref

    @experiment_ref.setter 
    def experiment_ref(self, value: Experiment):
        self.__experiment_ref = value

    @property
    def model_file(self) -> str:
        return self.__model_file

    @model_file.setter 
    def model_file(self, value: str):
        self.__model_file = value

    @property
    def reports(self) -> List[str]:
        return self.__reports

    @reports.setter 
    def reports(self, value: List[str]):
        self.__reports = value

    @property
    def outputs(self) -> List[str]:
        return self.__outputs

    @outputs.setter 
    def outputs(self, value: List[str]):
        self.__outputs = value

    @property
    def parameters(self) -> Parameters:
        return self.__parameters

    @parameters.setter 
    def parameters(self, value: Parameters):
        self.__parameters = value
   
    def __init__(self, uuid: str = None, name: str = None, experiment_ref: Experiment = None, model_file: str = None, reports: List[str] = None, outputs: List[str] = None, parameters: Parameters = None):
        self.__uuid             = uuid
        self.__name             = name
        self.__experiment_ref   = experiment_ref
        self.__model_file       = model_file
        if not reports:
            reports = []
        self.__reports          = reports
        if not outputs:
            outputs = []
        self.__outputs          = outputs
        self.__parameters       = parameters