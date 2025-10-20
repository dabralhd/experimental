from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ


class Experiment(DomainOBJ):
    """Experiment data model"""
    
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
    def description(self) -> str:
        return self.__description

    @description.setter 
    def description(self, value: str):
        self.__description = value

    __model_dev_file: str
    @property
    def model_dev_file(self) -> str:
        return self.__model_dev_file

    @model_dev_file.setter 
    def model_dev_file(self, value: str):
        self.__model_dev_file = value

    def __init__(self, uuid: str = None, name: str = None, description: str = None, model_dev_file: str = None):
        self.__uuid         = uuid
        self.__name         = name
        self.__description  = description
        self.__model_dev_file = model_dev_file
    
