
from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ


class Dataset(DomainOBJ):
    """Dataset data model"""
    
    @property
    def name(self) -> str:
        return self.__name

    @name.setter 
    def name(self, value: str):
        self.__name = value

    @property
    def dataset_id(self) -> str:
        return self.__dataset_id

    @dataset_id.setter 
    def dataset_id(self, value: str):
        self.__dataset_id = value    

    def __init__(self, name: str = None, dataset_id: str = None):
        self.__name = name
        self.__dataset_id = dataset_id
    
