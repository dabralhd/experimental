
from project_api.vespucciprjmng.domain.tool import Parameters, Tool


class DBTool(Tool):
    """DB Tool data model"""
    
    @property
    def uuid(self) -> str:
        return self.__uuid

    @uuid.setter 
    def uuid(self, value: str):
        self.__uuid = value

    def __init__(self, uuid: str= None, name: str = None, version: str = None, parameters: Parameters = None):
        super().__init__(name, version, parameters)
        self.__uuid = uuid
    
