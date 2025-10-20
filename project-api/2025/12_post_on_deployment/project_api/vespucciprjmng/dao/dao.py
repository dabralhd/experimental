from abc import abstractmethod
from typing import List, TypeVar

from project_api.vespucciprjmng.dao.data_session import DataSession

DOMAIN_TYPE = TypeVar('DOMAIN_TYPE') 
ID_TYPE     = TypeVar('ID_TYPE', int, str) 

class DAO():

    _data_session: DataSession
    @property
    def data_session(self):
        return self._data_session

    @abstractmethod
    def getAll() -> List[DOMAIN_TYPE]:
        pass

    @abstractmethod
    def get(id: ID_TYPE) -> DOMAIN_TYPE:
        pass

    @abstractmethod
    def delete(self, domainObj: DOMAIN_TYPE) -> None:
        pass

    @abstractmethod
    def save(self, domainObj: DOMAIN_TYPE) -> None:
        pass
    
    def __init__(self, data_session: DataSession):
        self._data_session = data_session
        pass