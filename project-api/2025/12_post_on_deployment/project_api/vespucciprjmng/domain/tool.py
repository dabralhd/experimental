
from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ


class Parameters(object):
    pass

class Tool(DomainOBJ):
    """Tool data model"""
    
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

    __parameters: Parameters
    @property
    def parameters(self) -> Parameters:
        return self.__parameters

    @parameters.setter 
    def parameters(self, value: Parameters):
        self.__parameters = value

    def __init__(self, name: str = None, version: str = None, parameters: Parameters = None):
        self.__name = name
        self.__version = version
        self.__parameters = parameters
    
